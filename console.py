#!/usr/bin/python3
"""
The `Console` Module that Defines HBNB command interpreter.
"""

from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models import storage
from cmd import Cmd


class HBNBCommand(Cmd):
    """
    Defines HBNB command interpreter.

    Public Class Attributes:
        prompt (str): command prompt.
    """

    # make a custom prompt
    prompt = "(hbnb) "
    classes = FileStorage.classes

    # ============== Implemented Commands ================

    def do_all(self, arg):
        """Prints string representation of objs based or not on class name."""
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return

        data = []

        for key, value in storage.all().items():
            if key.split(".")[0] == arg or not arg:
                data.append(str(value))

        print(data)

    def do_count(self, arg):
        """Counts the number of instances of a specific class."""
        objects = []

        if not arg:
            print("** class name missing **")
            return

        for obj in storage.all().values():
            if obj.to_dict()["__class__"] == arg:
                objects.append(obj)

        print(len(objects))

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id."""
        if self.is_valid(arg, "create"):
            new_obj = self.classes[arg]()
            new_obj.save()
            print(new_obj.id)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        if self.is_valid(arg, "destroy"):
            obj_key = arg.replace(" ", ".")
            objects = storage.all()
            obj_data = objects.get(obj_key)

            if obj_data:
                del objects[obj_key]
                storage.__objects = objects
                storage.save()
            else:
                print("** no instance found **")

    def do_EOF(self, arg):
        """EOF detected to exit from the program"""
        return True

    def do_quit(self, arg):
        """Quit command to exit from the program"""
        return True

    def do_show(self, arg):
        """Prints the representation of an obj based on class name and id."""
        if self.is_valid(arg, "show"):
            obj_key = arg.replace(" ", ".")
            obj_data = storage.all().get(obj_key)

            if obj_data:
                print(obj_data)
            else:
                print("** no instance found **")

    def do_update(self, arg):
        """Updates an instance data based on the class name and id."""
        if self.is_valid(arg, "update"):
            args = arg.split()
            cls_name, obj_id = args[:2]
            obj = storage.all().get(f"{cls_name}.{obj_id}")

            if not obj:
                print("** no instance found **")
                return
            if len(args) == 2:
                print("** attribute name missing **")
                return False
            elif len(args) == 3:
                print("** value missing **")
                return False

            attr, value = args[2:4]

            if value[0] in ['"', "'"]:
                value = value[1:-1]
            elif "." in value:
                value = float(value)
            else:
                value = int(value)

            print("updated")
            setattr(obj, attr, value)
            storage.save()

    # ==================== Overwrite Built-in Functionns ====================

    def emptyline(self):
        """Does nothing if empty line."""
        pass

    def precmd(self, line):
        """Overwrite built-in precmd to handle a specific pattern of input."""
        commands = ["all", "count", "show", "destroy", "update"]
        args = line.split("(")

        if len(args) == 2:
            cls_name, command = args[0].split(".")
            cm_args = args[1][:-1]

            if command not in commands:
                return line

            if len(cm_args) > 0:
                if ", {" in cm_args:
                    obj_id, cm_args = cm_args.split(", {")
                    cm_args = cm_args[:-1].split(", ")
                    for i, cm_arg in enumerate(cm_args):
                        key, value = cm_args[i].split(": ")
                        query = f"{cls_name} {obj_id} {key[1:-1]} {value}"
                        if i == len(cm_args) - 1:
                            return "update " + query
                        self.do_update(query)
                elif ", " in cm_args:
                    obj_id, attr, value = cm_args.split(", ")
                    obj_id, attr = obj_id[1:-1], attr[1:-1]
                    query = f"update {cls_name} {obj_id} {attr} {value}"
                    return query
                query = f"{command} {cls_name} {cm_args[1:-1]}"
                return query
            else:
                return f"{command} {cls_name}"

        return line

    # ====================== Helper Functions =======================

    def is_valid(self, arg, operation):
        """Create, Delete, and Display data from a data source."""
        if not arg:
            print("** class name missing **")
            return False

        args = arg.split()
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return False
        elif len(args) == 1 and operation != "create":
            print("** instance id missing **")
            return False

        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
