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
        self.goal = Vector()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.update_move_method()

    def update_move_method(self):
        if self.mode.current_mode is SCATTER:
            self.move_method = self.random_movement
            self.color = GREEN

        elif self.mode.current_mode is CHASE:
            self.move_method = self.goal_movement
            self.color = BLUE

        elif self.mode.current_mode is WAIT:
            self.move_method = self.wait_movement
            self.color = WHITE
        
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
        self.goal = self.pacman.node.position
        distances = []

        for direction in directions:
            distance = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(distance.magnitudeSquared())

        index = distances.index(min(distances))
        return directions[index]
    
    def wait_movement(self, directions):
        if UP in directions:
            return UP
        elif DOWN in directions:
            return DOWN
        return directions[0]



# class GhostsGroup():
#     def __init__(self, node, pacman):
#         self.ghost1 = Ghost(node, pacman)
#         self.ghost2 = Ghost(node, pacman)

#         self.ghosts_list = [self.ghost1, self.ghost2]