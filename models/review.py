#!/usr/bin/python3
"""The review Module."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
        Class that define a new Airbnb review.

        Public class attributes:
            - place_id (string): empty string
            - user_id (string): empty string
            - text (string): empty string
    """
    place_id = ""
    user_id = ""
    text = ""

    def __init__(self, *arg, **kwarg):
        super().__init__(**kwarg)
