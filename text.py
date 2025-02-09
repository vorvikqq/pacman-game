import pygame
from vector import Vector
from constants import *

class Text():
    def __init__(self, text, color, x, y, size, time = None, visible = True, id = None):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.showtime = time
        self.visible = visible
        self.position = Vector(x, y)
        self.timer = 0
        self.label = None
        self.setup_font("PressStart2P-Regular.ttf")
        self.create_label()

    def setup_font(self, font_name):
        self.font = pygame.font.Font(font_name, self.size)

    def create_label(self):
        self.label = self.font.render(self.text, 1, self.color)

    def change_text(self, new_text):
        new_text = str(new_text)
        self.create_label()

    def update(self, dt):
        if self.showtime is not None:
            self.timer += dt

            if self.timer >= self.showtime:
                self.timer = 0
                self.showtime = None

    def render(self, screen):
        if self.visible:
            coords = self.position.asTuple()
            screen.blit(self.label, coords)



        

        


