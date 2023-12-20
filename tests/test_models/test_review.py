#!/usr/bin/python3
"""Defines unittests for review."""

import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.review import Review
from models.base_model import BaseModel


class TestEmptyReview(unittest.TestCase):
    """Test cases for an empty Review object"""

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

    def test_empty_review_instance(self):
        """Test creation of an empty Review instance"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertIsInstance(review, Review)
        self.assertIsNone(review.text)
        self.assertIsNone(review.place_id)
        self.assertIsNone(review.user_id)


if __name__ == '__main__':
    unittest.main()
