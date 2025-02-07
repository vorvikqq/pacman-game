import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from random import randint
from entity import Entity
from modes import ModeController

class Ghost(Entity):

    def __init__(self, node, pacman):
        super().__init__(node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.update_move_method()

    def update_move_method(self):
        if self.mode.current_mode is SCATTER:
            self.set_speed(100)
            self.move_method = self.scatter_movement
            # self.color = ORANGE

        elif self.mode.current_mode is CHASE:
            self.set_speed(100)
            self.move_method = self.goal_movement
            # self.color = BLUE

        elif self.mode.current_mode is WAIT:
            self.set_speed(100)
            self.move_method = self.wait_movement
            # self.color = WHITE

        elif self.mode.current_mode is RANDOM:
            self.set_speed(100)
            self.move_method = self.random_movement
            # self.color = GREEN

        elif self.mode.current_mode is FREIGHT:
            self.set_speed(50)
            self.move_method = self.freight_movement

        elif self.mode.current_mode is SPAWN:
            self.set_speed(200)
            self.move_method = self.spawn_movement

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position

        elif self.mode.current_mode is SCATTER:
            self.goal = self.scatter_goal


        
    """
        Method which overrides Entity(update) method and basically contorls movement of ghost
        Technically, for now ghosts move fully random
    """
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        self.mode.update(dt)

        if self.overshot_target():
            self.node = self.target
            directions_list = self.valid_directions_list()

            new_direction = self.move_method(directions_list)

            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

            self.target = self.get_new_target(new_direction)

            if self.target != self.node:
                self.direction = new_direction
                
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

        self.update_goal()
        
    """
        Method for getting all avaliable directions for ghost to move

        returns a list of all possible directions to go 
    """
    def valid_directions_list(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions
    
    """
        Method for getting a random direction from list

        returns random element from given directions list
    """
    def random_movement(self, directions):
        return directions[randint(0, len(directions) - 1)]
    """
        Method for getting a closest direction to pacman that calculates the less direction to pacmans current position

        returns a closest direction to pacman
    """
    def goal_movement(self, directions):
        distances = []

        for direction in directions:
            distance = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(distance.magnitudeSquared())

        index = distances.index(min(distances))
        return directions[index]
    
    def wait_movement(self, directions):
        return self.direction * -1
    
    def scatter_movement(self, directions):
        return self.goal_movement(directions)
    
    def freight_movement(self, directions):
        return self.random_movement(directions)
    
    def spawn_movement(self, directions):
        return self.goal_movement(directions)
    
    def start_freight(self):
        self.mode.set_freight_mode()
        if self.mode.current_mode == FREIGHT:
            self.set_speed(50)
            self.move_method = self.random_movement
    
    def normal_mode(self):
        self.set_speed(100)
        self.move_method = self.goal_movement


class Blinky(Ghost):
    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.mode = ModeController(self, SCATTER)  
        self.color = PURPLE

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(0, 0)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal

class Pinky(Ghost):
    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.color = PINK

        
    def update_goal(self):
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(520, 80)

        
        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal

class Inky(Ghost):
    def __init__(self, node, pacman, blinky = None):
        super().__init__(node, pacman)
        self.color = CYAN
        self.blinky = blinky


    def update_goal(self):
        if self.mode.current_mode is CHASE:
            pacman_plus_two = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
            self.goal = (pacman_plus_two - self.blinky.position) * 2 + self.blinky.position

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(520, 640)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class Clyde(Ghost):
    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.color = ORANGE


    def update_goal(self):
        if self.mode.current_mode is CHASE:
            d = self.pacman.position - self.position

            d_squared = d.magnitudeSquared()

            if d_squared <= (TILEWIDTH * 8) ** 2:
                self.mode.current_mode = SCATTER
                self.goal = Vector(0, TILEHEIGHT*NROWS)

            else:
                self.goal = self.pacman.node.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(0, TILEHEIGHT*NROWS)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class GhostsGroup():
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)

        self.ghosts_list = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts_list)
    
    def update(self, dt):
        for ghost in self.ghosts_list:
            ghost.update(dt)
    
    def start_freight(self):
        for ghost in self:
            ghost.start_freight()
        self.resetPoints()

    def render(self, screen):
        for ghost in self.ghosts_list:
            ghost.render(screen)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200