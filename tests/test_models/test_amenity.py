#!/usr/bin/python3
"""Defines unittests for amenity."""

import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from unittest.mock import patch


class TestEmptyAmenity(unittest.TestCase):
    """Test cases for an empty Amenity object"""

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

    def test_empty_amenity_instance(self):
        """Test creation of an empty Amenity instance"""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity, Amenity)
        self.assertIsNone(amenity.name)


if __name__ == '__main__':
    unittest.main()
