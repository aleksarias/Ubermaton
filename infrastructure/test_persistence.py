from domain.models import Person, Location, PersonStatus
from infrastructure.persistence import InMemPeopleRepository, InMemVehicleRepository, InMemLocationMapRepository

people_repo = InMemPeopleRepository()
vehicle_repo = InMemVehicleRepository()
map_repo = InMemLocationMapRepository()

me = Person(name='Alex Arias', pickup=Location(1, 0), dropoff=Location(4, 5), status=PersonStatus.REQUESTED_VEHICLE)


def test_inmem_add_person():
    people_repo.add(me)


def test_inmem_get_person():
    repo_me = people_repo.get('Alex Arias')
    assert repo_me == me


def test_in_assertion():
    assert me in people_repo.get_all()


def test_inmem_remove_person():
    people_repo.remove('Alex Arias')
    assert me not in people_repo.get_all()


def test_inmem_add_vehicle():
    pass


def test_inmem_remove_vehicle():
    pass


def test_inmem_get_vehicle():
    pass
