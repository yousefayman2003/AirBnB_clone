#!/usr/bin/python3
"""Module containing unit test for User Class"""
import unittest
import json
import os
from datetime import datetime
from uuid import uuid4
from time import sleep
from models.user import User
from models.engine.file_storage import FileStorage
from models import storage


class TestUser(unittest.TestCase):
    """unit test for User Class"""

    def setUp(self):
        """First code to run before any test"""
        self.storage = storage
        self.storage._FileStorage__file_path = "test.json"

    def tearDown(self):
        """Code To Run after every test"""
        storage._FileStorage__file_path = FileStorage._FileStorage__file_path

    def test_attributes(self):
        """Test if instance has all attributes of class"""
        obj = User()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))
        self.assertTrue(hasattr(obj, "email"))
        self.assertTrue(hasattr(obj, "password"))
        self.assertTrue(hasattr(obj, "first_name"))
        self.assertTrue(hasattr(obj, "last_name"))

    def test_init_no_kwargs(self):
        """Test Constructor with no kwargs"""
        obj = User()

        # check if obj is saved:
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)

        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.email, str)
        self.assertIsInstance(obj.password, str)
        self.assertIsInstance(obj.first_name, str)
        self.assertIsInstance(obj.last_name, str)
        self.assertEqual(obj.email, "")
        self.assertEqual(obj.password, "")
        self.assertEqual(obj.first_name, "")
        self.assertEqual(obj.last_name, "")
        self.assertEqual(
            str(type(obj)), "<class 'models.user.User'>")

    def test_init_kwargs(self):
        """Test Constructor with kwargs"""
        obj = User(id=str(uuid4), created_at="2023-05-15T08:30:00.000000",
                   updated_at="2023-10-22T18:45:30.500000",
                   email="email@gmail.com", password="123e4",
                   first_name="john", last_name="michel")
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.email, str)
        self.assertIsInstance(obj.password, str)
        self.assertIsInstance(obj.first_name, str)
        self.assertIsInstance(obj.last_name, str)
        self.assertEqual(obj.created_at, datetime(2023, 5, 15, 8, 30))
        self.assertEqual(obj.updated_at, datetime(
            2023, 10, 22, 18, 45, 30, 500000))
        self.assertEqual(obj.email, "email@gmail.com")
        self.assertEqual(obj.password, "123e4")
        self.assertEqual(obj.first_name, "john")
        self.assertEqual(obj.last_name, "michel")
        self.assertEqual(
            str(type(obj)), "<class 'models.user.User'>")

    def test_equality(self):
        """test if two objects are not equal"""
        obj1 = User()
        obj2 = User(**obj1.to_dict())

        self.assertNotEqual(obj1, obj2)

    def test_str(self):
        """test the __str__ method"""
        obj = User()
        string = f"[User] ({obj.id}) {obj.__dict__}"
        self.assertEqual(obj.__str__(), string)

    def test_save(self):
        """Test the save method"""
        obj = User()
        # get last updated at time
        time = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertNotEqual(time, obj.updated_at)

    def test_save_file(self):
        """Tests the save method of storage inside save"""
        obj = User()
        obj.save()
        key = f"{obj.__class__.__name__}.{obj.id}"

        self.assertTrue(os.path.isfile(self.storage._FileStorage__file_path))
        with open(self.storage._FileStorage__file_path, "r") as file:
            data = json.load(file).keys()
            self.assertTrue(key in data)

    def test_to_dict(self):
        """Test the to_dict method"""
        obj = User()
        dictionary = obj.to_dict()
        self.assertIsInstance(dictionary, dict)
        self.assertIn("__class__", dictionary)
        self.assertIsInstance(dictionary["__class__"], str)
        self.assertEqual(dictionary["__class__"], "User")
        self.assertIn("id", dictionary)
        self.assertIn("created_at", dictionary)
        self.assertIsInstance(dictionary["created_at"], str)
        self.assertIn("updated_at", dictionary)
        self.assertIsInstance(dictionary["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
