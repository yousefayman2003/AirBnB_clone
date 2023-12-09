#!/usr/bin/python3
"""Module containing unit test for Review Class"""
import unittest
import json
import os
from datetime import datetime
from uuid import uuid4
from time import sleep
from models.review import Review
from models.engine.file_storage import FileStorage


class TestReview(unittest.TestCase):
    """unit test for Review Class"""

    def test_attributes(self):
        """Test if instance has all attributes of class"""
        obj = Review()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))
        self.assertTrue(hasattr(obj, "place_id"))
        self.assertTrue(hasattr(obj, "user_id"))
        self.assertTrue(hasattr(obj, "text"))

    def test_init_no_kwargs(self):
        """Test Constructor with no kwargs"""
        now = datetime.now()
        obj = Review()

        # check if obj is saved:
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)

        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.place_id, str)
        self.assertIsInstance(obj.user_id, str)
        self.assertIsInstance(obj.text, str)
        self.assertEqual(obj.created_at, now)
        self.assertEqual(obj.updated_at, now)
        self.assertEqual(obj.place_id, "")
        self.assertEqual(obj.user_id, "")
        self.assertEqual(obj.text, "")
        self.assertEqual(
            str(type(obj)), "<class 'models.review.Review'>")

    def test_init_kwargs(self):
        """Test Constructor with kwargs"""
        obj = Review(id=str(uuid4), created_at="2023-05-15T08:30:00.000000",
                     updated_at="2023-10-22T18:45:30.500000",
                     place_id="1", user_id="24", text="text")
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.place_id, str)
        self.assertIsInstance(obj.user_id, str)
        self.assertIsInstance(obj.text, str)
        self.assertEqual(obj.created_at, datetime(2023, 5, 15, 8, 30))
        self.assertEqual(obj.updated_at, datetime(
            2023, 10, 22, 18, 45, 30, 500000))
        self.assertEqual(obj.place_id, "1")
        self.assertEqual(obj.user_id, "24")
        self.assertEqual(obj.text, "text")
        self.assertEqual(
            str(type(obj)), "<class 'models.review.Review'>")

    def test_equality(self):
        """test if two objects are not equal"""
        obj1 = Review()
        obj2 = Review(**obj1.to_dict())

        self.assertNotEqual(obj1, obj2)

    def test_str(self):
        """test the __str__ method"""
        obj = Review()
        string = f"[Review] ({obj.id}) {obj.__dict__}"
        self.assertEqual(obj.__str__(), string)

    def test_save(self):
        """Test the save method"""
        obj = Review()
        # get last updated at time
        time = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertNotEqual(time, obj.updated_at)

    def test_save_file(self):
        """Tests the save method of storage inside save"""
        obj = Review()
        obj.save()
        key = f"{obj.__class__.__name__}.{obj.id}"

        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, "r") as file:
            data = json.load(file).keys()
            self.assertTrue(key in data)

    def test_to_dict(self):
        """Test the to_dict method"""
        obj = Review()
        dictionary = obj.to_dict()
        self.assertIsInstance(dictionary, dict)
        self.assertIn("__class__", dictionary)
        self.assertIsInstance(dictionary["__class__"], str)
        self.assertEqual(dictionary["__class__"], "Review")
        self.assertIn("id", dictionary)
        self.assertIn("created_at", dictionary)
        self.assertIsInstance(dictionary["created_at"], str)
        self.assertIn("updated_at", dictionary)
        self.assertIsInstance(dictionary["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
