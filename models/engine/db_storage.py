#!/usr/bin/python3

"""In this module defines DBStorage class"""


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class DBStorage:
    """Defines DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """
        
        """
        username = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db_name = os.getenv("HBNB_MYSQL_DB")

        db_url = f"mysql+mysqldb://{username}:{password}@{host}/{db_name}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session (self.__session) all objects
        depending of the class name (cls). If cls is None, return all objects
        from the current database session.

        Parameters
        ----------
        cls: class optional (default=None)
            Class objects to be queried

        Returns
        -------
        dict
            A dictionary of objects of one type of class currently stored
            in the database if cls is not None, else a dictionary of all
            objects currently stored in the database.
        """
        objs = []
        if cls:
            # If cls is a string, convert it to a class
            if isinstance(cls, str):
                try:
                    cls = eval(cls)
                except Exception as e:
                    pass
            if issubclass(cls, Base):
                # Retrieve from database all objects of cls and append
                # them to objs list
                objs.extend(self.__session.query(cls).all())
        else:
            for subclass in Base.__subclasses__():
                # Retrieve from database all objects of subclass and append
                # them to objs list
                objs.extend(self.__session.query(subclass).all())
        objs_dict = {}
        for obj in objs:
            key = f"{objs.__class__.__name__}.{obj.id}"
            try:
                del obj._sa_instance_state
                obj[key] = obj
            except Exception as e:
                pass
        return objs_dict

    def new(self, obj):
        """
        Add object to the current database session (self.__session)

        Paraemters
        ----------
        obj: object
            Object to be added to the current database session.
        """
        self.__session.add(obj)
      
    def save(self):
        """
        Commit all changes of the current database session (self.__session)
        """
        self.__session.commit()
      
    def delete(self, obj=None):
        """
        Delete from the current database session obj if not None

        Parameters
        ----------
          object : class oject, optional (default=None)
            Object to be deleted from curret database session.
        """
        self.__session.delete(obj)
      
    def reload(self):
        """
        Create all tables in the database
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()