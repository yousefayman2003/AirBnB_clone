#!/usr/bin/python3
"""Module containing unit test for FileStorage Class"""
import unittest
import json
from models.engine.file_storage import FileStorage


class TestBaseModel(unittest.TestCase):
    """Unit test for FileStorage Class"""

    def setUp(self):
        """First code to run before any test"""
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = "test.json"

    def test_all(self):
        """Test all method"""
        self.assertIsInstance(self.storage.all(), dict)
        objects = self.storage._FileStorage__objects
        self.assertEqual(self.storage.all(), objects)

    def test_new(self):
        """Test new method"""
        classes = self.storage.classes

        for class_name in classes.values():
            obj = class_name()
            self.storage.new(obj)
            self.assertIn(f"{obj.__class__.__name__}.{obj.id}",
                          self.storage.all().keys())
            self.assertIn(obj, self.storage.all().values())

    def test_save(self):
        """Test save method"""
        classes = self.storage.classes

        for class_name in classes.values():
            obj = class_name()
            self.storage.new(obj)
            self.storage.save()

            # check if object is successfully saved in file
            with open(self.storage._FileStorage__file_path, "r") as f:
                data = json.load(f)
                self.assertIn(
                    f"{obj.__class__.__name__}.{obj.id}", data.keys())

    def test_reload(self):
        """Test reload method"""
        classes = self.storage.classes

        for class_name in classes.values():
            obj = class_name()
            self.storage.new(obj)
            self.storage.save()
            self.storage.reload()
            # check if object is successfully reloaded
            self.assertIn(f"{obj.__class__.__name__}.{obj.id}",
                          self.storage._FileStorage__objects.keys())


if __name__ == "__main__":
    unittest.main()
