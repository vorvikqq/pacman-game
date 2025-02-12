import pygame
from constants import *
import numpy as np
from animation import Animation

class SpritesSheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor) #take color that made that transparent
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        # according to the constants
        # the size of the sprite sheet changes 
        #AND! regardless of the value of TILEWIDTH and TILEHEIGHT, 
        # sprites will be displayed correctly

    def get_image(self, x, y, width, height):
        """
        method that cuts out a single sprite from a spritesheet
        """
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())
    
# Creating separate classes to store 
# all character part sprites to separate them 
# from the class class and avoid a sprite table file.

class PacmanSprites(SpritesSheet):
    def __init__(self, entity):
        SpritesSheet.__init__(self)
        self.entity = entity
        self.entity.image = self.get_start_Image()
        self.animations = {}
        self.define_ani_for_pacman()
        self.stop_image = (8, 0)

    def get_start_Image(self):
        """ 
        Returns the initial image of Pacman (for start position)
        """
        return self.get_image(8, 0)
        
    def get_image(self, x, y):
        """
        Recives a sprite image from the sprite sheet
        """
        return SpritesSheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)
    
    def define_ani_for_pacman(self):
        """
        a set of animations for different directions of movement for pacman
        """
        self.animations[LEFT] = Animation(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animation(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animation(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animation(((8,2), (4, 0), (4, 2), (4, 0)))
    
    def update(self, d_time):
        if self.entity.direction == LEFT:
            self.entity.image = self.get_image(*self.animations[LEFT].update(d_time))
            self.stop_image = (8, 0)
        elif self.entity.direction == RIGHT:
            self.entity.image = self.get_image(*self.animations[RIGHT].update(d_time))
            self.stop_image = (10, 0)
        elif self.entity.direction == DOWN:
            self.entity.image = self.get_image(*self.animations[DOWN].update(d_time))
            self.stop_image = (8, 2)
        elif self.entity.direction == UP:
            self.entity.image = self.get_image(*self.animations[UP].update(d_time))
            self.stop_image = (10, 2)
        elif self.entity.direction == STOP:
            self.entity.image = self.get_image(*self.stop_image)
    
    def reset(self):
        """
        Reset all animations to their original state
        """
        for key in list(self.animations.keys()):
            self.animations[key].reset()

class GhostSprites(SpritesSheet):
    def __init__(self, entity):
        SpritesSheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.get_start_Image()
               
    def get_start_Image(self):
        return self.get_image(self.x[self.entity.name], 4)

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)
    
    #add ani (ani picture) for ghost
    def update(self):
        x = self.x[self.entity.name]
        if self.entity.direction == LEFT:
            self.entity.image = self.get_image(x, 8)
        elif self.entity.direction == RIGHT:
            self.entity.image = self.get_image(x, 10)
        elif self.entity.direction == DOWN:
            self.entity.image = self.get_image(x, 6)
        elif self.entity.direction == UP:
            self.entity.image = self.get_image(x, 4)

class FruitSprites(SpritesSheet):
    def __init__(self, entity):
        SpritesSheet.__init__(self)
        self.entity = entity
        self.entity.image = self.get_start_Image()

    def get_start_Image(self):
        return self.get_image(16, 8)

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class LifeSprites(SpritesSheet):
    def __init__(self, numlives):
        SpritesSheet.__init__(self)
        self.reset_lives(numlives)
    
    def remove_image(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def reset_lives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.get_image(0,0))

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)
    
class MazeSprites(SpritesSheet):
    def __init__(self, mazefile, rot_file):
        SpritesSheet.__init__(self)
        self.data = self.read_mazeFile(mazefile)
        self.rot_data = self.read_mazeFile(rot_file)

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, TILEWIDTH, TILEHEIGHT)

    def read_mazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def construct_background(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)
                    rot_val = int(self.rot_data[row][col])#get val for rotate 
                    sprite = self.rotate(sprite, rot_val)#give it val for out sprite object
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background
    
    def rotate(self, sprite, value):
       return pygame.transform.rotate(sprite, value*90)#each time miltiply by 90
