from typing import Union, List

from domain.models import Person, PersonStatus, Location
from domain.services import VehicleService, PeopleService, LocationMapService

DEFAULT_VEHICLE = 'default'


def time_step_single_vehicle(
        request: Union[List[Person], None],
        people_service: PeopleService,
        vehicle_service: VehicleService,
        map_service: LocationMapService
):
    """

    :param request:
    :param people_service:
    :param vehicle_service:
    :param map_service:
    :return:
    """

    vehicle_location, arrived_at_destination, vehicle_destinations = vehicle_service.ping(DEFAULT_VEHICLE)
    dropped_off = None
    picked_up = None
    if arrived_at_destination:
        dropped_off = people_service.get_by_dropoff_location(vehicle_location)
        for person in dropped_off:
            vehicle_service.remove_passenger(DEFAULT_VEHICLE, person.name)
            person.status = PersonStatus.INACTIVE
            people_service.update(person)
        picked_up = people_service.get_by_pickup_location(vehicle_location)
        for person in picked_up:
            vehicle_service.add_passenger(DEFAULT_VEHICLE, person.name)
            vehicle_service.add_destination(DEFAULT_VEHICLE, person.dropoff)
            person.status = PersonStatus.IN_VEHICLE
            people_service.update(person)
        vehicle_service.remove_destination(DEFAULT_VEHICLE, vehicle_location)

    if request:
        for person in request:
            # TODO: Move domain model state change to methods in domain model
            person.status = PersonStatus.REQUESTED_VEHICLE
            people_service.update_or_add(person)
            # If there were multiple vehicles, call map service to get closest vehicle to person
            vehicle_service.add_destination(DEFAULT_VEHICLE, person.pickup)

    if arrived_at_destination or request:
        # Since vehicle occupancy is infinite, get closest pick up or drop off to vehicle without concern for occupancy
        vehicle_destinations = vehicle_service.get_destinations(DEFAULT_VEHICLE)
        if vehicle_destinations:
            path_to_next_stop = map_service.get_itinerary(vehicle_location, vehicle_destinations)
            vehicle_service.update_itinerary(DEFAULT_VEHICLE, path_to_next_stop)

    return (
        vehicle_location, vehicle_service.get_passengers(DEFAULT_VEHICLE), dropped_off, picked_up, vehicle_destinations
    )
