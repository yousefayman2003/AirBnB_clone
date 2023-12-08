#!/usr/bin/python3
"""
The Amenity Module.
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Class that defines a new Airbnb amenity.

    Public class attributes:
        - name (string): empty string
    """

    name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
