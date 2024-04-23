#!/usr/bin/python3

"""In this module defines the Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """Impliments the Review class"""
    place_id = ""
    user_id = ""
    text = ""
