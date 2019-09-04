from networkx.generators import lattice

from domain.models import Person, PersonStatus, Location
from domain.services import PeopleService, VehicleService, LocationMapService
from infrastructure.gateways import NetworkXGateway
from infrastructure.persistence import InMemPeopleRepository, InMemVehicleRepository, InMemLocationMapRepository
from usecases.process_time_steps import time_step_single_vehicle


people_service = PeopleService(InMemPeopleRepository())
vehicle_service = VehicleService(InMemVehicleRepository())
map_service = LocationMapService(InMemLocationMapRepository(), NetworkXGateway(lattice.grid_2d_graph(10, 10)))


def test_ten_time_steps():
    time_steps = [
        [
            {"name": "Elon", "start": [2, 2], "end": [8, 7]},
            {"name": "George", "start": [1, 2], "end": [4, 3]}
        ],
        [],
        [
            {"name": "Nancy", "start": [9, 9],  "end": [1, 3]}
        ],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    for step in time_steps:
        request = [
            Person(
                item['name'],
                Location(item['start'][0], item['start'][1]),
                Location(item['end'][0], item['end'][1]),
                PersonStatus.REQUESTED_VEHICLE)
            for item in step
        ]
        vehicle_location, passengers, dropped_off, picked_up = time_step_single_vehicle(
            request,
            people_service,
            vehicle_service,
            map_service
        )

        message = f'Vehicle is at {vehicle_location} with passengers {", ".join(passengers)} | '
        if dropped_off:
            message += f'Dropped off {", ".join(p.name for p in dropped_off)} '
        if picked_up:
            message += f'Picked up {", ".join(p.name for p in picked_up)} '
        print(message)


if __name__ == '__main__':
    test_ten_time_steps()
