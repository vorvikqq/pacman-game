import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from fruit import Fruit
from ghosts import GhostsGroup
from pauser import Pause
from text import TextGroup
from sprites import LifeSprites
from sprites import MazeSprites

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        pygame.display.set_caption("Pac-Man Game")
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.background_norm = None
        self.background_finish = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textGroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.finishBG = False
        self.finishTime = 0.2
        self.finishTimer = 0
        self.fruit_captured = []

    def restart_game(self):
        self.lives = 5
        self.level = 0
        self.score = 0
        self.textGroup.update_score(self.score)
        self.textGroup.update_level(self.level)
        self.textGroup.show_text(READYTXT)
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.lifesprites.reset_lives(self.lives)
        self.fruit_captured = []

    def reset_level(self):
        self.pause.paused = True
        self.textGroup.show_text(READYTXT)
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None


    def next_level(self):
        self.show_entities()
        self.level += 1
        self.textGroup.update_level(self.level)
        self.pause.paused = True
        self.startGame()

    def setBackground(self):
        # self.background = pygame.surface.Surface(SCREENSIZE).convert()
        # self.background.fill(BLACK)
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_finish = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_finish.fill(BLACK)
        self.background_norm = self.mazesprites.construct_background(self.background_norm, self.level%5)
        self.background_finish = self.mazesprites.construct_background(self.background_finish, 5)
        self.finishBG = False
        self.background = self.background_norm

    def startGame(self):
        # self.setBackground()
        self.mazesprites = MazeSprites("mazetest.txt", "mazetest_rot.txt")
        self.setBackground()
        # self.background = self.mazesprites.construct_background(self.background, self.level%5)
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


        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2 + 11.5, 3 + 14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2 + 11.5, 3 + 14, RIGHT, self.ghosts)
        self.ghosts.inky.spawn_node.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.spawn_node.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.textGroup.update(dt)
        self.pelletGroup.update(dt)

        if not self.pause.paused:
            # self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkFruitEvents()
            self.checkGhostEvents()
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)
        if self.finishBG:
            self.finishTimer += dt
            if self.finishTimer >= self.finishTime:
                self.finishTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_finish
                else:
                    self.background = self.background_norm
        after_pause_method = self.pause.update(dt)
        if after_pause_method is not None:
            after_pause_method()
        self.checkEvents()
        self.render()
    
    def update_score(self, points):
        self.score += points
        self.textGroup.update_score(self.score)

    def checkFruitEvents(self):
        if self.pelletGroup.num_eaten == 50 or self.pelletGroup.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.update_score(self.fruit.points)
                self.textGroup.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                #перевірка чи походить зображення з того самого місця на файлу картинків
                fruit_captured = False
                for fruit in self.fruit_captured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruit_captured = True
                        break
                if not fruit_captured:
                    self.fruit_captured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pelletGroup.pellets)
        if pellet:
            self.pelletGroup.num_eaten += 1
            self.update_score(pellet.points)
            if self.pelletGroup.num_eaten == 30:
                self.ghosts.inky.spawn_node.allowAccess(RIGHT, self.ghosts.inky)
            if self.pelletGroup.num_eaten == 70:
                self.ghosts.clyde.spawn_node.allowAccess(LEFT, self.ghosts.clyde)
            self.pelletGroup.pellets.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()
            if self.pelletGroup.is_empty():
                self.finishBG = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)
                self.next_level()

    
    def checkEvents(self):
        for event in pygame.event.get():
            if(event.type == QUIT):
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.textGroup.hide_text()
                            self.show_entities()
                        else:
                            self.textGroup.show_text(PAUSETXT)
                            self.hide_entities()
                            # self.show_entities()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current_mode is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.textGroup.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current_mode is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.remove_image()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textGroup.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)


    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()
    
    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()
    
    def render(self):
        self.screen.blit(self.background, (0, 0))
        # self.nodes.render(self.screen)
        self.pelletGroup.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textGroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        #відображення фрукта наче життя але фрукта що пакмен його з'їв
        for i in range(len(self.fruit_captured)):
            x = SCREENWIDTH - self.fruit_captured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruit_captured[i].get_height()
            self.screen.blit(self.fruit_captured[i], (x, y))

        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()