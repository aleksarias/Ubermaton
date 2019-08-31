import pytest

from domain.models import LocationsMap


def test_create_grid_locations_map():
    locations_map = LocationsMap('Bogus Square Grid')
    locations_map.init_grid_location_network(5, 5)
    assert len(locations_map.network) == 25
