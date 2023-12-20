#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column


class Amenity(BaseModel, Base):
    """Represents the Amenity table
    contains name field"""
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
