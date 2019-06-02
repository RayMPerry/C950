import datetime
from . import stack

class Package:
    def __init__(self, id, address, city, state, zip_code, deadline, weight, special_notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = "PARKED"

        self.calculate_deadline()
        
    def get_valid_keys(self):
        return ['id', 'address', 'city', 'state', 'zip_code', 'deadline', 'special_notes', 'status']

    def calculate_deadline(self):
        deadline_array = self.deadline.replace(':', ' ').split(' ')
        if len(deadline_array) == 1:
            self.deadline_timestamp = datetime.datetime(2019, 6, 1, 21, 0, 0).timestamp()
        elif len(deadline_array) == 3:
            hours = int(deadline_array[0]) + 12 if deadline_array[2] == 'PM' and deadline_array[0] != '12' else int(deadline_array[0])
            self.deadline_timestamp = datetime.datetime(2019, 6, 1, hours, int(deadline_array[1]), 0).timestamp()
    
    def update_info(self, event = {}):
        keys_to_update = event.keys()
        if not len(keys_to_update):
            return
        
        for key_name in keys_to_update:
            if key_name not in self.get_valid_keys():
                return
            
            if key_name == 'id':
                self.id = event[key_name]
            if key_name == 'address':
                self.address = event[key_name]
            if key_name == 'city':
                self.city = event[key_name]
            if key_name == 'state':
                self.state = event[key_name]
            if key_name == 'zip_code':
                self.zip_code = event[key_name]
            if key_name == 'deadline':
                self.deadline = event[key_name]
                self.calculate_deadline()
            if key_name == 'special_notes':
                self.special_notes = event[key_name]
            if key_name == 'status':
                self.status = event[key_name]

        return self

    
    def calculate_priority(self):
        priority = self.deadline_timestamp
        special_penalty = 0

        cities = {
            'Holladay': 0,
            'Murray': 0,
            'West Valley City': 1000,
            'Millcreek': 2000,
            'Salt Lake City': 3000,
        }

        if 'Can only be on truck 2' in self.special_notes:
            special_penalty += 5000
        if 'Delayed on flight' in self.special_notes:
            special_penalty += 2500
        if 'Wrong address' in self.special_notes:
            special_penalty += 2000
        if 'Must be delivered' in self.special_notes:
            special_penalty -= 1000

        return priority + cities[self.city] + special_penalty

    def __str__(self):
        return f'[ {self.status:28} ] #{self.id:3} addressed to {self.address}, {self.city}, {self.state} {self.zip_code} due @ {self.deadline} ({self.special_notes})'

class Truck:
    def __init__(self, id = None, driver = None, capacity = 16, hub_node = None):
        self.id = id
        self.driver = driver
        self.capacity = capacity
        self.hub_node = hub_node

        self.packages = []
        self.miles_per_hour = 18
        self.speed = self.miles_per_hour / 60
        self.remaining_distance = 0
        self.miles_traveled = 0
        
        self.prev_node = None
        self.current_node = hub_node # Might not be necessary.
        self.next_node = None

        self.times_resupplied = 0
        self.finished = False

    def load_package(self, package):
        self.packages.append(package)
        get_priority = lambda item: item.deadline_timestamp - 1000 if 'Delayed' in item.special_notes else item.deadline_timestamp
        self.packages.sort(key = get_priority)

    def deliver_package(self, pqueue, current_time):
        if len(self.packages) <= 0:
            return
        
        packages_to_deliver = [package for package in self.packages if package.address == self.current_node.address]
        self.packages = [package for package in self.packages if package.address != self.current_node.address]
        
        for package_to_deliver in packages_to_deliver:
            queue = pqueue.contents()
            queue_item = pqueue.find(package_to_deliver.id)
            queue_index = queue.index(queue_item)
            if not queue_item:
                return
        
            queue[queue_index].value.status = 'DELIVERED LATE' if current_time > package_to_deliver.deadline_timestamp else 'DELIVERED'

    def get_current_progress(self):
        truck_id = self.id
        number_of_packages = len(self.packages)
        
        if self.finished:
            return f'Truck #{truck_id}: Complete.'

        if self.next_node:
            return f'Truck #{truck_id}: {number_of_packages} left, {self.miles_traveled} miles traveled. En route to {self.next_node.address}.'
        else:
            return f'Truck #{truck_id}: Parked.'

    def drive(self, route_graph, pqueue, current_time):
        if self.finished:
            return
        
        if not self.next_node:
            if len(self.packages):
                self.next_node = route_graph.get_node_by_address(self.packages[0].address)
                self.remaining_distance = float(route_graph.get_edge_by_addresses(self.current_node.address, self.next_node.address).distance)
            else:
                self.next_node = self.hub_node

        if self.next_node:
            self.remaining_distance -= self.speed
            self.miles_traveled = round(self.miles_traveled + self.speed, 3)
        
        if self.remaining_distance <= 0:
            self.current_node = self.next_node
            self.deliver_package(pqueue, current_time)
            self.next_node = None
        
    def done(self):
        self.finished = True
        self.get_current_progress()
