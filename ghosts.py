import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from random import randint
from entity import Entity

class Ghost(Entity):
    #color is temp here, just for better testing
    def __init__(self, node, move_method, color, pacman = None):
        super().__init__(node)
        self.name = GHOST
        self.color = color
        self.goal = Vector()
        self.pacman = pacman
        self.move_method = move_method 
    """
        Method which overrides Entity(update) method and basically contorls movement of ghost
        Technically, for now ghosts move fully random
    """
    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt 
        if self.overshot_target():
            self.node = self.target
            directions_list = self.valid_directions_list()

            new_direction = self.move_method(self, directions_list)

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
    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]
    """
        Method for getting a closest direction to pacman that calculates the less direction to pacmans current position

        returns a closest direction to pacman
    """
    def goal_direction(self, directions):
        self.goal = self.pacman.node.position
        distances = []

        for direction in directions:
            distance = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(distance.magnitudeSquared())

        index = distances.index(min(distances))
        return directions[index]