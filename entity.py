import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from random import randint

class Entity():
    def __init__(self, node):
        self.name = ""
        self.directions = {
          STOP : Vector(),
          UP: Vector(0,-1),
          DOWN : Vector(0,1),
          LEFT : Vector(-1,0),
          RIGHT : Vector(1,0)
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.collide_radius = 5
        self.radius = 10
        self.color = WHITE
        self.node = node
        self.set_position()
        self.target = node
        self.home_goal = node
        self.visible = True
        self.set_spawn_node(node)
        self.image = None
    
    def set_position(self):
        self.position = self.node.position.copy()
    
    def set_spawn_node(self, given_node):
        self.node = given_node
        self.target = given_node
        self.home_goal = given_node.position
        self.spawn_node = given_node
        self.set_position()
        self.direction = UP

    
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False
    
    """
        Method that gives us a list of all posible directions that entity can go

        returns a list of all posible directions
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

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2_target = vec1.magnitudeSquared()
            node2_self = vec2.magnitudeSquared()
            return node2_self >= node2_target
        return False
    
    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
    
    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False
    
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                #  screen.blit(self.image, self.position.asTuple())
                # correct position for enteties in game
                adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def set_speed(self, speed):
        self.speed = speed * TILEWIDTH / 16
    
    def reset(self):
        self.set_spawn_node(self.spawn_node)
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.visible = True


