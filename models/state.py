#!/usr/bin/python3

"""In this module defines the State class"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref


class State(BaseModel, Base):
    """Impliments the State class"""
    __tablename__ = "states"
  
    name = Column(String(128), nullable=False)

    # If DBStorage
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        # Define the relationship with the City class
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """
            Return the list of City instances with state_id equals to the current State.id
            """
            from models import storage
            from models.city import City
            # Holds City instances with state_id equals to the current State.id
            list_of_cities = []
            for city in storage.all(City).values():
                # If the city has the same state_id as the current State
                if city.state_id == self.id:
                    list_of_cities.append(city)
            return list_of_cities
