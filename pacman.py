import pygame
from pygame.locals import *
from vector import Vector
from constants import *

class Pacman(object):
    def __init__(self):
        self.name = PACMAN
        self.position = Vector(200, 400)
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

    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        self.direction = direction
    
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

