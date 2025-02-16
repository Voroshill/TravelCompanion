from enum import Enum


class Category(str, Enum):
    restaurant = "restaurant"
    cafe = "cafe"
    store = "store"
    bar = "bar"
