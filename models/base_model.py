#!/usr/bin/python3
"""This is the base model class for AirBnB"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """This class will defines all common attributes/methods
    for other classes

    Attributes
    ----------
    id : str (class attribute)
        a column containing a unique string/identifier (60 characters)
    created_at : datetime.datetime (class attribute, default: current datetime)
        a column containing a datetime a new user is created.
    updated_at : datetime.datetime (class attribute, default: current datetime)
        a column containing a datetime user is updated.

    """

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """returns a string
        Return:
            returns a string of class name, id, and dictionary
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__)

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """updates the public instance attribute 'updated_at' to current
        datetime (i.e the current datetime object is saved)and save the
        object (user data)
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of
        __dict__ of the instance.
        The created_at and updated_at keys in the dictionary
        are of string type datetime
        """
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()

        if "_sa_instance_state" in my_dict:
            my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """ Deletes Current Instance from the storage models.storage """
        models.storage.delete(self)
