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
        self.destroy = False
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
        self.text = str(new_text)
        self.create_label()

    def update(self, dt):
        if self.showtime is not None:
            self.timer += dt

            if self.timer >= self.showtime:
                self.timer = 0
                self.showtime = None
                self.destroy = True

    def render(self, screen):
        if self.visible:
            coords = self.position.asTuple()
            screen.blit(self.label, coords)


class TextGroup():
    def __init__(self):
        self.nextid = 5
        self.alltext = {}
        self.setup_text()
        self.show_text(READYTXT)

    def add_text(self, text, color, x, y, size, time=None, id=None):
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        self.nextid += 1
        return self.nextid
        
    def remove_text(self, id):
        self.alltext.pop(id)

    def setup_text(self):
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, TILEHEIGHT)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, TILEHEIGHT)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, TILEHEIGHT, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, TILEHEIGHT, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, TILEHEIGHT, visible=False)
        self.add_text("SCORE", WHITE, 0, 0, TILEHEIGHT)
        self.add_text("LEVEL", WHITE, 23*TILEWIDTH, 0, TILEHEIGHT)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.remove_text(tkey)

    def show_text(self, id):
        self.hide_text()
        self.alltext[id].visible = True

    def hide_text(self):
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def update_score(self, score):
        self.update_text(SCORETXT, str(score).zfill(8))

    def update_level(self, level):
        self.update_text(LEVELTXT, str(level + 1).zfill(3))

    def update_text(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].change_text(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)

    



        

        


