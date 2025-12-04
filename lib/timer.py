import time
from enum import Enum

class TimerMode(Enum):
    WORK = 1
    UNSET = 0
    REST = -1

class PomoderoTimer:
    def __init__(self, work_duration : int | float = 45, rest_duration : int | float = 15):
        '''
        Initializing the pomodero timer object.
        
        :param work_duration: Amount of time spent working (in minutes).
        :type work_duration: int | float
        :param rest_duration: Amount of time spent resting (in minutes).
        :type rest_duration: int | float
        '''
        
        self.work_time = work_duration
        self.rest_time = rest_duration
        self.mode = TimerMode.UNSET
        
        self.pause_start_time = None
        self.pause_duration = 0
        
    def begin_work_time(self):
        '''
        Begin working time.
        '''
        self.start_time = time.time()
        self.end_time = self.start_time + 60 * self.work_time
        self.mode = TimerMode.WORK
    
    def begin_rest_time(self):
        '''
        Begin resting time.
        '''
        self.start_time = time.time()
        self.end_time = self.start_time + 60 * self.rest_time
        self.mode = TimerMode.REST
    
    def stop_timer(self):
        '''
        Stop timer entirely.
        '''
        self.mode = TimerMode.UNSET
    
    def get_pause_duration(self) -> int | float:
        '''
        Get pause duration.
        '''
        if self.pause_start_time is not None:
            return time.time() - self.pause_start_time
        else:
            return 0
        
    
    def pause_timer(self):
        '''
        Pause the timer. Does nothing if the timer is already paused.
        '''
        if self.pause_start_time is None:
            self.pause_start_time = time.time()
    
    def unpause_timer(self):
        '''
        Unpause the timer. Does nothing if the timer is not paused.
        '''
        if self.pause_start_time is not None:
            self.pause_duration = self.get_pause_duration()
            self.start_time += self.pause_duration
            self.end_time += self.pause_duration
            self.pause_start_time = None
    
    def update(self) -> bool:
        '''
        Update timer. Unload timer if max time reached.
        Return False if timer is unloaded.
        Return True otherwise.
        '''
        
        current_time = time.time()
        if current_time >= self.end_time:
            self.mode = TimerMode.UNSET
            return False
        return True
    
    def get_timer(self) -> tuple[float] | None:
        '''
        Get timer data.
        
        Return None if no timer is active.
        
        If a timer is active, return a tuple.
        (epoch_start_time, epoch_current_time, epoch_end_time)
        '''
        current_time = time.time()
        self.pause_duration = self.get_pause_duration()
        
        if self.mode == TimerMode.UNSET:
            return None
        
        if self.pause_start_time is not None:
            return (self.start_time + self.pause_duration, current_time, self.end_time + self.pause_duration)
        
        return (self.start_time, current_time, self.end_time)
        