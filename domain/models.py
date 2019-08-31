from enum import Enum
from typing import List, Union


class Location(object):
    """
    Represents a point
    """

    def __init__(self, x_coordinate: int, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

    @property
    def coordinates(self):
        return self.x, self.y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: 'Location'):
        return (self.x == other.x) and (self.y == other.y)


class MapLocation(Location):
    """
    Represents a point which can contain vehicles and people
    """

    def __init__(self, x, y):
        Location.__init__(self, x, y)
        self.people: List[Person] = []
        self.vehicles: List[Vehicle] = []


class PersonStatus(str, Enum):
    REQUESTED_VEHICLE = 'requested vehicle'
    IN_VEHICLE = 'in vehicle'
    INACTIVE = 'inactive'


class Person:
    """
    A user of the vehicle
    """
    def __init__(self, name: str, pickup: Location, dropoff: Location, status: PersonStatus):
        self.name = name
        self.pickup = pickup
        self.dropoff = dropoff
        self.status = status

    def __repr__(self):
        return f'{self.name} - status {self.status} | pickup: {self.pickup}, dropoff: {self.dropoff}'

    def __str__(self):
        return f'{self.name} - status {self.status} | pickup: {self.pickup}, dropoff: {self.dropoff}'


class Vehicle(object):
    """
    Represents a vehicle
    """
    def __init__(self, name: str, max_occupancy: Union[None, int]):
        self.name = name
        self.max_occupancy = max_occupancy
        self.passengers: List[Person] = []

    def add_passenger(self, passenger: Person):
        if self.max_occupancy:
            assert len(self.passengers) + 1 <= self.max_occupancy
        self.passengers.append(passenger)

    def waypoints(self):



class LocationsMap(object):
    """
    A map that contains all the locations people and vehicles can exist
    """
    def __init__(self, name: str):
        self.name = name
        self.nodes: Union[List[Location], None] = None

    def init_grid_network(self, x_nodes: int, y_nodes: int):
        self.nodes = [MapLocation(x, y) for x in range(x_nodes) for y in range(y_nodes)]

    def get_vehicle_itinerary(self, waypoints: List[Location]):
        pass


