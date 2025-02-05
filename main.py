import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("mazetest.txt")
        self.pelletGroup = PelletGroup("mazetest.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.random_ghost = Ghost(self.nodes.getRandomStartTempNode(), self.pacman)
        self.goal_ghost = Ghost(self.nodes.getRandomStartTempNode(), self.pacman)

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.pacman.update(dt)
        self.random_ghost.update(dt)
        self.goal_ghost.update(dt)
        self.pelletGroup.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()

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
        self.pacman.render(self.screen)
        self.random_ghost.render(self.screen)
        self.goal_ghost.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()