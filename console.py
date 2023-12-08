#!/usr/bin/python3
"""The `Console` Module that Defines HBNB command interpeter."""
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.engine.file_storage import FileStorage
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
    classes = FileStorage.classes

    ######################## Implemented Commands #######################
    def do_all(self, arg):
        """Prints all string representation of all instances.

        based or not on the class name.
        """

        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return

        # retrieve data of all objects from source file
        data = []
        for key, value in storage.all().items():
            if not arg:
                data.append(str(value))
            elif key.split(".")[0] == arg:
                data.append(str(value))

        print(data)

    def do_count(self, arg):
        """counts the number of instances of a specific class"""
        data = {**storage.all()}

        for key, value in data.items():
            data[key] = value.to_dict()

        objects = []
        for obj, obj_data in data.items():
            cls_name = obj_data["__class__"]
            if cls_name == arg:
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

    def do_EOF(self, arg):
        """EOF detected to exit from the program"""
        print("")
        return True

    def do_quit(self, arg):
        """Quit command to exit from the program\n"""
        return True

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

            # Cast the data type of value to the appropriate one
            if value[0] == '"':
                value = value.replace('"', "")
            elif "." in value:
                value = float(value)
            else:
                value = int(value)
            # update the requested object and save the updated in the json file
            setattr(req_ins, attr, value)
            storage.save()

    ######################## Overwrite Built-in Functions #######################
    def emptyline(self):
        """does nothing if empty line."""
        pass

    def precmd(self, line):
        """Overwrite built-in precmd to handle a specific pattern of input.

        handle this pattern of input "<class name>.command(<attributes>)" by
        using the impelemented commands.
        """

        commands = ["all", "count", "show", "destroy", "update"]

        # split the line to [<class name>.command, <arguments>]
        args = line.split("(")

        # parse input only if it's in the expected pattern
        if len(args) == 2:
            cls_name, command = args[0].split(".")
            command_args = args[1][:-1]

            if command not in commands:
                return line

            # if the requested command take attributes
            # rather than the class name extract them
            if len(command_args) > 0:
                # handle update command with dictionary
                if ", {" in command_args and command == "update":
                    obj_id, updates = command_args.split(", {")
                    updates = updates[:-1]
                    updates = updates.split(", ")
                    for i in range(len(updates)):
                        update = updates[i]
                        key, value = update.split(": ")
                        query = f"{cls_name} {obj_id[1:-1]} {key[1:-1]} {value[1:-1]}"
                        if i == len(updates) - 1:
                            return "update " + query
                        self.do_update(query)
                # handle update command with attribute and its new value
                elif ", " in command_args and command == "update":
                    obj_id, attr, value = command_args.split(", ")
                    query = f"update {cls_name} {obj_id[1:-1]} {attr[1:-1]} {value}"
                    return query
                # any other command
                query = f"{command} {cls_name} {command_args[1:-1]}"
                return query
            else:
                return f"{command} {cls_name}"

        return line

    ######################## Helper Functions #######################
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
