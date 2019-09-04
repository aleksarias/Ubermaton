import os
import pickle

from parametrization import Parametrization
from networkx.generators.lattice import grid_2d_graph

import config
from infrastructure.gateways import GoogleDirectionsGateway, NetworkXGateway
from interfaces.serializers import json_serialize

gdg = GoogleDirectionsGateway(config.GOOGLE_API_KEY)
ng = NetworkXGateway(grid_2d_graph(10, 10))

origin = gdg.get_address_location('5502 Broken Sound Blvd NW Boca Raton, FL')
destinations = [
    gdg.get_address_location(d) for d in [
        '7841 NW 170th St. Hialeah, FL 33015',
        '1182 NW 162nd Ave. Pembroke Pines, FL 33028',
        '9742 Rennes Lane Delray Beach, FL 33446', ]
]


@Parametrization.parameters('actual', 'expected')
@Parametrization.case(
    'test_itinerary_json_serialize',
    actual=json_serialize(gdg.get_next_destination(origin, destinations)),
    expected='interfaces/fixtures/directions_gateway_itinerary.pkl'
)
def test_custom_json_serializer(actual, expected):
    if os.getenv('GEN_GOLDEN_FILES'):
        with open(expected, 'wb') as fh:
            pickle.dump(actual, fh)
    expected_obj = pickle.load(open(expected, 'rb'))
    assert actual == expected_obj
