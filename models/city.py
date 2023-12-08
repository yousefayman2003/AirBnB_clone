#!/usr/bin/python3
"""
The City Module.
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Class that defines a new Airbnb city.

    Public class attributes:
        - state_id (string): empty string
        - name (string): empty string
    """

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
