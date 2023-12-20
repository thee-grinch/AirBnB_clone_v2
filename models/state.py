#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models import storage
from models.city import City
from sqlalchemy import String, Column
from models.base_model import BaseModel
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="state", cascade="delete")

    else:
        @property
        def cities(self):
            """Gets list of all related cities"""
            cities = []
            for city in list(storage.all(City).values()):
                if city.state_id == self.id:
                    cities.append(city)
            return cities
