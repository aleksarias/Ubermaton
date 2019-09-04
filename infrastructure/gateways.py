from typing import List, Union, Tuple, Dict, Set

import googlemaps
import networkx as nx
from networkx.algorithms import shortest_paths

from domain.gateways import DirectionsGateway
from domain.models import Location


class NetworkXGateway(DirectionsGateway):

    def __init__(self, graph: nx.Graph):
        """
        Uses the networkx package to create a graph on which to a network for which directions and travel times can be
        generated. For a list of functions that generate commonly useful graphs please see:
        https://networkx.github.io/documentation/stable/reference/generators.html

        :param graph:
        """
        assert graph.number_of_nodes() > 0, "Graph cannot empty"
        self._graph = graph
        print('Graph initialized')

    def validate_location(self, location: Location):
        assert location.coordinates in self._graph.nodes

    def get_next_destination(self, origin: Location, destinations: List[Location]) -> Location:
        assert isinstance(origin, Location)
        for d in destinations:
            assert isinstance(d, Location)
        destination_lengths = [
            shortest_paths.shortest_path_length(self._graph, origin.coordinates, d.coordinates) for d in destinations
        ]
        closest_destination = destinations[destination_lengths.index(min(destination_lengths))]
        return closest_destination

    def shortest_path_to_destination(self, origin: Location, destination: Location) -> List[Location]:
        path: List[Tuple[int]] = shortest_paths.shortest_path(self._graph, origin.coordinates, destination.coordinates)
        return [Location(node[0], node[1]) for node in path]


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
        self._client = googlemaps.Client(key=api_key)

    def _geocode(self, request):
        # TODO: create request and response schema for api
        raise NotImplemented

    def _distance_matrix(self, request):
        # TODO: create request and response schema for api
        raise NotImplemented

    def get_address_location(self, address: str) -> Location:
        """
        Convenience method for converting an address to a Location type

        :param address:
        :return:
        """
        result: dict = self._client.geocode(address)
        x, y = result[0]['geometry']['location'].values()
        return Location(x, y)

    def _get_distance_matrix(self, origin: Location, destinations: List[Location]) -> List[dict]:
        """
        Accepts an origin and a list of destinations and returns a list that contains the distance to each destination
        from the origin

        :param origin:
        :param destinations:
        :return:
        """
        destinations: List[Tuple[str]] = self._convert_locations_to_coordinates(destinations)
        result = self._client.distance_matrix(origin.coordinates, destinations)
        destinations: List[dict] = [
            {**cost, 'location': destination} for destination, cost in zip(destinations, result['rows'][0]['elements'])
        ]
        return destinations

    @staticmethod
    def _convert_locations_to_coordinates(locations: List[Location]) -> List[tuple]:
        """
        Converts Location type to a coordinate tuple, (x,y)

        :param locations:
        :return:
        """
        return [l.coordinates for l in locations]

    def get_next_destination(self, origin: Location, destinations: List[Location]) -> Location:
        """
        Accepts an origin and a list of destinations and returns an itinerary (route) that's optimized so that each
        destination can be reached in the least amount of time

        :param origin:
        :param destinations:
        :return:
        """
        # Make sure origin and destinations are of type Location (just in case)
        origin = self.get_address_location(origin) if isinstance(origin, str) else origin
        destinations: List[Location] = [
            self.get_address_location(d) if isinstance(d, str) else d for d in destinations
        ]
        path_costs = self._get_distance_matrix(origin, destinations)
        next_destination = destinations[
            path_costs.index(min(path_costs, key=lambda x: x['distance']['value']))
        ]
        return next_destination

    def shortest_path_to_destination(self, origin: Location, destination: Location) -> List[Location]:
        raise NotImplemented
