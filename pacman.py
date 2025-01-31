import pygame
from pygame.locals import *
from vector import Vector
from constants import *

class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.directions = {
          STOP : Vector(),
          UP: Vector(0,-1),
          DOWN : Vector(0,1),
          LEFT : Vector(-1,0),
          RIGHT : Vector(1,0)
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.set_position()

    def set_position(self):
        self.position = self.node.position.copy()
    def update(self, dt):	
        direction = self.getValidKey()
        self.direction = direction
        self.node = self.get_new_target(direction)
        self.set_position()

    def valid_direction(self,direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP
    
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

