from abc import ABC, abstractmethod
from typing import List

from domain.models import Vehicle, Person, LocationsMap, Location, PersonStatus


class PeopleRepository(ABC):
    """
    Stores people that use the vehicle service
    """
    @abstractmethod
    def add(self, vehicle: Person) -> None:
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        pass

    @abstractmethod
    def update(self, person: Person) -> Person:
        pass

    @abstractmethod
    def get(self, name: str) -> Person:
        pass

    @abstractmethod
    def get_all(self) -> List[Person]:
        pass

    @abstractmethod
    def get_by_dropoff(self, location: Location, status: PersonStatus) -> List[Person]:
        pass

    @abstractmethod
    def get_by_pickup(self, location: Location, status: PersonStatus) -> List[Person]:
        pass


class VehicleRepository(ABC):
    """
    Stores the vehicles for the vehicle service
    """

    @abstractmethod
    def add(self, vehicle: Vehicle) -> None:
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        pass

    @abstractmethod
    def update(self, vehicle: Vehicle) -> Vehicle:
        pass

    @abstractmethod
    def get(self, name: str) -> Vehicle:
        pass

    @abstractmethod
    def get_all(self) -> List[Vehicle]:
        pass


class LocationMapRepository(ABC):
    """
    Stores the location maps where the vehicle and people can exist
    """

    @abstractmethod
    def add(self, location_map: LocationsMap) -> None:
        pass

    @abstractmethod
    def remove(self, name: str) -> None:
        pass

    @abstractmethod
    def update(self, location_map: LocationsMap) -> LocationsMap:
        pass

    @abstractmethod
    def get(self, name: str) -> LocationsMap:
        pass

    @abstractmethod
    def get_all(self) -> List[LocationsMap]:
        pass
