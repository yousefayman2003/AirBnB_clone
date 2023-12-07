#!/usr/bin/python3
"""The `Console` Module that Defines HBNB command interpeter."""
from models.base_model import BaseModel
from models.user import User
from models import storage
import json
import cmd


class HBNBCommand(cmd.Cmd):
    """
        Defines HBNB command interpreter.

        Public Class Attributes:
            prompt (str): command prompt.
    """

    # make a custom prompt
    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel, "User": User}

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id."""

        if self.is_valid(arg, "create"):
            new_obj = self.classes[arg]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance.

        based on the class name and id.
        """

        if self.is_valid(arg, "show"):
            # get all objects from the data source
            req_ins = arg.replace(" ", ".")
            ins_data = storage.all().get(req_ins)

            if not ins_data:
                print("** no instance found **")
            else:
                print(ins_data)

    def do_all(self, arg):
        """Prints all string representation of all instances.

        based or not on the class name.
        """

        # retrieve data of all objects from source file
        data = {**storage.all()}

        for key, value in data.items():
            data[key] = value.to_dict()

        # no filter needed
        if not arg:
            print(data)
        # filter data based on a class name
        elif arg in self.classes:
            filtered_data = {}
            for obj, obj_data in data.items():
                cls_name = obj_data["__class__"]
                if cls_name == arg:
                    filtered_data[obj] = obj_data
            print(filtered_data)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance.

        based on the class name and id by adding or updating attribute.
        """

        if self.is_valid(arg, "update"):
            # try to access the requested object to update it
            args = arg.split()
            attr, value = args[2:]
            all_objs = storage.all()
            req_ins_key = ".".join(args[:2])
            req_ins = all_objs.get(req_ins_key)

            if not req_ins:
                print("** no instance found **")
                return

            # Cast the type of value
            # depend on the data type of value of attr key
            if type(req_ins.__dict__.get(attr)) is int:
                value = int(value)
            elif type(req_ins.__dict__.get(attr)) is float:
                value = float(value)
            # update the requested object and save the updated in the json file
            setattr(req_ins, attr, value)
            storage.save()

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""

        if self.is_valid(arg, "destroy"):
            # get all objects from the data source
            req_ins = arg.replace(" ", ".")
            all_data = storage.all()
            ins_data = all_data.get(req_ins)

            if not ins_data:
                print("** no instance found **")
            else:
                del all_data[req_ins]
                storage.__objects = all_data
                storage.save()

    def do_quit(self, arg):
        """Quit command to exit from the program\n"""
        return True

    def do_EOF(self, arg):
        """EOF detected to exit from the program"""
        return True

    def is_valid(self, arg, operation):
        """Create, Delete, and Display data from a data source."""

        # checks that the requested command is valid
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
        elif len(args) == 2 and operation == "update":
            print("** attribute name missing **")
            return False
        elif len(args) == 3 and operation == "update":
            print("** value missing **")
            return False

        return True

    def emptyline(self):
        """does nothing if empty line."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
