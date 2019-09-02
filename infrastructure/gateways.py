from typing import List, Union, Tuple, Dict

import googlemaps

from domain.gateways import DirectionsGateway
from domain.models import Location


class NetworkXGateway(DirectionsGateway):

    def get_itinerary(self, origin, destinations):
        raise NotImplemented("Method hasn't been implemented")


class GoogleDirectionsGateway(DirectionsGateway):
    """
    https://developers.google.com/maps/documentation/
    """
    def __init__(self, api_key: str):
        """
        To get an API get from google:
        https://cloud.google.com/docs/authentication/api-keys#creating_an_api_key
        Make sure to enable products: Directions API, Distance Matrix API, and Geocoding API
        :param api_key:
        """
        self.client = googlemaps.Client(key=api_key)

    def _geocode(self, request):
        # TODO: create request and response schema for api
        raise NotImplemented

    def _distance_matrix(self, request):
        # TODO: create request and response schema for api
        raise NotImplemented

    def get_address_location(self, address: str) -> Location:
        """

        :param address:
        :return:
        """
        result: dict = self.client.geocode(address)
        x, y = result[0]['geometry']['location'].values()
        return Location(x, y)

    def get_distance_matrix(self, origin: Union[Location, str], destinations: Union[List[Location], List[str]]):
        """
        Accepts an origin and a list of destinations and returns a list that contains the distance to each destination
        from the origin
        :param origin:
        :param destinations:
        :return:
        """
        # Make sure origin and destinations are of type Location
        origin = self.get_address_location(origin) if isinstance(origin, str) else origin
        destinations: List[Location] = [
            self.get_address_location(d) if isinstance(d, str) else d for d in destinations
        ]
        destinations: List[Tuple[str]] = self._convert_locations_to_coordinates(destinations)
        result = self.client.distance_matrix(origin.coordinates, destinations)
        destinations: List[Dict[tuple, dict]] = [
            {destination: cost['rows']['elements']} for destination, cost in zip(destinations, result)
        ]
        return destinations

    def get_itinerary(self, origin: Location, destinations: List[Location]):
        """
        Accepts an origin and a list of destinations and returns an itinerary (route) that's optimized so that each
        destination can be reached in the least amount of time
        :param origin:
        :param destinations:
        :return:
        """
        # TODO: Add logic

    @staticmethod
    def _convert_locations_to_coordinates(locations: List[Location]) -> List[tuple]:
        """
        Converts Location type to a coordinate tuple, (x,y)
        :param locations:
        :return:
        """
        return [l.coordinates for l in locations]