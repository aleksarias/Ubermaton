import json

import config
from interfaces.serializers import json_serialize
from infrastructure.gateways import GoogleDirectionsGateway


def test_google_directions_gateway_geocoding():
    gateway = GoogleDirectionsGateway(api_key=config.GOOGLE_API_KEY)
    print(json_serialize(gateway.get_address_location('5502 Broken Sound Blvd NW Boca Raton, FL 33487')))


def test_google_directions_gateway_distance_matrix():
    gateway = GoogleDirectionsGateway(api_key=config.GOOGLE_API_KEY)
    origin = '5502 Broken Sound Blvd NW Boca Raton, FL'
    destinations = [
        '7841 NW 170th St. Hialeah, FL 33015',
        '1182 NW 162nd Ave. Pembroke Pines, FL 33028',
        '9742 Rennes Lane Delray Beach, FL 33446',
    ]
    print(json.dumps(gateway.get_distance_matrix(origin, destinations)))


def test_google_directions_gateway_itinerary():
    pass
