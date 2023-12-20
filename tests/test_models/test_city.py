#!/usr/bin/python3
"""Defines unittests for city"""

import unittest
from models.city import City
from models.state import State
from models.engine.db_storage import DBStorage


class TestCityModel(unittest.TestCase):
    """Test cases for the City model"""

    def setUp(self):
        """Set up the test environment"""
        self.storage = DBStorage()
        self.storage.reload()

    def test_create_city(self):
        """Test creating a City associated with a State"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()

        city = City(name="San Francisco", state_id=state.id)
        self.storage.new(city)
        self.storage.save()
        city_from_db = self.storage.all(City).values()

        self.assertTrue(city_from_db)
        self.assertTrue(len(city_from_db) > 0)


if __name__ == '__main__':
    unittest.main()
