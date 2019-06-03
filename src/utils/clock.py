from enum import Enum

class ClockState(Enum):
    STOPPED = 0,
    RUNNING = 1,
    PAUSED = 2

class Clock:
    # This is my timer class.
    def __init__(self, start_point = 500, timestep = 10, delay_start_point = 250, **kwargs):
        # Set up the clock.
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
        # This starts the clock...
        if self.state == ClockState.RUNNING:
            # if it's not already running.
            print('Clock has already been started.')
            return
        self.state = ClockState.RUNNING

    def stop(self):
        # This stops the clock...
        if self.state == ClockState.STOPPED:
            # if it isn't already stopped.
            print('Clock has already been stopped.')
            return
        self.state = ClockState.STOPPED

    def pause(self):
        # This pauses the clock...
        if self.state != ClockState.RUNNING:
            # if it's already running.
            print('Clock must be running to be paused.')
            return
        self.state = ClockState.PAUSED

    def reset(self):
        # This resets the clock...
        if self.state == ClockState.RUNNING:
            # if it's already running.
            print('Clock cannot be reset while running.')
            return
        self.remaining_time = self.start_point
        
    def tick(self):
        # This updates the clock...
        if self.state != ClockState.RUNNING:
            # if it's already running.
            print('Clock is not running.')
            return False
        while self.delay > 0:
            # This allows us to delay each tick for an arbitrary amount of time.
            self.delay -= self.timestep
            if self.delay_function:
                # If a function was provided, we execute that on each iteration.
                self.delay_function()
        self.delay = self.delay_start_point
        self.remaining_time -= self.timestep
        if self.remaining_time <= 0:
            # If time's up...
            if not self.is_repeating:
                # If it's not a recurring clock, we stop it.
                self.state = ClockState.STOPPED
            else:
                # Otherwise, we restart it.
                self.remaining_time = self.start_point
            return True

        return False
                
    def show(self):
        # Returns a formatted string describing the clock.
        print(f'Clock: {self.remaining_time} @ {self.timestep} (delayed by {self.delay_start_point}) per tick')
        
    def is_stopped(self):
        # Tells you whether the clock is stopped or not.
        return self.state == ClockState.STOPPED
    
