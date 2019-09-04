from enum import Enum
from typing import List, Union, Dict, Set


class Location(object):
    """
    Represents a point
    """

    def __init__(self, x_coordinate: int, y_coordinate: int):
        self.x: int = x_coordinate
        self.y: int = y_coordinate

    @property
    def coordinates(self):
        return self.x, self.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x},{self.y})'

    def __eq__(self, other: 'Location'):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))


class PersonStatus(str, Enum):
    REQUESTED_VEHICLE = 'requested vehicle'
    IN_VEHICLE = 'in vehicle'
    INACTIVE = 'inactive'


class Person:
    """
    A user of the vehicle
    """
    def __init__(self, name: str, pickup: Location, dropoff: Location, status: PersonStatus):
        self.name: str = name
        self.pickup: Location = pickup
        self.dropoff: Location = dropoff
        self.status: PersonStatus = status

    def __repr__(self):
        return f'{self.name} - status {self.status} | pickup: {self.pickup}, dropoff: {self.dropoff}'

    def __str__(self):
        return f'{self.name} - status {self.status} | pickup: {self.pickup}, dropoff: {self.dropoff}'

    def __eq__(self, other: 'Person'):
        return self.__dict__ == other.__dict__


class Vehicle(object):
    """
    Represents a vehicle
    """
    def __init__(self, name: str, max_occupancy: Union[None, int], location: Location):
        self.name = name
        self.max_occupancy = max_occupancy
        self.location: Location = location
        self.passengers: List[str] = []
        self.itinerary: List[Location] = []
        self.itinerary_step: int = 0
        self.destinations_queue: List[Location] = []

    def __eq__(self, other: 'Vehicle'):
        return self.__dict__ == other.__dict__


class LocationsMap(object):
    """
    A map that contains all the locations people and vehicles can exist
    """
    def __init__(self):
        self.people: List[Dict[str, Location]] = []
        self.vehicles: List[Dict[str, Location]] = []

    def __eq__(self, other: 'LocationsMap'):
        return self.__dict__ == other.__dict__
