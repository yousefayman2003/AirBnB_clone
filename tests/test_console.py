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

    TestCases of TestHBNBCommand:
        - test_help(self)
        - test_help_cm(self)

        - do_all(self, arg)
        - do_count(self, arg)
        - do_create(self, arg)
        - do_destroy(self, arg)
        - do_EOF(self, arg)
        - do_quit(self, arg)
        - do_show(self, arg)
        - do_update(self, arg)

        - emptyline(self)
        - precmd(self, arg)

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

    # ----------------- Test help and help <topic> ------------ #

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
        self.assertEqual(result, "\n")

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

    # def test_precmd(self):

    # -------------- Test output of invalid Commands ------------- #

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
