#!/usr/bin/python3
"""Module containing unit test for Place Class"""
import unittest
import json
import os
from datetime import datetime
from uuid import uuid4
from time import sleep
from models.place import Place
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):
    """unit test for Place Class"""

    def test_attributes(self):
        """Test if instance has all attributes of class"""
        obj = Place()
        self.assertTrue(hasattr(obj, "id"))
        self.assertTrue(hasattr(obj, "created_at"))
        self.assertTrue(hasattr(obj, "updated_at"))
        self.assertTrue(hasattr(obj, "city_id"))
        self.assertTrue(hasattr(obj, "user_id"))
        self.assertTrue(hasattr(obj, "name"))
        self.assertTrue(hasattr(obj, "description"))
        self.assertTrue(hasattr(obj, "number_rooms"))
        self.assertTrue(hasattr(obj, "number_bathrooms"))
        self.assertTrue(hasattr(obj, "max_guest"))
        self.assertTrue(hasattr(obj, "price_by_night"))
        self.assertTrue(hasattr(obj, "latitude"))
        self.assertTrue(hasattr(obj, "longitude"))
        self.assertTrue(hasattr(obj, "amenity_ids"))

    def test_init_no_kwargs(self):
        """Test Constructor with no kwargs"""
        now = datetime.now()
        obj = Place()

        # check if obj is saved:
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertTrue(key in FileStorage._FileStorage__objects)

        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.city_id, str)
        self.assertIsInstance(obj.user_id, str)
        self.assertIsInstance(obj.name, str)
        self.assertIsInstance(obj.number_rooms, int)
        self.assertIsInstance(obj.number_bathrooms, int)
        self.assertIsInstance(obj.max_guest, int)
        self.assertIsInstance(obj.price_by_night, int)
        self.assertIsInstance(obj.longitude, float)
        self.assertIsInstance(obj.latitude, float)
        self.assertIsInstance(obj.amenity_ids, list)
        for id in obj.amenity_ids:
            self.assertIsInstance(id, int)
        self.assertEqual(obj.created_at, now)
        self.assertEqual(obj.updated_at, now)
        self.assertEqual(obj.city_id, "")
        self.assertEqual(obj.user_id, "")
        self.assertEqual(obj.name, "")
        self.assertEqual(obj.number_rooms, 0)
        self.assertEqual(obj.number_bathrooms, 0)
        self.assertEqual(obj.max_guest, 0)
        self.assertEqual(obj.price_by_night, 0)
        self.assertEqual(obj.longitude, 0.0)
        self.assertEqual(obj.latitude, 0.0)
        self.assertEqual(obj.amenity_ids, [])
        self.assertEqual(
            str(type(obj)), "<class 'models.place.Place'>")

    def test_init_kwargs(self):
        """Test Constructor with kwargs"""
        obj = Place(id=str(uuid4), created_at="2023-05-15T08:30:00.000000",
                    updated_at="2023-10-22T18:45:30.500000", city_id="1",
                    user_id="21", name="Jewel", number_rooms=4,
                    number_bathrooms=2, max_guest=2, price_by_night=30,
                    longitude=11.3, latitude=10.345, amenity_ids=[1, 4, 5])
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertIsInstance(obj.city_id, str)
        self.assertIsInstance(obj.user_id, str)
        self.assertIsInstance(obj.name, str)
        self.assertIsInstance(obj.number_rooms, int)
        self.assertIsInstance(obj.number_bathrooms, int)
        self.assertIsInstance(obj.max_guest, int)
        self.assertIsInstance(obj.price_by_night, int)
        self.assertIsInstance(obj.longitude, float)
        self.assertIsInstance(obj.latitude, float)
        self.assertIsInstance(obj.amenity_ids, list)
        for id in obj.amenity_ids:
            self.assertIsInstance(id, int)
        self.assertEqual(obj.created_at, datetime(2023, 5, 15, 8, 30))
        self.assertEqual(obj.updated_at, datetime(
            2023, 10, 22, 18, 45, 30, 500000))
        self.assertEqual(obj.city_id, "1")
        self.assertEqual(obj.user_id, "21")
        self.assertEqual(obj.name, "Jewel")
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.number_bathrooms, 2)
        self.assertEqual(obj.max_guest, 2)
        self.assertEqual(obj.price_by_night, 30)
        self.assertEqual(obj.longitude, 11.3)
        self.assertEqual(obj.latitude, 10.345)
        self.assertEqual(obj.amenity_ids, [1, 4, 5])
        self.assertEqual(
            str(type(obj)), "<class 'models.place.Place'>")

    def test_equality(self):
        """test if two objects are not equal"""
        obj1 = Place()
        obj2 = Place(**obj1.to_dict())

        self.assertNotEqual(obj1, obj2)

    def test_str(self):
        """test the __str__ method"""
        obj = Place()
        string = f"[Place] ({obj.id}) {obj.__dict__}"
        self.assertEqual(obj.__str__(), string)

    def test_save(self):
        """Test the save method"""
        obj = Place()
        # get last updated at time
        time = obj.updated_at
        sleep(0.1)
        obj.save()
        self.assertNotEqual(time, obj.updated_at)

    def test_save_file(self):
        """Tests the save method of storage inside save"""
        obj = Place()
        obj.save()
        key = f"{obj.__class__.__name__}.{obj.id}"

        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, "r") as file:
            data = json.load(file).keys()
            self.assertTrue(key in data)

    def test_to_dict(self):
        """Test the to_dict method"""
        obj = Place()
        dictionary = obj.to_dict()
        self.assertIsInstance(dictionary, dict)
        self.assertIn("__class__", dictionary)
        self.assertIsInstance(dictionary["__class__"], str)
        self.assertEqual(dictionary["__class__"], "Place")
        self.assertIn("id", dictionary)
        self.assertIn("created_at", dictionary)
        self.assertIsInstance(dictionary["created_at"], str)
        self.assertIn("updated_at", dictionary)
        self.assertIsInstance(dictionary["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
