from enum import Enum

class ClockState(Enum):
    STOPPED = 0,
    RUNNING = 1,
    PAUSED = 2

class Clock:
    def __init__(self, start_point = 500, timestep = 10, delay_start_point = 250, **kwargs):
        self.start_point = start_point
        self.timestep = timestep
        self.remaining_time = self.start_point
        self.delay_start_point = delay_start_point
        self.delay = self.delay_start_point

        try:
            self.is_repeating = kwargs['is_repeating']
        except KeyError:
            self.is_repeating = False

        try:
            self.delay_function = kwargs['delay_function']
        except KeyError:
            self.delay_function = None

        self.state = ClockState.STOPPED

    def start(self):
        if self.state == ClockState.RUNNING:
            print('Clock has already been started.')
            return
        self.state = ClockState.RUNNING

    def stop(self):
        if self.state == ClockState.STOPPED:
            print('Clock has already been stopped.')
            return
        self.state = ClockState.STOPPED

    def pause(self):
        if self.state != ClockState.RUNNING:
            print('Clock must be running to be paused.')
            return
        self.state = ClockState.PAUSED

    def reset(self):
        if self.state == ClockState.RUNNING:
            print('Clock cannot be reset while running.')
            return
        self.remaining_time = self.start_point
        
    def tick(self):
        if not self.state == ClockState.RUNNING:
            print('Clock is not running.')
            return False
        while self.delay > 0:
            self.delay -= self.timestep
            if self.delay_function:
                self.delay_function()
        self.delay = self.delay_start_point
        self.remaining_time -= self.timestep
        if self.remaining_time <= 0:
            if not self.is_repeating:
                self.state = ClockState.STOPPED
            else:
                self.remaining_time = self.start_point
            return True

        return False
                
                
    def show(self):
        print(f'Clock: {self.remaining_time} @ {self.timestep} (delayed by {self.delay_start_point}) per tick')
        
    def is_stopped(self):
        return self.state == ClockState.STOPPED
    
