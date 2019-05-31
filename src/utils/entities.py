from . import stack

class Package:
    def __init__(self, id, addressee, deadline, city, zip_code, weight):
        self.id = id
        self.addressee = addressee
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.status = "PARKED"

    def update_info(self, **kwargs):
        keys_to_update = kwargs.keys()
        if not len(keys_to_update):
            return
        for key_name in keys_to_update:
            try:
                self[key_name] = kwargs[key_name]
            except KeyError as error:
                pass

        return self

class Truck:
    def __init__(self, id=None, driver=None, capacity=16, hub_node=0):
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

    def unload_package(self, package=None):
        self.packages.pop()

    def deliver_package(self):
        pass

    
    

