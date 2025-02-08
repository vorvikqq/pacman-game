import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from fruit import Fruit
from ghosts import GhostsGroup
from pauser import Pause

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.startGame()

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

        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.ghosts = GhostsGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.set_spawn_node(self.nodes.getNodeFromTiles(2+11.5, 14))
        self.ghosts.pinky.set_spawn_node(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.set_spawn_node(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.set_spawn_node(self.nodes.getNodeFromTiles(4+11.5, 3+14))

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.pelletGroup.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkFruitEvents()
            self.checkGhostEvents()
        after_pause_method = self.pause.update(dt)
        if after_pause_method is not None:
            after_pause_method()
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
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()
            if self.pelletGroup.is_empty():
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    
    def checkEvents(self):
        for event in pygame.event.get():
            if(event.type == QUIT):
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause.set_pause(player_paused=True)
                    if not self.pause.paused:
                        self.show_entities
                    else:
                        self.hide_entities()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current_mode is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()

    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()
    
    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pelletGroup.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()