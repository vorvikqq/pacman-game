from constants import *

class Animation(object):
    def __init__(self, frames=[], speed=40, loop=True):
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop #repeat animation
        self.d_time = 0
        self.is_finished = False

    def reset(self):
        self.current_frame = 0
        self.is_finished = False

    def update(self, dt):
        if not self.is_finished:
            self.next_frame(dt)
        if self.current_frame == len(self.frames):#якщо досягається останнього кадру
            if self.loop:
                self.current_frame = 0 #починаємо спочтку
            else:
                self.is_finished = True
                self.current_frame -= 1
   
        return self.frames[self.current_frame]
    
    def next_frame(self, d_time):
        self.d_time += d_time
        if self.d_time >= (1.0 / self.speed):
            self.current_frame += 1
            self.d_time = 0