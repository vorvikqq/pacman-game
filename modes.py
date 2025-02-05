from constants import *

class DefaultMode():
    def __init__(self):
        self.timer = 0
        self.mode = None
        self.wait()

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.time:
            if self.mode == WAIT:
                self.scatter() 
            elif self.mode == SCATTER:
                self.chase()
            elif self.mode == CHASE:
                self.scatter()
            

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

    def wait(self):
        self.mode = WAIT
        self.time = 5
        self.timer = 0

class ModeController():
    def __init__(self, ghost):
        self.main_mode = DefaultMode()
        self.current_mode = self.main_mode.mode
        self.ghost = ghost

    def update(self, dt):
        self.main_mode.update(dt)
        self.current_mode = self.main_mode.mode  
        self.ghost.update_move_method()  