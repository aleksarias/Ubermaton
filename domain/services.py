from domain.gateways import DirectionsGateway
from domain.repositories import VehicleRepository, LocationMapRepository, PeopleRepository


class PersonService(object):

    def __init__(self, repo: PeopleRepository):
        pass


class VehicleService(object):

    def __init__(self, repo: VehicleRepository):
        pass


class LocationMapService(object):

    def __init__(self, repo: LocationMapRepository, directions: DirectionsGateway):
        pass
