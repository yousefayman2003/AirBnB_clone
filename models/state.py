#!/usr/bin/python3
"""The State Module."""
from models.base_model import BaseModel


class State(BaseModel):
    """
        Class that define a new Airbnb State.

        Public class attributes:
            - name (string): empty string
    """

    name = ""

    def __init__(self, *arg, **kwarg):
        super().__init__(**kwarg)
