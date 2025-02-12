import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        super().__init__(node)
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
        # self.collideRadius = 5
        self.color = YELLOW
        self.node = node
        self.set_position()
        self.target = node
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        
    
    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.get_start_image()
        self.sprites.reset()
    
    def die(self):
        self.alive = False
        self.direction = STOP

    # def set_position(self):
    #     self.position = self.node.position.copy()

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt 
        direction = self.getValidKey()
        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            
            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()

    # def valid_direction(self,direction):
    #     if direction is not STOP:
    #         if self.node.neighbors[direction] is not None:
    #             return True
    #     return False

    # def get_new_target(self, direction):
    #     if self.valid_direction(direction):
    #         return self.node.neighbors[direction]
    #     return self.node

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
    
    
    # def render(self, screen):
    #     p = self.position.asInt()
    #     pygame.draw.circle(screen, self.color, p, self.radius)
    
    # def overshot_target(self):
    #     if self.target is not None:
    #         vec1 = self.target.position - self.node.position
    #         vec2 = self.position - self.node.position
    #         node2_target = vec1.magnitudeSquared()
    #         node2_self = vec2.magnitudeSquared()
    #         return node2_self >= node2_target
    #     return False
    
    # def reverse_direction(self):
    #     self.direction *= -1
    #     temp = self.node
    #     self.node = self.target
    #     self.target = temp

    # def opposite_direction(self, direction):
    #     if direction is not STOP:
    #         if direction == self.direction * -1:
    #             return True
    #     return False

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    # def eatPellets(self, pelletList):
    #     for pellet in pelletList:
    #         if self.collideCheck(pellet):
    #             return pellet
    #     return None    
    
    def collide_ghost(self, ghost):
        return self.collideCheck(ghost)
    
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collide_radius + other.collide_radius)**2
        if dSquared <= rSquared:
            return True
        return False
    

    # #TEMP ONLY
    # def render(self, screen):
    #     p = self.position.asInt()
    #     pygame.draw.circle(screen, self.color, p, self.radius)
    #     print(p)
