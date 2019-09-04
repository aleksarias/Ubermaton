from copy import copy
from typing import List, Union

from domain.models import Person, Vehicle, Location, PersonStatus
from domain.repositories import PeopleRepository, VehicleRepository, LocationMapRepository


class InMemPeopleRepository(PeopleRepository):

    def __init__(self):
        self.db: List[Person] = []

    def add(self, person: Person) -> None:
        self.db.append(person)

    def remove(self, name: str) -> None:
        self.db = [item for item in self.db if item.name != name]

    def update(self, person: Person):
        for i, item in enumerate(self.db):
            if item.name == person.name:
                self.db[i] = person

    def get(self, name: str) -> Person:
        for item in self.db:
            if item.name == name:
                return copy(item)

    def get_all(self) -> List[Person]:
        return copy(self.db)

    def get_by_dropoff(self, location: Location, status: PersonStatus) -> List[Person]:
        return [p for p in self.db if (p.dropoff == location and p.status == status)]

    def get_by_pickup(self, location: Location, status: PersonStatus) -> List[Person]:
        return [p for p in self.db if (p.pickup == location and p.status == status)]


class InMemVehicleRepository(VehicleRepository):

    def __init__(self):
        self.db: List[Vehicle] = []

    def add(self, vehicle: Vehicle) -> None:
        self.db.append(vehicle)

    def remove(self, name: str) -> None:
        self.db = [item for item in self.db if item.name != name]

    def update(self, vehicle: Vehicle):
        for i, item in enumerate(self.db):
            if item.name == vehicle.name:
                self.db[i] = vehicle

    def get(self, name: str) -> Vehicle:
        for item in self.db:
            if item.name == name:
                return copy(item)

    def get_all(self) -> List[Vehicle]:
        return copy(self.db)


class InMemLocationMapRepository(LocationMapRepository):

    def __init__(self):
        self.db: List[Union[Vehicle, Person]] = []

    def add(self, entity: Union[Vehicle, Person]) -> None:
        self.db.append(entity)

    def remove(self, name: str) -> None:
        self.db = [item for item in self.db if item.name != name]

    def update(self, entity: Union[Vehicle, Person]):
        for i, item in enumerate(self.db):
            if item.name == entity.name:
                self.db[i] = entity

    def get(self, name: str) -> Union[Vehicle, Person]:
        for item in self.db:
            if item.name == name:
                return copy(item)

    def get_all(self) -> List[Union[Vehicle, Person]]:
        return copy(self.db)
