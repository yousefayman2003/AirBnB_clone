#!/usr/bin/python3
"""The Amenity Module."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
        Class that define a new Airbnb amenity.

        Public class attributes:
            - name (string): empty string
    """
    name = ""

    def __init__(self, *arg, **kwarg):
        super().__init__(**kwarg)
