#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import MySQLdb
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        models.storage.reload()
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)
        e = os.environ
        cls.conn = MySQLdb.connect(host=e.get("HBNB_MYSQL_HOST", "localhost"),
                                   port=3306,
                                   user=e.get("HBNB_MYSQL_USER", "root"),
                                   passwd=e.get("HBNB_MYSQL_PWD", "root"),
                                   db=e.get("HBNB_MYSQL_DB", "hbnb_dev_db"),
                                   charset="utf8")

        cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class"""
        cls.cur.close()
        cls.conn.close()

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Test that count returns the number of all DBStorage objects"""
        my_len = len(models.storage.all().values())
        self.cur.execute("SELECT * FROM states")
        s = len(self.cur.fetchall())
        self.cur.execute("SELECT * FROM amenities")
        a = len(self.cur.fetchall())
        self.cur.execute("SELECT * FROM cities")
        c = len(self.cur.fetchall())
        self.cur.execute("SELECT * FROM places")
        p = len(self.cur.fetchall())
        self.cur.execute("SELECT * FROM reviews")
        r = len(self.cur.fetchall())
        self.cur.execute("SELECT * FROM users")
        u = len(self.cur.fetchall())
        total = s + a + c + p + r + u
        self.assertEqual(total, my_len)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_state(self):
        """Test count returns the number of State DBStorage.__objects"""
        my_len = len(models.storage.all("State").values())
        self.cur.execute("SELECT * FROM states")
        self.assertEqual(len(self.cur.fetchall()), my_len)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_state(self):
        """Test that get returns the specific State DBStorage.__objects"""
        try:
            self.cur.execute("SELECT id FROM states LIMIT 1")
            stuff = [x for x in self.cur.fetchall()]
            my_id = ""
            if len(stuff) > 0:
                more_stuff = [y for y in stuff]
                if len(more_stuff) > 0:
                    my_id = more_stuff[0]
            other_name = models.storage.get('State', my_id)
            if other_name is not None:
                other_name = other_name.name
            else:
                other_name = ""
            my_id = "'" + my_id + "'"
            self.cur.execute("SELECT name FROM states WHERE id=" + my_id)
            stuff = [x for x in self.cur.fetchall()]
            my_name = ""
            if len(stuff) > 0:
                more_stuff = [y for y in stuff]
                if len(more_stuff) > 0:
                    my_name = more_stuff[0]

            self.assertEqual(my_name, other_name)
        except:
            self.assertEqual(True, False)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
