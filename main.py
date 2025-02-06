import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost, GhostsGroup

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
        
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)

        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.ghosts = GhostsGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.set_spawn_node(self.nodes.getNodeFromTiles(2+11.5, 14))
        self.ghosts.pinky.set_spawn_node(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.set_spawn_node(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.set_spawn_node(self.nodes.getNodeFromTiles(4+11.5, 3+14))

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt)
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
        self.ghosts.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()