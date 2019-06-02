from . import stack

class Package:
    # id, address, city, state, zip_code, delivery_deadline, weight, special_notes
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

    def update_info(self, **kwargs):
        keys_to_update = kwargs.keys()
        if not len(keys_to_update):
            return
        for key_name in keys_to_update:
            try:
                self[key_name] = kwargs[key_name]
            except KeyError:
                pass

        return self

    def calculate_priority(self):
        priority = 0
        special_penalty = 0
        deadline = self.deadline.replace(':', ' ').split(' ')
        if len(deadline) == 1:
            priority = 1000 * 60 * 60 * 21 if deadline[0] == 'EOD' else 0
        elif len(deadline) == 3:
            priority += int(deadline[0]) * 1000 * 60 * 60 + int(deadline[1]) * 1000 * 60
            priority += 1000 * 60 * 60 * 12 if deadline[2] == 'PM' and int(deadline[0]) != 12 else 0

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
    def __init__(self, id = None, driver = None, capacity = 16, hub_node = 0):
        self.id = id
        self.driver = driver
        self.capacity = capacity
        self.hub_node = hub_node

        self.packages = Stack()
        self.miles_per_hour = 18
        self.speed = 0.3

        self.prev_node = None
        self.curr_node = None # Might not be necessary.
        self.next_node = None

        self.finished = False

    def load_package(self, package):
        self.packages.push(package)

    def deliver_package(self):
        package_to_deliver = self.packages.pop()
        

    def get_current_progress(self):
        truck_id = self.id
        number_of_packages = self.packages.count()

        if self.finished:
            print(f'Truck #{truck_id} has completed it\'s rounds.')
        else:
            print(f'Truck #{truck_id} has {number_of_packages} remaining.')

    def done(self):
        self.finished = True
        self.get_current_progress()

    
    

