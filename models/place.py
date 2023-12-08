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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city_id = ""
        self.user_id = ""
        self.name = ""
        self.description = ""
        self.number_rooms = 0
        self.number_bathrooms = 0
        self.max_guest = 0
        self.price_by_night = 0
        self.latitude = 0.0
        self.longitude = 0.0
        self.amenity_ids = []
