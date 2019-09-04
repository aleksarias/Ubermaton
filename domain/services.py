from typing import List, Set

from domain.gateways import DirectionsGateway
from domain.models import Person, Vehicle, Location, PersonStatus
from domain.repositories import VehicleRepository, LocationMapRepository, PeopleRepository


class PeopleService(object):

    def __init__(self, repo: PeopleRepository):
        self._repo = repo

    def add(self, person: Person):
        self._repo.add(person)

    def update(self, person: Person):
        self._repo.update(person)

    def remove(self, name: str):
        self._repo.remove(name)

    def get(self, name: str) -> Person:
        return self._repo.get(name)

    def get_all(self) -> List[Person]:
        return self._repo.get_all()

    def update_or_add(self, person: Person):
        if person not in self._repo.get_all():
            self._repo.add(person)
        else:
            self._repo.update(person)

    def get_by_dropoff_location(self, location: Location) -> List[Person]:
        return self._repo.get_by_dropoff(location, PersonStatus.IN_VEHICLE)

    def get_by_pickup_location(self, location: Location) -> List[Person]:
        return self._repo.get_by_pickup(location, PersonStatus.REQUESTED_VEHICLE)


class VehicleService(object):

    def __init__(self, repo: VehicleRepository):
        self._repo = repo
        if len(self._repo.get_all()) == 0:
            self._repo.add(Vehicle('default', None, Location(0, 0)))

    def add(self, vehicle: Vehicle):
        self._repo.add(vehicle)

    def update(self, vehicle: Vehicle):
        self._repo.update(vehicle)

    def remove(self, name: str):
        self._repo.remove(name)

    def get(self, name: str) -> Vehicle:
        return self._repo.get(name)

    def get_all(self) -> List[Vehicle]:
        return self._repo.get_all()

    def add_passenger(self, name: str, passenger_name: str):
        vehicle = self.get(name)
        if vehicle.max_occupancy:
            assert len(vehicle.passengers) + 1 <= vehicle.max_occupancy
        vehicle.passengers.append(passenger_name)

    def get_passengers(self, name):
        vehicle = self.get(name)
        return vehicle.passengers

    def remove_passenger(self, name: str, passenger_name: str):
        vehicle = self.get(name)
        vehicle.passengers.remove(passenger_name)

    def update_location(self, name: str, location: Location):
        vehicle = self.get(name)
        vehicle.location = location
        self.update(vehicle)

    def add_destination(self, name, destination: Location):
        vehicle = self.get(name)
        if destination not in vehicle.destinations_queue:
            assert isinstance(destination, Location)
            vehicle.destinations_queue.append(destination)
        self.update(vehicle)

    def remove_destination(self, name, destination: Location):
        vehicle = self.get(name)
        vehicle.destinations_queue.remove(destination)
        self.update(vehicle)

    def get_destinations(self, name: str) -> List[Location]:
        vehicle = self.get(name)
        return vehicle.destinations_queue

    def get_vehicle_location(self, name: str) -> Location:
        vehicle = self.get(name)
        return vehicle.location

    def update_itinerary(self, name: str, itinerary: List[Location]):
        for stop in itinerary:
            assert isinstance(stop, Location)
        vehicle = self.get(name)
        vehicle.itinerary = itinerary
        vehicle.itinerary_step = 1
        self.update(vehicle)

    def ping(self, name: str) -> (Location, bool):
        vehicle = self.get(name)
        arrived_at_destination = False
        if vehicle.itinerary:
            vehicle.location = vehicle.itinerary[vehicle.itinerary_step]
            if vehicle.itinerary[-1] == vehicle.location:
                vehicle.itinerary = []
                arrived_at_destination = True
            vehicle.itinerary_step += 1
            self.update(vehicle)
        return vehicle.location, arrived_at_destination, vehicle.destinations_queue


class LocationMapService(object):

    def __init__(self, repo: LocationMapRepository, directions: DirectionsGateway):
        # TODO: Leverage LocationMap repo for some caching, perhaps
        self._repo = repo
        self._directions = directions

    def get_closest(self, origin: Location, destination: List[Location]):
        """
        Utility for getting closest destination or ie, closest car to a person
        :param origin:
        :param destination:
        :return:
        """
        # TODO:

    def get_itinerary(self, origin: Location, destinations: List[Location]) -> List[Location]:
        next_destination = self._directions.get_next_destination(origin, destinations)
        shortest_path_to_next_destination = self._directions.shortest_path_to_destination(origin, next_destination)
        return shortest_path_to_next_destination
