import pygame
from .timer import PomoderoTimer, TimerMode

class PomoderoTimerUI(PomoderoTimer):
    def __init__(self, width : int, height : int, border_size : int, border_color : tuple[int], inside_padding : int, drain_color : tuple[int], fill_color : tuple[int], empty_color : tuple[int] = (0, 0, 0), work_duration : int | float = 45, rest_duration : int | float = 15):
        '''
        Initialize Pomodero Timer Surface for Pygame.
        
        :param height: Height of the timer in pixels.
        :type height: int
        :param width: Width of the timer in pixels.
        :type width: int
        :param border_size: The size of the border.
        :type border_size: int
        :param border_color: The color of the border.
        :type border_color: tuple[int]
        :param inside_padding: The padding amount between the bar and the border in pixels (0 means no padding).
        :type inside_padding: int
        :param drain_color: Color the bar displays while it is being drained (working time).
        :type drain_color: tuple[int]
        :param fill_color: Color the bar displays while it is being filled (resting time). 
        :type fill_color: tuple[int]
        :param empty_color: Color the bar displays behind the filled segment.
        :type empty_color: tuple[int]
        :param work_duration: Amount of time spent working (in minutes).
        :type work_duration: int | float
        :param rest_duration: Amount of time spent resting (in minutes).
        :type rest_duration: int | float
        '''
        super().__init__(work_duration, rest_duration)
        
        self.height = height
        self.width = width
        
        self.border_size = border_size
        self.padding = inside_padding
        
        self.border_color = border_color
        self.drain_color = drain_color
        self.fill_color = fill_color
        self.empty_color = empty_color
        
        self.timer_object = pygame.Surface((width, height))
        
        self.work_start_alarm = pygame.mixer.Sound("sound/2001_battle_start.wav")
        self.work_start_alarm.set_volume(1)
        
        self.work_end_alarm   = pygame.mixer.Sound("sound/2016_quest_clear.wav")
        self.work_end_alarm.set_volume(1)
    
    def draw_timer(self) -> pygame.Surface:
        '''
        Return the timer object.
        '''
        
        self.timer_object.fill(self.border_color)
        # Draw border
        pygame.draw.rect(
            self.timer_object, 
            self.empty_color, 
            (
                (self.border_size, self.border_size), 
                (self.width - 2 * self.border_size, self.height - 2 * self.border_size)
            )
        )
        bar_width  = self.width  - (self.border_size + self.padding) * 2
        bar_height = self.height - (self.border_size + self.padding) * 2
        
        timer_data = self.get_timer()
        filled_pixel = int(min(max(((timer_data[1] - timer_data[0]) / (timer_data[2] - timer_data[0])), 0), 1) * bar_width)
        
        # Draw filled bar
        if self.mode == TimerMode.WORK:
            pygame.draw.rect(
                self.timer_object,
                self.drain_color if not self.is_timer_paused() else (128, 128, 128),
                (
                    (self.border_size + self.padding, self.border_size + self.padding),
                    (bar_width - filled_pixel, bar_height)
                )
            )
        elif self.mode == TimerMode.REST:
            pygame.draw.rect(
                self.timer_object,
                self.fill_color if not self.is_timer_paused() else (128, 128, 128),
                (
                    (self.border_size + self.padding, self.border_size + self.padding),
                    (filled_pixel, bar_height)                    
                )
            )
        
        return self.timer_object
    
    def timer_update(self):
        '''
        Update timer
        '''
        last_mode = self.mode
        if not self.update():
            if last_mode == TimerMode.WORK:
                self.work_end_alarm.play()
                self.begin_rest_time()
            else:
                self.work_start_alarm.play()
                self.begin_work_time()
    
    def toggle_pause_timer(self):
        '''
        Toggle pause the timer.
        '''
        if self.pause_start_time is None:
            self.pause_timer()
        else:
            self.unpause_timer()
    
    def is_timer_paused(self) -> bool:
        '''
        Check if the timer is paused.
        '''
        return self.pause_start_time is not None

    def is_work_time(self) -> bool:
        '''
        Check if it is work time.
        '''
        return self.mode == TimerMode.WORK
    
    def stop_internal_timer(self):
        '''
        Kill.
        '''
        self.stop_timer()