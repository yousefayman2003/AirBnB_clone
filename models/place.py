#!/usr/bin/python3
"""
The Place Module.
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    Class that defines a new Airbnb place.

    Public class attributes:
        - city_id (string): empty string
        - user_id (string): empty string
        - name (string): empty string
        - description (string): empty string
        - number_rooms (int): 0
        - number_bathrooms (int): 0
        - max_guest (int): 0
        - price_by_night (int): 0
        - latitude (float): 0.0
        - longitude (float): 0.0
        - amenity_ids (list[str]): empty list
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
