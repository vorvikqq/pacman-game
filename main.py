import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from fruit import Fruit

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("mazetest.txt")
        self.pelletGroup = PelletGroup("mazetest.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.getStartTempNode())

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.pacman.update(dt)
        self.pelletGroup.update(dt)
        if self.fruit is not None:
            self.fruit.update(dt)
        self.checkPelletEvents()
        self.checkFruitEvents()
        self.checkEvents()
        self.render()
    
    def checkFruitEvents(self):
        if self.pelletGroup.num_eaten == 50 or self.pelletGroup.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pelletGroup.pellets)
        if pellet:
            self.pelletGroup.num_eaten += 1
            self.pelletGroup.pellets.remove(pellet)

    def checkEvents(self):
        for event in pygame.event.get():
            if(event.type == QUIT):
                exit()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pelletGroup.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()