#!/usr/bin/python3
"""Module containing unit test for State Class"""
import unittest
import json
import os
from datetime import datetime
from uuid import uuid4
from time import sleep
from models.state import State
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):
    """unit test for State Class"""

    def test_attributes(self):
        """Test if instance has all attributes of class"""
        obj = State()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))
        self.assertTrue(hasattr(obj, "name"))

    def test_init_no_kwargs(self):
        """Test Constructor with no kwargs"""
        now = datetime.now()
        obj = State()

        # check if obj is saved:
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)

        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.name, str)
        self.assertEqual(obj.created_at, now)
        self.assertEqual(obj.updated_at, now)
        self.assertEqual(obj.name, "")
        self.assertEqual(
            str(type(obj)), "<class 'models.state.State'>")

    def test_init_kwargs(self):
        """Test Constructor with kwargs"""
        obj = State(id=str(uuid4), created_at="2023-05-15T08:30:00.000000",
                    updated_at="2023-10-22T18:45:30.500000",
                    name="Free parking")
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.name, str)
        self.assertEqual(obj.created_at, datetime(2023, 5, 15, 8, 30))
        self.assertEqual(obj.updated_at, datetime(
            2023, 10, 22, 18, 45, 30, 500000))
        self.assertEqual(obj.name, "Free parking")
        self.assertEqual(
            str(type(obj)), "<class 'models.state.State'>")

    def test_equality(self):
        """test if two objects are not equal"""
        obj1 = State()
        obj2 = State(**obj1.to_dict())

        self.assertNotEqual(obj1, obj2)

    def test_str(self):
        """test the __str__ method"""
        obj = State()
        string = f"[State] ({obj.id}) {obj.__dict__}"
        self.assertEqual(obj.__str__(), string)

    def test_save(self):
        """Test the save method"""
        obj = State()
        # get last updated at time
        time = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertNotEqual(time, obj.updated_at)

    def test_save_file(self):
        """Tests the save method of storage inside save"""
        obj = State()
        obj.save()
        key = f"{obj.__class__.__name__}.{obj.id}"

        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, "r") as file:
            data = json.load(file).keys()
            self.assertTrue(key in data)

    def test_to_dict(self):
        """Test the to_dict method"""
        obj = State()
        dictionary = obj.to_dict()
        self.assertIsInstance(dictionary, dict)
        self.assertIn("__class__", dictionary)
        self.assertIsInstance(dictionary["__class__"], str)
        self.assertEqual(dictionary["__class__"], "State")
        self.assertIn("id", dictionary)
        self.assertIn("created_at", dictionary)
        self.assertIsInstance(dictionary["created_at"], str)
        self.assertIn("updated_at", dictionary)
        self.assertIsInstance(dictionary["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
