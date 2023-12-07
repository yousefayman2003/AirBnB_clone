#!/usr/bin/python3
"""The User Module.

    A simple module, since it has only one class called (User).
"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class that define a new Airbnb user.

        Public class attributes:
            - email (string): empty string
            - password (string: empty string
            - first_name (string): empty string
            - last_name (string): empty string
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *arg, **kwarg):
        super().__init__(**kwarg)
