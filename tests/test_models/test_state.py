#!/usr/bin/python3
"""Defines unittests for state."""

import unittest
from models.state import State
from models.engine.db_storage import DBStorage


class TestStateModel(unittest.TestCase):
    """Test cases for the State model"""

    def setUp(self):
        """Set up the test environment"""
        self.storage = DBStorage()
        self.storage.reload()

    def test_create_state(self):
        """Test creating a State"""
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        state_from_db = self.storage.all(State).values()

        self.assertTrue(state_from_db)
        self.assertTrue(len(state_from_db) > 0)


if __name__ == '__main__':
    unittest.main()
