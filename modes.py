from constants import *

class DefaultMode():
    def __init__(self, start_mode = WAIT):  
        self.timer = 0
        self.mode = None
        self.set_mode(start_mode)

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.time:
            if self.mode == WAIT:
                self.scatter()
            elif self.mode == SCATTER:
                self.chase()
            elif self.mode == CHASE:
                self.scatter()

            elif self.mode == RANDOM:
                self.scatter()
                
            elif self.mode == FREIGHT:
                self.scatter()

            elif self.mode == SPAWN:
                self.wait()
    
    def set_mode(self, mode):  
        if mode == SCATTER:
            self.scatter()
        elif mode == CHASE:
            self.chase()
        elif mode == WAIT:
            self.wait()
        elif mode == RANDOM:
            self.random()
        elif mode == FREIGHT:
            self.freight()
        elif mode == SPAWN:
            self.spawn()

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
        self.time = 3
        self.timer = 0

    def random(self):
        self.mode = RANDOM
        self.time = 10
        self.timer = 0
    
    def freight(self):
        self.mode = FREIGHT
        self.time = 7
        self.timer = 0

    def spawn(self):
        self.mode = SPAWN
        self.time = 5  
        self.timer = 0

    

class ModeController():
    def __init__(self, ghost, start_mode = WAIT):
        self.main_mode = DefaultMode(start_mode)
        self.current_mode = self.main_mode.mode
        self.ghost = ghost

    def update(self, dt):
        self.main_mode.update(dt)
        self.current_mode = self.main_mode.mode  
        self.ghost.update_move_method()

        if self.current_mode == SPAWN and self.ghost.node.position == self.ghost.home_goal:
            self.main_mode.set_mode(WAIT)
