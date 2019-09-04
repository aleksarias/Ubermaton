from abc import ABC, abstractmethod
from typing import List, Set

from domain.models import Location


class DirectionsGateway(ABC):

    @abstractmethod
    def get_next_destination(self, origin: Location, destinations: List[Location]) -> Location:
        pass

    @abstractmethod
    def shortest_path_to_destination(self, origin: Location, destination: Location) -> List[Location]:
        pass
