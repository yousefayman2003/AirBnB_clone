"""The `Console` Module that Defines HBNB command interpeter."""
import cmd


class HBNBCommand(cmd.Cmd):
    """
        Defines HBNB command interpreter.

        Public Class Attributes:
            prompt (str): command prompt.
    """

    # make a custom prompt
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """quit command to exit from the program"""
        return True

    def do_EOF(self, arg):
        """EOF detected to exit from the program"""
        return True

    def emptyline(self):
        """does nothing if empty line."""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
