import pickle
import os

from networkx.generators import lattice

import config
from domain.models import Location
from infrastructure.gateways import GoogleDirectionsGateway, NetworkXGateway


# TODO: stub internet dependent responses


def test_google_directions_gateway_geocoding():
    gateway = GoogleDirectionsGateway(api_key=config.GOOGLE_API_KEY)
    response = gateway.get_address_location('5502 Broken Sound Blvd NW Boca Raton, FL 33487')
    if os.getenv('GEN_GOLDEN_FILES'):
        with open('infrastructure/fixtures/google_directions_gateway_geocoding.pkl', 'wb') as fh:
            pickle.dump(response, fh)
    with open('infrastructure/fixtures/google_directions_gateway_geocoding.pkl', 'rb') as fh:
        golden = pickle.load(fh)
    assert response == golden


def test_google_directions_gateway_distance_matrix():
    gateway = GoogleDirectionsGateway(api_key=config.GOOGLE_API_KEY)
    origin = gateway.get_address_location('5502 Broken Sound Blvd NW Boca Raton, FL')
    destinations = [
        gateway.get_address_location(d) for d in [
            '7841 NW 170th St. Hialeah, FL 33015',
            '1182 NW 162nd Ave. Pembroke Pines, FL 33028',
            '9742 Rennes Lane Delray Beach, FL 33446', ]
    ]
    response = gateway._get_distance_matrix(origin, destinations)
    if os.getenv('GEN_GOLDEN_FILES'):
        with open('infrastructure/fixtures/google_directions_gateway_distance_matrix.pkl', 'wb') as fh:
            pickle.dump(response, fh)
    with open('infrastructure/fixtures/google_directions_gateway_distance_matrix.pkl', 'rb') as fh:
        golden = pickle.load(fh)
    assert response == golden


def test_google_directions_gateway_next_destination():
    gateway = GoogleDirectionsGateway(api_key=config.GOOGLE_API_KEY)
    origin_address = '5502 Broken Sound Blvd NW Boca Raton, FL'
    origin = gateway.get_address_location(origin_address)
    destination_addresses = [
            '7841 NW 170th St. Hialeah, FL 33015',
            '1182 NW 162nd Ave. Pembroke Pines, FL 33028',
            '9742 Rennes Lane Delray Beach, FL 33446',
        ]
    destinations = [gateway.get_address_location(d) for d in destination_addresses]
    next_destination = gateway.get_next_destination(origin, destinations)
    assert destination_addresses[destinations.index(next_destination)] == '9742 Rennes Lane Delray Beach, FL 33446'


def test_networkx_gateway_next_destination():
    gateway = NetworkXGateway(lattice.grid_2d_graph(10, 10))
    origin = Location(0, 0)
    destinations = [Location(1, 1), Location(2, 5), Location(2,4)]
    next_destination = gateway.get_next_destination(origin, destinations)
    assert next_destination == Location(1, 1)
