class PriorityQueueItem:
    # This is the wrapper item class for my priority queue.
    def __init__(self, identifier, priority, item_value = None):
        # Set up.
        self.identifier = identifier
        self.priority = priority
        self.value = item_value

class PriorityQueue():
    # This is my priority queue class.
    def __init__(self):
        # Set up.
        self.items = []

    def push(self, identifier = 0, item = None, priority = 0):
        # This pushes an item onto the queue.
        self.items.append(PriorityQueueItem(identifier, priority, item))

    def peek(self):
        # This looks at the next queue item.
        return self.items[0] if len(self.items) > 0 else None
        
    def pop(self):
        # This returns the next queue item.
        return self.items.pop(0).value

    def prioritize(self):
        # This resorts the queue based on priority.
        get_priority = lambda item: item.priority
        self.items.sort(key = get_priority)

    def contents(self):
        # This returns the raw contents of the queue.
        return self.items

    def find(self, identifier):
        # This finds a queue item based on the identifier.
        results = [item for item in self.items if item.identifier == str(identifier)]
        return results.pop() if len(results) > 0 else None
    
    def __str__(self):
        # This prints a formatted string for each item in the queue.
        for index, item in enumerate(self.items):
            print(f'{item.value}')

        return ''
