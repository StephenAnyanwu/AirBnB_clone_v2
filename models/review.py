#!/usr/bin/python3

"""In this module defines the Review class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Review(BaseModel):
    """Impliments the Review class"""
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
