from abc import ABC, abstractmethod
from typing import List

from domain.models import Location


class DirectionsGateway(ABC):

    @abstractmethod
    def get_itinerary(self, origin, destinations):
        pass
