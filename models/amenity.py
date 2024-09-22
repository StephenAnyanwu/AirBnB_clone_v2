#!/usr/bin/python3

"""In this module defines the Amenity class"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Impliments the Amenity class"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
