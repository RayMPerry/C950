import datetime

class Package:
    # This is my package class.
    def __init__(self, id, address, city, state, zip_code, deadline, weight, special_notes):
        # Set up.
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
        # This returns an array of valid keys. I planned on making it assign things programmatically.
        return ['id', 'address', 'city', 'state', 'zip_code', 'deadline', 'special_notes', 'status']

    def calculate_deadline(self):
        # This calculates the UNIX timestamp that I use as the main weighting factor in the queue.
        deadline_array = self.deadline.replace(':', ' ').split(' ')
        if len(deadline_array) == 1:
            # If the array contains exactly one element, it's probably `EOD`.
            self.deadline_timestamp = datetime.datetime(2019, 6, 1, 17, 0, 0).timestamp()
        elif len(deadline_array) == 3:
            # If the array contains exactly three elements, it was parsable and I can do my math on it.
            hours = int(deadline_array[0]) + 12 if deadline_array[2] == 'PM' and deadline_array[0] != '12' else int(deadline_array[0])
            self.deadline_timestamp = datetime.datetime(2019, 6, 1, hours, int(deadline_array[1]), 0).timestamp()
    
    def update_info(self, event = {}):
        # This updates the package.
        keys_to_update = event.keys()
        if not len(keys_to_update):
            # If nothing's there, we don't care.
            return
        
        for key_name in keys_to_update:
            # For each key name, we try to safely update it.
            if key_name not in self.get_valid_keys():
                # If it's invalid, throw it out.
                return

            # Assign the appropriate value to its property.
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
                # Set the deadline and recalculate the timestamp.
                self.deadline = event[key_name]
                self.calculate_deadline()
            if key_name == 'special_notes':
                self.special_notes = event[key_name]
            if key_name == 'status':
                self.status = event[key_name]

        return self

    
    def calculate_priority(self):
        # This calculates the majority of weighting factors sans the distance penalty.
        priority = self.deadline_timestamp
        special_penalty = 0

        cities = {
            'Holladay': 0,
            'Murray': 0,
            'West Valley City': 2000,
            'Millcreek': 3000,
            'Salt Lake City': 6000,
        }

        # Certain phrases in `special_notes` are weighted up and down, based on urgency.
        if 'Delayed on flight' in self.special_notes:
            special_penalty += 7000
        if 'Can only be on truck 2' in self.special_notes:
            special_penalty += 5000
        if 'Wrong address' in self.special_notes:
            special_penalty += 2500
        if 'Must be delivered' in self.special_notes:
            special_penalty -= 3000

        return priority + cities[self.city] + special_penalty

    def __str__(self):
        # Returns a formatted string about the package.
        return f'[ {self.status:28} ] #{self.id:3} addressed to {self.address}, {self.city}, {self.state} {self.zip_code} due @ {self.deadline} [{self.weight} oz] ({self.special_notes})'

class Truck:
    # This is my truck class.
    def __init__(self, id = None, driver = None, capacity = 16, hub_node = None):
        # Set up.
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

    def load_package(self, package, priority = 0):
        # This loads the package into the truck and sorts it again to ensure the weighting is maintained.
        highest_priority = lambda item: item.deadline_timestamp + priority - 5000 if 'Delayed' in item.special_notes else item.deadline_timestamp + priority
        self.packages.sort(key = highest_priority)
        self.packages.append(package)

    def deliver_package(self, route_graph, pqueue, current_time):
        # If we've reached our destination, attempt to deliver the appropriate packages.
        if len(self.packages) <= 0:
            return
        
        packages_to_deliver = [package for package in self.packages if package.address == self.current_node.address]
        self.packages = [package for package in self.packages if package.address != self.current_node.address]
        
        for package_to_deliver in packages_to_deliver:
            # For each package to deliver, update the original queue.
            queue = pqueue.contents()
            queue_item = pqueue.find(package_to_deliver.id)
            queue_index = queue.index(queue_item)
            if not queue_item:
                # If you can't find it, throw it out.
                return
        
            queue[queue_index].value.status = 'DELIVERED LATE' if current_time > package_to_deliver.deadline_timestamp else 'DELIVERED'
        self.sort_packages_by_distance(route_graph)

    def sort_packages_by_distance(self, route_graph):
        def closest_distance(package):
            distance = float(route_graph.get_edge_by_addresses(self.current_node.address, package.address).distance)
            return distance * -1 if 'Delayed' in package.special_notes else distance 
        self.packages.sort(key = closest_distance)
            
    def get_current_progress(self):
        # This returns a formatted string based on the truck's progress.
        truck_id = self.id
        number_of_packages = len(self.packages)
        
        if self.finished:
            # If the truck is finished...
            return f'Truck #{truck_id}: Complete.'

        if self.next_node:
            # If the truck has another destination...
            return f'Truck #{truck_id}: {number_of_packages} left, {self.miles_traveled} miles traveled. En route to {self.next_node.address}.'
        else:
            # If the truck is waiting...
            return f'Truck #{truck_id}: Parked.'

    def drive(self, route_graph, pqueue, current_time):
        # This updates the truck.
        if self.finished:
            # If it's finished, don't do anything.
            return
        
        if not self.next_node:
            # If it doesn't have a destination, try to give it one.
            if len(self.packages):
                # If it has packages, go to the next destination.
                self.next_node = route_graph.get_node_by_address(self.packages[0].address)
                # self.next_node = route_graph.get_closest_node(self.current_node, self.packages)
                self.remaining_distance = float(route_graph.get_edge_by_addresses(self.current_node.address, self.next_node.address).distance)
            else:
                # Otherwise, go back to the Hub to resupply.
                self.next_node = self.hub_node

        if self.next_node:
            # If there is another destination, update.
            self.remaining_distance -= self.speed
            self.miles_traveled = round(self.miles_traveled + self.speed, 3)
        
        if self.remaining_distance <= 0:
            # If we've reached the destination, deliver the packages and wait.
            self.current_node = self.next_node
            self.deliver_package(route_graph, pqueue, current_time)
            self.next_node = None
        
    def done(self):
        self.finished = True
        self.get_current_progress()
