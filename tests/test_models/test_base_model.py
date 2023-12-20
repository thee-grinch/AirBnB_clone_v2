#!/usr/bin/python3
"""Defines unittests for basemodel"""

import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class"""

    def test_attributes(self):
        """Test attributes creation"""
        base = BaseModel()
        self.assertTrue(hasattr(base, 'id'))
        self.assertTrue(hasattr(base, 'created_at'))
        self.assertTrue(hasattr(base, 'updated_at'))


if __name__ == '__main__':
    unittest.main()
