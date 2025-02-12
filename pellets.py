import pygame
from vector import Vector
from constants import *
import numpy as np
from typing import List

class Pellet:
    def __init__(self, row: int, column: int):
        self.name = PELLET
        self.position = Vector(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = YELLOW
        self.radius = int(2 * TILEWIDTH / 16)#change to less num for less pellet
        self.collide_radius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            # p = self.position.asInt()
            adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
            p = (self.position + adjust).asInt() 
            pygame.draw.circle(screen, self.color, p, self.radius)

class PowerPellet(Pellet):
    def __init__(self, row: int, column: int):
        super().__init__(row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.4
        self.timer = 0

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0

class PelletGroup:
    def __init__(self, pellet_file: str):
        self.pellets: List[Pellet] = []
        self.power_pellets: List[PowerPellet] = []
        self.create_pellet_list(pellet_file)
        self.num_eaten: int = 0

    def update(self, dt: float) -> None:
        for power_pellet in self.power_pellets:
            power_pellet.update(dt)

    def create_pellet_list(self, pellet_file: str) -> None:
        data = self.read_pellet_file(pellet_file)
        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                if cell in {'.', '+'}:
                    self.pellets.append(Pellet(row_index, col_index))
                elif cell in {'P', 'p'}:
                    power_pellet = PowerPellet(row_index, col_index)
                    self.pellets.append(power_pellet)
                    self.power_pellets.append(power_pellet)

    def read_pellet_file(self, text_file: str) -> np.ndarray:
        return np.loadtxt(text_file, dtype='<U1')

    def is_empty(self) -> bool:
        return not self.pellets

    def render(self, screen):
        for pellet in self.pellets:
            pellet.render(screen)