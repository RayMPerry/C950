# Ray Perry - 000981059

import time, os, sys, tty, csv
from enum import Enum
from utils import graph, clock, screen, queue
from utils.entities import Package

class ProgramState(Enum):
    RUNNING = 0
    PAUSED = 1
    STOPPED = 2

class Application:
    def __init__(self):
        self.state = ProgramState.RUNNING
        self.key_bindings = {
            'p': self.pause,
            'q': self.quit
        }
        tty.setcbreak(sys.stdin)

    def start(self):
        if __name__ == '__main__':
            self.load()

    def load(self):
        print('Beginning application.')
        self.update()

    def detect_keypress(self):
        input = sys.stdin.read(1)
        if len(input) > 0:
            try:
                self.key_bindings[input]
            except KeyError:
                pass
        return

    def pause(self):
        print('Paused.')
        self.state = ProgramState.PAUSED

    def stop(self):
        print('Stopped.')
        self.state = ProgramState.STOPPED
                    
    def quit(self):
        self.state = ProgramState.STOPPED
        print('Shutting down application.')
        
    def update(self):
        test1(self)


def test1(self):
    print('Generating routes.')
    route_graph = graph.generate()
    print('Generating queue.')
    pqueue = load_queue()

    print('Starting clock.')
    app_clock = clock.Clock(600, 1, 45000, is_repeating=True)
    app_clock.start()
    self.quit()
    
    try:
        while self.state != ProgramState.STOPPED:
            screen.clear(36)
            app_clock.show()
            app_clock.tick()
            if app_clock.is_stopped():
                self.quit()
    except KeyboardInterrupt:
        self.quit()

def load_queue():
    _pqueue = queue.PriorityQueue()

    with open('data/packages.csv') as packages_file:
        for index, row in enumerate(csv.reader(packages_file)):
            if index:
                package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                _pqueue.push(package.id, package, package.calculate_priority())
    
    _pqueue.prioritize()

    print(_pqueue)

    return _pqueue

    
Application().start()

# Local Variables:
# compile-command: "python3 main.py"
# End:
