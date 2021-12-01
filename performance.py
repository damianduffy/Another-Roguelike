import time
import collections
import timeit

'''
Possible improvements:
 - draw the sprite count.
 - package more of the code in main game.py so it's just a 
    call to a method in this class (looks cleaner in the main game.py).
 - nicer console output or draw nicely to screen.
 '''

# --- FPSCounter class is used to get game performance stats ---
class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)
        self.total_program_time = 0
        self.processing_time = 0
        self.start_time = 0
        self.draw_start_time = 0
        self.draw_time = 0
        self.program_start_time = timeit.default_timer()
        self.sprite_count_list = []
        self.fps_list = []
        self.processing_time_list = []
        self.drawing_time_list = []
        self.last_fps_reading = 0

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)
    
    def get_default_timer(self):
        return timeit.default_timer()
    
    def set_processing_time(self):
        self.processing_time = self.get_default_timer() - self.start_time

    def set_start_time(self):
        self.start_time = self.get_default_timer()
    
    def set_total_program_time(self):
        self.total_program_time = int(self.get_default_timer() - self.program_start_time)
    
    def set_draw_time(self):
        self.draw_time = self.get_default_timer() - self.draw_start_time
    
    def set_draw_start_time(self):
        self.draw_start_time = self.get_default_timer()
    
    def get_total_program_time(self):
        return self.total_program_time
    
    def time_since_last_reading(self):
        return self.total_program_time > self.last_fps_reading
    
    def set_last_reading(self):
        self.last_fps_reading = self.total_program_time
    
    def get_timings(self):
        print(f"Running: {self.total_program_time}s \t| FPS: {self.get_fps():.1f} \t| Processing: {self.processing_time:.4f}s \t| Drawing: {self.draw_time:.4f}s")
    
    def update(self):
        self.fps_list.append(round(self.get_fps(), 1))
        self.processing_time_list.append(self.processing_time)
        self.drawing_time_list.append(self.draw_time)