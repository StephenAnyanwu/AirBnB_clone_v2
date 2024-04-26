#!/usr/bin/python3

"""In this module defines the BaseModel class"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import ForeignKey, create_engine
import uuid
from datetime import datetime
import re


Base = declarative_base()


class BaseModel:
    """
    Impliment the base class for all models

    Attributes
    ----------
    id : str (instance attribute)
        The unique identifier of a created object
    created_at : datetime.datetime (instance attribute)
        The date and time a new user is created.
    updated_at : datetime.datetime (instance attribute)
        The date and time a user (profile) is updated.

    Methods
    -------
    save()
         Update the public instance attribute updated_at with the
         current datetime (i.e the current datetime object is saved)
         and save the object (user data) in a file
    to_dict()
        Return a dictionary containing all keys/values of __dict__
        of the instance
    __str__()
         Return and print the string representation of BaseModel object
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, nullable=False)
  
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        *args : any type (optional, non-keyworded arguments)
        **kwargs : any type (optional, keyworded arguments)
            dictionary of an existing or already created object/instance
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                time_fmt = '%Y-%m-%d %H:%M:%S.%f'
                if key == "id":
                    self.id = str(value)
                elif key == "created_at":
                    # Replace the 'T' in str type  datetime with ' '
                    value_fmt = re.sub('T', ' ', value)
                    # Convert the str type datetime to datetime object
                    self.created_at = datetime.strptime(value_fmt, time_fmt)
                elif key == "updated_at":
                    # Replace the 'T' in str type  datetime with ' '
                    value_fmt = re.sub('T', ' ', value)
                    # Convert the str type datetime to datetime object
                    self.updated_at = datetime.strptime(value_fmt, time_fmt)
                else:
                    if key != "__class__":
                        # If key in kwargs is not the instance attribute except
                        # '__class__', create instance attribute with key/value
                        setattr(self, key, value)
        
    def save(self):
        """
        Update the public instance attribute 'updated_at' with the current
        datetime (i.e the current datetime object is saved)and save the
        object (user data) in a file
        """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of
        __dict__ of the instance.
        The created_at and updated_at keys in the dictionary
        are of string type datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in obj_dict:
            del obj_dict["_sa_instance_state"]
        return obj_dict
    
    def delete(self):
        """Delete the current instance from the storage (models.storage)"""
        from models import storage
        storage.delete(self)
  
    def __str__(self):
        """
        Return and print the string representation of BaseModel object
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
