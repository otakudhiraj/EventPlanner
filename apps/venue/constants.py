from enum import Enum


class FoodType(Enum):
    VEG="Vegetarian"
    NON_VEG="Non-Vegetarian"

    @classmethod
    def choices(cls):
        return [(member.value, member.name) for member in cls]