#!/usr/bin/python3

"""In this module defines User class"""

from models.base_model import BaseModel


class User(BaseModel):
    """Defines the class User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
