class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
        return self.stack

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[0] if len(self.stack) > 0 else None

    def count(self):
        return len(self.stack)

    def contents(self):
        return self.stack
