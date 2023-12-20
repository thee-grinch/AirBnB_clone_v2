from io import StringIO
import os
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from console import HBNBCommand
from models.user import User
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from datetime import datetime
from unittest.mock import patch

class TestUserDBStorage(unittest.TestCase):
    """Test cases for User class with DBStorage"""

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

    def test_user_instance(self):
        """Test User instance creation"""
        user = User()
        self.assertIsInstance(user, BaseModel)
        self.assertIsInstance(user, User)

    def test_user_attributes(self):
        """Test User attributes"""
        user = User(email="gui@hbtn.io", password="guipwd", first_name="Guillaume", last_name="Snow")
        self.assertEqual(user.email, "gui@hbtn.io")
        self.assertEqual(user.password, "guipwd")
        self.assertEqual(user.first_name, "Guillaume")
        self.assertEqual(user.last_name, "Snow")

    def test_user_attributes_db(self):
        """Test User attributes in the database"""
        user = User(email="gui@hbtn.io", password="guipwd", first_name="Guillaume", last_name="Snow")
        self.session.add(user)
        self.session.commit()
        user_id = user.id

        # Fetch the user from the database
        db_user = self.session.query(User).filter_by(id=user_id).first()

        self.assertEqual(db_user.email, "gui@hbtn.io")
        self.assertEqual(db_user.password, "guipwd")
        self.assertEqual(db_user.first_name, "Guillaume")
        self.assertEqual(db_user.last_name, "Snow")

    def test_user_create_command(self):
        """Test create User command in the console"""
        with patch('sys.stdout', new=StringIO()) as output:
            command = 'create User email="gui@hbtn.io" password="guipwd" first_name="Guillaume" last_name="Snow"'
            HBNBCommand().onecmd(command)
            user_id = output.getvalue().strip()

        # Fetch the user from the database
        db_user = self.session.query(User).filter_by(id=user_id).first()

        self.assertEqual(db_user.email, "gui@hbtn.io")
        self.assertEqual(db_user.password, "guipwd")
        self.assertEqual(db_user.first_name, "Guillaume")
        self.assertEqual(db_user.last_name, "Snow")

if __name__ == '__main__':
    unittest.main()
