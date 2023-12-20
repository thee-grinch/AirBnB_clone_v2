#!/usr/bin/python3

"""Test cases for the console"""
from io import StringIO
import os
import unittest
import MySQLdb
from unittest.mock import patch
from models.engine.file_storage import FileStorage
from models.state import State
from console import HBNBCommand
import console


@patch('console.storage')
class TestConsole(unittest.TestCase):
    """Tests console.py"""

    def query_db(self, string):
        """Sending database query"""
        db = MySQLdb.connect(
            user=os.getenv('HBNB_MYSQL_USER'),
            host=os.getenv('HBNB_MYSQL_HOST'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            port=3306,
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = db.cursor()
        cur.execute(string)
        count = cur.fetchall()
        cur.close()
        db.close()
        return count

    def ouput(self, command):
        """Returns the output from stdout"""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand.onecmd(command)
            return output.getvalue().strip()

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'db',
                     'only db storage is supported for testing')
    def test_create_with_att(self):
        """Test do_create with attribute"""
        sql = "SELECT * FROM states"
        count = self.query_db(sql)
        self.ouput('create State name="California"')
        new_count = self.query_db(sql)
        self.assertEqual(len(new_count) - len(count), 1)

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != 'file',
                     'only file storage is supported for testing')
    def test_state_deletion(self):
        """Test deletion of State objects"""
        fs = FileStorage()
        new_state = State()
        new_state.name = "California"
        fs.new(new_state)
        fs.save()
        all_states = self.fs.all(State)
        initial_state_count = len(all_states)
        fs.delete(new_state)
        fs.save()
        all_states = self.fs.all(State)
        self.assertEqual(len(all_states), initial_state_count - 1)

        # with patch('sys.stdout', new=StringIO()) as id:
        #     HBNBCommand().onecmd('create State name="California_is_good"')
        #     model_id = id.getvalue()
        #     self.assertTrue(len(model_id) > 0)
        # with patch('sys.stdout', new=StringIO()) as contents:
        #     HBNBCommand().onecmd('all State')
        #     self.assertTrue("California is good" in contents.getvalue())
