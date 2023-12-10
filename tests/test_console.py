#!/usr/bin/python3
"""
The `test_console` Module tests the functionality of each unit
(unit test) in the console module.
"""

from console import HBNBCommand
from io import StringIO
from models import storage
from unittest.mock import patch
import sys
import unittest


class TestHBNBCommand(unittest.TestCase):
    """
    Tests the functionality of HBNBCommand Class of console module.

    TestCases:
    ----------
        - test_help(self)
        - test_help_cm(self)

        - test_do_all(self, arg)
        - test_do_count(self, arg)
        - test_do_create(self, arg)
        - test_do_destroy(self, arg)
        - test_do_EOF(self, arg)
        - test_do_quit(self, arg)
        - test_do_show(self, arg)
        - test_do_update(self, arg)

        - test_emptyline(self)
        - test_precmd(self, arg)

        - is_valid(self, arg, operation)

    Helper instance functions:
        - exec_cm(self, line)
    """

    # ---------------- setUp and tearDown code ---------------- #

    @classmethod
    def setUpClass(cls):
        """
        Initialization code for TestHBNBCommand.
        """
        cls.cmds = [cmd[3:] for cmd in HBNBCommand.__dict__ if "do_" in cmd]

        cls.output_buffer = StringIO()
        sys.stdout = cls.output_buffer

        cls().test_data()

    def setUp(self):
        """
        Repetitive code (run before each test).
        """
        # clear the output_buffer to prepare it for storing a new value
        TestHBNBCommand.output_buffer.seek(0)
        TestHBNBCommand.output_buffer.truncate()

    # --------------- Test help, help <topic> and its errors --------------- #

    def test_help(self):
        """
        Tests that the help command helps users to know all available commands
        in the HBNBCommand CLI.
        """
        result = self.exec_cm("help").split("\n")
        expect = ["Documented commands (type help <topic>):",
                  "========================================"]

        self.assertTrue(len(result) == 6)

        for cmd in self.cmds:
            found_cm = (cmd in result[3])
            if not found_cm:
                break

        self.assertEqual(result[1:3], expect)
        self.assertTrue(found_cm)

    def test_help_cmd(self):
        """
        Tests that the help <command> gives users a brief documentation to
        help them understand what the <command> do.
        """
        for cmd in self.cmds:
            result = self.exec_cm(f"help {cmd}")
            self.assertTrue(len(result) > 25)

    def test_help_errors(self):
        """
        Tests help command errors.
        """
        result = self.exec_cm(f"help test")
        expect = "*** No help on test\n"

        self.assertEqual(result, expect)

    # ----------------- Test output of valid commands ------------ #

    def test_do_all(self):
        """
        Tests that all command returns all objects in the data source
        depend on class or not.
        """
        # test `all` with no args
        result = self.exec_cm("all")
        expect = self.filter_with_cls(None)

        print(expect)
        expect = self.output_buffer.getvalue()

        self.assertEqual(result, expect)

        # test `all` with class name as argument
        for cls in storage.classes:
            result = self.exec_cm(f"all {cls}")
            expect = self.filter_with_cls(cls)

            self.setUp()
            print(expect)
            expect = self.output_buffer.getvalue()

            self.assertEqual(expect, result)

    def test_do_count(self):
        """
        Tests that count command give the user the right number of instances
        of a specific class.
        """
        for cls in storage.classes:
            result = self.exec_cm(f"count {cls}").replace("\n", "")
            expect = self.filter_with_cls(cls)

            self.assertEqual(result, str(len(expect)))

    def test_do_create(self):
        """
        Tests that create command creates a new object in the data source.
        """
        for cls in storage.classes:
            obj_id = self.exec_cm(f"create {cls}").replace("\n", "")
            obj_key = f"{cls}.{obj_id}"
            self.assertIn(obj_key, storage.all())

    def test_do_destroy(self):
        """
        Tests that destroy cmd deletes a specific object from the data source.
        """
        primary_keys = list(storage.all().keys())
        for key in primary_keys:
            cls_name, obj_id = key.split(".")
            self.exec_cm(f"destroy {cls_name} {obj_id}")
            self.assertNotIn(key, storage.all())
        self.test_data()

    def test_do_EOF(self):
        """
        Tests that the HBNBCommand handles the EOF condition.
        """
        result = self.exec_cm("EOF")
        self.assertEqual(result, "")

    def test_do_quit(self):
        """
        Tests that HBNBCommand exits the CLI when quit command is requested.
        """
        result = self.exec_cm("quit")
        self.assertEqual(result, "")

    def test_do_show(self):
        """
        Tests that show command displays the requested object.
        """
        for key, obj in storage.all().items():
            cls, obj_id = key.split(".")
            result = self.exec_cm(f"show {cls} {obj_id}")
            print(obj)
            expect = self.output_buffer.getvalue()
            self.assertEqual(result, expect)
            self.setUp()

    def test_do_update(self):
        """
        Tests that update command updates requested object successfully.
        """
        for key, obj in storage.all().items():
            cls, obj_id = key.split(".")
            self.exec_cm(f"update {cls} {obj_id} first_name 'Mohammed'")
            self.exec_cm(f"update {cls} {obj_id} last_name 'Mustafa'")
            self.exec_cm(f"update {cls} {obj_id} Age 21")
            self.exec_cm(f"update {cls} {obj_id} Salary 2000.20")

            self.assertEqual(obj.first_name, "Mohammed")
            self.assertEqual(obj.last_name, "Mustafa")
            self.assertEqual(obj.Age, 21)
            self.assertEqual(obj.Salary, 2000.20)

    def test_emptyline(self):
        """
        Tests that HBNBComannd emptylines.
        """
        result = self.exec_cm("\n")

        self.assertEqual(result, "")

    def test_precmd(self):
        """
        Tests that the precmd in HBNBCommand parse input that follows a spcefic
        pattern and pass it to onecmd method to execute it.
        """
        for cls in storage.classes:
            obj_id = self.exec_cm(f"create {cls}").replace("\n", "")
            obj_key = f"{cls}.{obj_id}"

            # test <class_name>.all() pattern
            result = self.exec_cm(HBNBCommand().precmd(f"{cls}.all()"))
            expect = self.exec_cm(f"all {cls}")

            self.assertEqual(result, expect)

            # test <class_name>.show(<id>)
            query = f"{cls}.show('{obj_id}')"
            result = self.exec_cm(HBNBCommand().precmd(query))
            expect = self.exec_cm(f"show {cls} {obj_id}")

            self.assertEqual(result, expect)

            # test <class_name>.update(<id>)
            query = f"{cls}.update('{obj_id}', 'first', 'Mohammed')"
            self.exec_cm(HBNBCommand().precmd(query))

            query = f"{cls}.update('{obj_id}', 'last', 'Mustafa')"
            self.exec_cm(HBNBCommand().precmd(query))

            query = f"{cls}.update('{obj_id}', 'age', 21)"
            self.exec_cm(HBNBCommand().precmd(query))

            query = f"{cls}.update('{obj_id}', 'salary', 2000.20)"
            self.exec_cm(HBNBCommand().precmd(query))

            obj = storage.all().get(obj_key)
            self.assertEqual(obj.first, "Mohammed")
            self.assertEqual(obj.last, "Mustafa")
            self.assertEqual(obj.age, 21)
            self.assertEqual(obj.salary, 2000.20)

            # test <class_name>.count()
            result = self.exec_cm(HBNBCommand().precmd(f"{cls}.count()"))
            expect = self.exec_cm(f"count {cls}")

            self.assertEqual(result, expect)

            # test <class_name>.destroy(<id>)
            self.exec_cm(HBNBCommand().precmd(f"{cls}.destory('{obj_id}')"))
            is_deleted = storage.all().get(obj_key, True)

            self.assertTrue(is_deleted)

    # -------------- Test output of invalid Commands ------------- #

    def test_do_all_errors(self):
        """
        Tests `all` command errors.
        """
        result = self.exec_cm(f"all asdjlf")
        expect = "** class doesn't exist **\n"

        self.assertEqual(result, expect)

    def test_do_count_errors(self):
        """
        Tests `count` command errors.
        """
        result = self.exec_cm("count asjdflk")
        expect = "0\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("count")
        expect = "** class name missing **\n"

        self.assertEqual(result, expect)

    def test_do_create_errors(self):
        """
        Tests `create` command errors.
        """
        result = self.exec_cm("create asjdflk")
        expect = "** class doesn't exist **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("create")
        expect = "** class name missing **\n"

        self.assertEqual(result, expect)

    def test_do_destroy_errors(self):
        """
        Tests `destroy` command errors.
        """
        result = self.exec_cm("create asjdflk")
        expect = "** class doesn't exist **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("create")
        expect = "** class name missing **\n"

        self.assertEqual(result, expect)

    def test_do_show_errors(self):
        """
        Tests `show` command errors.
        """
        result = self.exec_cm("show")
        expect = "** class name missing **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("show sadf32k")
        expect = "** class doesn't exist **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("show BaseModel")
        expect = "** instance id missing **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("show BaseModel 239h8hjad")
        expect = "** no instance found **\n"

        self.assertEqual(result, expect)

    def test_do_update_errors(self):
        """
        Tests `update` command errors.
        """
        result = self.exec_cm("update")
        expect = "** class name missing **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("update sadf32k")
        expect = "** class doesn't exist **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("update BaseModel")
        expect = "** instance id missing **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm("update BaseModel 239h8hjad")
        expect = "** no instance found **\n"

        self.assertEqual(result, expect)

        obj_id = list(storage.all().keys())[0].split(".")[1]
        result = self.exec_cm(f"update BaseModel {obj_id}")
        expect = "** attribute name missing **\n"

        self.assertEqual(result, expect)

        result = self.exec_cm(f"update BaseModel {obj_id} test")
        expect = "** value missing **\n"

        self.assertEqual(result, expect)

    def test_invalid_syntax(self):
        """
        Tests invalid syntax error.
        """
        result = self.exec_cm("test")
        expect = "*** Unknown syntax: test\n"

        self.assertEqual(result, expect)

    # -------------- Helper Functions ----------- #

    def test_data(self):
        """
        Creates 10 objects of each class in the data source.
        """
        for cls in storage.classes:
            for i in range(3):
                self.exec_cm(f"create {cls}")

    @staticmethod
    def exec_cm(line):
        """
        Pass a line of string to the HBNBCommand CLI to execute it.

        Parameters:
        -----------
            - line (string): a line of string what you to execute.

        Returns: the result of HBNBCommand of execution the <line>
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(line)

        return f.getvalue()

    @staticmethod
    def filter_with_cls(cls_name):
        """
        Filter the given objects data depend on a class.
        if None is the cls_name will return all data

        Parameters:
        -----------
            cls (string): the class name

        Returns: a list of string representations of the filtered objects
        """
        filtered_data = []
        for key, obj in storage.all().items():
            if key.split(".")[0] == cls_name or not cls_name:
                filtered_data.append(str(obj))
        return filtered_data


if __name__ == "__main__":
    unittest.main()
