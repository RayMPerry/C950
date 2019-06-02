class PriorityQueueItem:
    def __init__(self, identifier, priority, item_value = None):
        self.identifier = identifier
        self.priority = priority
        self.value = item_value

class PriorityQueue():
    def __init__(self):
        self.items = []

    def push(self, identifier = 0, item = None, priority = 0):
        self.items.append(PriorityQueueItem(identifier, priority, item))

    def peek(self):
        return self.items[0] if len(self.items) > 0 else None
        
    def pop(self):
        return self.items.pop(0).value

    def prioritize(self):
        get_priority = lambda item: item.priority
        self.items.sort(key = get_priority)

    def contents(self):
        return self.items

    def find(self, identifier):
        results = [item for item in self.items if item.identifier == str(identifier)]
        return results.pop() if len(results) > 0 else None
    
    def modify(self, queue_item, new_value):
        pass

    def __str__(self):
        for index, item in enumerate(self.items):
            print(f'{item.value}')
            
            # if index == (len(self.items) / 2):
            #     print('===============TRUCK 2===============')
            # elif  index and not index % 10:
            #     print('=============NEXT SHIPMENT===========')

        return ''
