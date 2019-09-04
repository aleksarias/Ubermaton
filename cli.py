import json

import cmd2 as cmd2
from cmd2 import Statement
from networkx.generators import lattice

from domain.services import PeopleService, VehicleService, LocationMapService
from infrastructure.gateways import NetworkXGateway
from infrastructure.persistence import InMemPeopleRepository, InMemVehicleRepository, InMemLocationMapRepository
from interfaces.serializers import person_serialize
from usecases.process_time_steps import time_step_single_vehicle


class UbermatonCLI(cmd2.Cmd):
    intro = '''
# Welcome to Ubermaton command line tool
#
# Initializing map to 2 dimensional grid...
# Please specify dimensions like so: initgrid 8, 20 [enter]
# To move a time step: t [enter]
# To input json (can accept multiline json) and take a step: 
#   json [enter] 
#   {"sample": "json"} [enter] [enter]
#
# To exit program: quit [enter]
    '''

    def __init__(self):
        self.multilineCommands = ['json']
        self.map_service = None
        self.vehicle_service = VehicleService(InMemVehicleRepository())
        self.people_service = PeopleService(InMemPeopleRepository())
        cmd2.Cmd.__init__(self, use_ipython=False, multiline_commands=['json'])

    def do_initgrid(self, line: str):
        """
        Initialize grid with a particular dimension ie, 5, 8
        :param line:
        :return:
        """
        if ',' not in line:
            print('Please use format: x, y')
            return
        x, y = line.replace(' ', '').split(',')
        x, y = int(x), int(y)
        self.map_service = LocationMapService(
            InMemLocationMapRepository(), NetworkXGateway(lattice.grid_2d_graph(x, y))
        )

    def default(self, statement: Statement):
        try:
            request = json.loads(statement) if statement else []
            request = [person_serialize(item) for item in request]
            vehicle_location, passengers, dropped_off, picked_up, destinations = time_step_single_vehicle(
                request,
                self.people_service,
                self.vehicle_service,
                self.map_service
            )
        except Exception as exc:
            print(exc)

        message = f'Vehicle is at {vehicle_location} with passengers {", ".join(passengers) if passengers else None} | '
        if dropped_off:
            message += f'Dropped off {", ".join(p.name for p in dropped_off)} '
        if picked_up:
            message += f'Picked up {", ".join(p.name for p in picked_up)} '
        print(message)

    def do_json(self, line):
        if self.map_service is None:
            print('Please call initgrid command with grid dimensions. Call command help for more info.')
        else:
            self.default(line)

    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    UbermatonCLI().cmdloop()
