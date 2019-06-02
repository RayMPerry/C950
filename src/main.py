# Ray Perry - 000981059

import time, datetime, os, sys, tty, csv
from enum import Enum
from utils import graph, clock, screen, queue
from utils.entities import Package, Truck

class ProgramState(Enum):
    RUNNING = 0
    PAUSED = 1
    STOPPED = 2

class Application:
    def __init__(self):
        self.state = ProgramState.RUNNING
        self.key_bindings = {
            'p': self.print_packages,
            'r': self.resume,
            'q': self.quit
        }

        self.route_graph = None
        self.pqueue = None
        self.current_time = None
        self.clock = None
        self.trucks = []

    def start(self):
        if __name__ == '__main__':
            self.load()

    def load(self):
        print('Generating routes.')
        self.route_graph = graph.generate()
        print('Generating queue.')
        self.pqueue = load_queue(self.route_graph, make_packages())
        print('Creating trucks.')

        hub_node = self.route_graph.get_node_by_address('Hub')
        truck_1 = Truck(1, 'Driver 1', 16, hub_node)
        truck_3 = Truck(3, None, 16, hub_node)
        
        for item in self.pqueue.contents()[0:10]:
            truck_1.load_package(item.value)
            update_packages(self, { 'id': item.identifier, 'status': 'EN ROUTE - TRUCK 1' })
        self.trucks.append(truck_1)
            
        print('Syncing clock.')
        self.current_time = datetime.datetime(2019, 6, 1, 8, 0, 0).timestamp()
        print('Starting timer.')
        self.app_clock = clock.Clock(600, 1, 500, is_repeating=True)
        self.app_clock.start()

        print('Beginning application.')
        self.update()

    def pause(self):
        self.state = ProgramState.PAUSED

    def stop(self):
        self.state = ProgramState.STOPPED

    def resume(self):
        self.state = ProgramState.RUNNING
        self.update()
        return True

    def complete(self):
        total_miles_traveled = sum([truck.miles_traveled for truck in self.trucks])
        
        print('Simulation complete.')
        print(f'Total miles traveled: {total_miles_traveled}')
        
        self.quit()
    
    def quit(self):
        self.state = ProgramState.STOPPED
        print('Shutting down application.')
        return True

    def print_packages(self):
        print(self.pqueue)
        return False
    
    def update(self):
        flight_arrival = datetime.datetime(2019, 6, 1, 9, 5, 0).timestamp()
        try:
            while self.state != ProgramState.STOPPED:
                if self.app_clock.tick():
                    screen.clear(75)
                    print(time.ctime(self.current_time))
                    for truck in self.trucks:
                        truck.drive(self.route_graph, self.pqueue, self.current_time)
                        if len(truck.packages) == 0 and truck.current_node.address == 'Hub':
                            if not truck.times_resupplied:
                                truck.times_resupplied += 1 
                                package_group = self.pqueue.contents()[20:31] if truck.id == 1 else self.pqueue.contents()[31:40]
                                for item in package_group:
                                    truck.load_package(item.value)
                                    update_packages(self, { 'id': item.identifier, 'status': f'EN ROUTE - TRUCK {truck.id}' })
                            elif truck.times_resupplied == 1:
                                truck.done()
                                
                        print(truck.get_current_progress())
                    print('Press Ctrl-C to pause the simulation.')
                    self.current_time += 60
                    if self.current_time == flight_arrival:
                        update_packages(self, { 'id': '9', 'address': '410 S State St', 'city': 'Salt Lake City', 'state': 'UT', 'zip_code': '84111', 'special_notes': '' })
                        truck_2 = Truck(2, 'Driver 2', 16, self.route_graph.get_node_by_address('Hub'))
                        for item in self.pqueue.contents()[10:20]:
                            truck_2.load_package(item.value)
                            update_packages(self, { 'id': item.identifier, 'status': 'EN ROUTE - TRUCK 2' })
                        self.trucks.append(truck_2)

                    if len(self.trucks) > 1 and self.trucks[0].finished and self.trucks[1].finished:
                        self.complete()
                        
        except KeyboardInterrupt:
            self.pause()
            terminating_input = False
            while not terminating_input:
                print(' SIMULATION PAUSED ^C')
                print('[p] Print all parcels')
                print('[r] Resume simulation')
                print('====================')
                print('[q] Quit simulation')
                print('====================\n')
                selection = input('> ')
                try:
                    terminating_input = self.key_bindings[selection.lower()]()
                except KeyError:
                    pass



def make_packages():
     return [Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for index, row in enumerate(csv.reader(open('data/packages.csv'))) if index]
        
def load_queue(route_graph, items):
    _pqueue = queue.PriorityQueue()
    for item in items:
        distance_penalty = (float(route_graph.get_edge_by_addresses('Hub', item.address).distance) / 18) * 10000
        _pqueue.push(item.id, item, item.calculate_priority() + distance_penalty)

    _pqueue.prioritize()
    return _pqueue

def update_packages(self, event = None):
    if not event:
        return

    queue = self.pqueue.contents()
    queue_item = self.pqueue.find(event['id'])
    queue_index = self.pqueue.contents().index(queue_item)
    if not queue_item:
        return

    old_package = queue_item.value
    new_package = Package(old_package.id, old_package.address, old_package.city, old_package.state, old_package.zip_code, old_package.deadline, old_package.weight, old_package.special_notes)
    new_package.update_info(event)
    
    queue[queue_index].value = new_package

    self.pqueue.prioritize()
    
    
Application().start()

# Local Variables:
# compile-command: "python3 main.py"
# End:
