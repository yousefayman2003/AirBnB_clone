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
    Serializes objects to a JSON file and deserializes JSON file to instances.

    Private class attributes:
        __file_path (str): path to the JSON file.
        __objects (dict): empty but will store all objects by <class name>.id.

    Public instance methods:
        all(self): returns the dictionary __objects.
        new(self, obj): sets in __objects the obj with key <obj class name>.id.
        save(self): serializes __objects to the JSON file (path: __file_path).
        reload(self): deserializes the JSON file (if it exists) to __objects.
    """
    __file_path = "file.json"
    __objects = {}
    classes = {"BaseModel": BaseModel, "User": User,
               "City": City, "Review": Review,
               "Amenity": Amenity, "Place": Place,
               "State": State}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        Args:
            obj (object): object to store.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file."""
        objects = {key: obj.to_dict() for key, obj in self.__objects.items()}

        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(objects, f, indent=4)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON
        file exists), otherwise do nothing.
        """
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                for value in data.values():
                    cls_name = value["__class__"]
                    obj = FileStorage.classes[cls_name](**value)
                    self.new(obj)
        except Exception:
            pass
