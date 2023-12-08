#!/usr/bin/python3
"""
The Review Module.
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Class that defines a new Airbnb review.

    Public class attributes:
        - place_id (string): empty string
        - user_id (string): empty string
        - text (string): empty string
    """

    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
