#!/usr/bin/python3
"""The `FileStorage` module."""
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review


class FileStorage:
    """
        Serializes instances to a JSON file and deserializes JSON file to instances.

        Private class attributes:
            __file_path (str): path to the JSON file.
            __objects (dict): empty but will store all objects by <class name>.id.

        Public instance methods:
            all(self): returns the dictionary __objects.
            new(self, obj): sets in __objects the obj with key <obj class name>.id.
            save(self): serializes __objects to the JSON file (path: __file_path).
            reload(self): deserializes the JSON file to __objects (only if the JSON file (__file_path) exists.

    """
    __file_path = "file.json"
    __objects = {}
    classes = {"BaseModel": BaseModel, "User": User,
               "City": City, "Review": Review,
               "Amenity": Amenity, "Place": Place,
               "State": State}

    def all(self):
        """returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """
            sets in __objects the obj with key <obj class name>.id.

            Args:
                obj (object): object to store.
        """
        self.__objects[f"{obj.__class__.__name__ }.{obj.id}"] = obj

    def save(self):
        """serializes __objects to the JSON file."""
        objects = {}

        for key, obj in self.__objects.items():
            objects[key] = obj.to_dict()

        with open(self.__file_path, "w") as f:
            json.dump(objects, f, indent=4)

    def reload(self):
        """
            deserializes the JSON file to __objects (only if the JSON
            file exists), otherwise do nothing.
        """
        try:
            with open(self.__file_path, "r") as f:
                data = json.loads(f.read())

                for value in data.values():
                    cls_name = value["__class__"]
                    obj = self.classes[cls_name](**value)
                    self.new(obj)
        except:
            pass
