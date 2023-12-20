#!/usr/bin/python3
"""Defines unittests for place."""

import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.place import Place
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from datetime import datetime
from unittest.mock import patch


class TestEmptyPlace(unittest.TestCase):
    """Test cases for an empty Place object"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                   format(os.getenv('HBNB_MYSQL_USER'),
                                          os.getenv('HBNB_MYSQL_PWD'),
                                          os.getenv('HBNB_MYSQL_HOST'),
                                          os.getenv('HBNB_MYSQL_DB'),
                                          pool_pre_ping=True))
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """Create a new session for each test"""
        self.session = self.Session()

    def tearDown(self):
        """Close the session after each test"""
        self.session.close()

    def test_empty_place_instance(self):
        """Test creation of an empty Place instance"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertIsInstance(place, Place)

        # Check that attributes are None or empty
        self.assertIsNone(place.city_id)
        self.assertIsNone(place.user_id)
        self.assertIsNone(place.name)
        self.assertIsNone(place.description)
        self.assertIsNone(place.number_rooms)
        self.assertIsNone(place.number_bathrooms)
        self.assertIsNone(place.max_guest)
        self.assertIsNone(place.price_by_night)
        self.assertIsNone(place.latitude)
        self.assertIsNone(place.longitude)


if __name__ == '__main__':
    unittest.main()
