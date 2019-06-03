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
    # This is the main class for the simulation.
    def __init__(self):
        # We initialize most of the constants here.
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
        # This starts the program.
        if __name__ == '__main__':
            self.load()

    def load(self):
        # This does the additional setup required to begin the simulation.
        print('Generating routes.')
        self.route_graph = graph.generate()
        print('Generating queue.')
        self.pqueue = load_queue(self.route_graph, make_packages())
        print('Creating trucks.')

        hub_node = self.route_graph.get_node_by_address('Hub')
        truck_1 = Truck(1, 'Driver 1', 16, hub_node)
        truck_3 = Truck(3, None, 16, hub_node)
        
        for item in self.pqueue.contents()[0:10]:
            # For each package in the slice, we load it into the truck and update it on the queue.
            truck_1.load_package(item.value)
            self.update_packages({ 'id': item.identifier, 'status': 'EN ROUTE - TRUCK 1' })
            
        self.trucks.append(truck_1)
            
        print('Syncing clock.')
        self.current_time = datetime.datetime(2019, 6, 1, 8, 0, 0).timestamp()
        print('Starting timer.')
        self.app_clock = clock.Clock(600, 1, 600, is_repeating=True)
        self.app_clock.start()

        print('Beginning application.')
        self.update()

    def pause(self):
        # This pauses the program's loop.
        self.state = ProgramState.PAUSED

    def stop(self):
        # This stops the program's loop.
        self.state = ProgramState.STOPPED

    def resume(self):
        # This resumes the program's loop.
        self.state = ProgramState.RUNNING
        self.update()
        return True

    def complete(self):
        # This gets the summations of the trucks and displays them. After that, it shuts down.
        total_miles_traveled = round(sum([truck.miles_traveled for truck in self.trucks]), 1)
        
        print('Simulation complete.')
        print(f'Total miles traveled: {total_miles_traveled}')
        
        self.quit()
    
    def quit(self):
        # This quits the program.
        self.stop()
        print('Shutting down application.')
        return True

    def print_packages(self):
        # This prints the table of packages.
        print(self.pqueue)
        return False

    def update_packages(self, event = None):
        # This allows us to update the packages based on a dictionary similar to the package itself.
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
    
    def update(self):
        # This is the main update loop.
        flight_arrival = datetime.datetime(2019, 6, 1, 9, 5, 0).timestamp()
        try:
            # It's rather difficult to get key presses in Python 3 without libraries.
            # So, I catch Ctrl-C (KeyboardInterrupt) and let that be the 'pause' key.
            while self.state != ProgramState.STOPPED:
                # While the program isn't stopped...
                if self.app_clock.tick():
                    # Update the app timer and if it says it's time to do things here, we do it
                    screen.clear(75)
                    print(time.ctime(self.current_time))
                    for truck in self.trucks:
                        # For each truck in the truck list...
                        truck.drive(self.route_graph, self.pqueue, self.current_time)
                        if len(truck.packages) == 0 and truck.current_node.address == 'Hub':
                            # If the truck is empty and it's at the Hub, attempt to resupply it.
                            if not truck.times_resupplied:
                                # If it has not resupplied at all, resupply the truck.
                                truck.times_resupplied += 1 
                                package_group = self.pqueue.contents()[20:31] if truck.id == 1 else self.pqueue.contents()[31:40]
                                for item in package_group:
                                    # For each item in the group of packages, load them into the truck.
                                    truck.load_package(item.value)
                                    self.update_packages({ 'id': item.identifier, 'status': f'EN ROUTE - TRUCK {truck.id}' })
                            elif truck.times_resupplied == 1:
                                # If the truck has already resupplied once, it's done.
                                truck.done()
                                
                        print(truck.get_current_progress())
                    print('Press Ctrl-C to pause the simulation.')
                    self.current_time += 60
                    if self.current_time == flight_arrival:
                        # When the flight arrives and we have all the packages, we send out the other truck.
                        self.update_packages({ 'id': '9', 'address': '410 S State St', 'city': 'Salt Lake City', 'state': 'UT', 'zip_code': '84111', 'special_notes': '' })
                        truck_2 = Truck(2, 'Driver 2', 16, self.route_graph.get_node_by_address('Hub'))
                        for item in self.pqueue.contents()[10:20]:
                            truck_2.load_package(item.value)
                            self.update_packages({ 'id': item.identifier, 'status': 'EN ROUTE - TRUCK 2' })
                        self.trucks.append(truck_2)

                    if len(self.trucks) > 1 and self.trucks[0].finished and self.trucks[1].finished:
                        # If both trucks have completed their rounds, we're done.
                        self.complete()
                        
        except KeyboardInterrupt:
            # If the user hits Ctrl-C, pause everything and present this menu.
            self.pause()
            terminating_input = False
            while not terminating_input:
                # If we've deemed the function to be non-terminating, continue to display this menu.
                print(' SIMULATION PAUSED ^C')
                print('[p] Print all parcels')
                print('[r] Resume simulation')
                print('====================')
                print('[q] Quit simulation')
                print('====================\n')
                selection = input('> ')
                try:
                    # Invoke the function and set the result to `terminating_input`.
                    terminating_input = self.key_bindings[selection.lower()]()
                except KeyError:
                    pass

def make_packages():
    # Return the list comprehension of raw packages.
    return [Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for index, row in enumerate(csv.reader(open('data/packages.csv'))) if index]
        
def load_queue(route_graph, items):
    # Begin weighing the queue items.
    _pqueue = queue.PriorityQueue()
    for item in items:
        # The farther away the destination is, the lower it goes.
        distance_penalty = int((float(route_graph.get_edge_by_addresses('Hub', item.address).distance) / 18) * 20000)
        _pqueue.push(item.id, item, item.calculate_priority() + distance_penalty)

    _pqueue.prioritize()
    return _pqueue

Application().start()

# Local Variables:
# compile-command: "python3 main.py"
# End:
