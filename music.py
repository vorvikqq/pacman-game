import pygame


class MusicController():
    def __init__(self):
        pygame.mixer.init()
        self.sound_status = True
        pygame.mixer.music.load("pacman sounds/main menu music.mp3")
        self.pacman_eat_sound = pygame.mixer.Sound("pacman sounds/pacman eating.mp3")
        self.pacman_eat_ghost_sound = pygame.mixer.Sound("pacman sounds/pacman eating ghost.mp3")
        self.pacman_die_sound = pygame.mixer.Sound("pacman sounds/pacman die.mp3")
        pygame.mixer.music.set_volume(0.15)
        self.pacman_eat_sound.set_volume(0.5)
        self.pacman_eat_ghost_sound.set_volume(0.15)
        self.pacman_die_sound.set_volume(0.15)

    def play_bg_music(self):
        pygame.mixer.music.play()

    def play_pacman_eat_music(self):
        if self.sound_status:
            if self.pacman_eat_sound.get_num_channels() == 0:  
                self.pacman_eat_sound.play(maxtime=280)

    def play_pacman_eat_ghost(self):
        if self.sound_status:
             self.pacman_eat_ghost_sound.play()

    def play_pacman_die(self):
        if self.sound_status == True:
            pygame.mixer.music.stop()
            self.pacman_eat_sound.stop()
            self.pacman_die_sound.play()


    def pause_music(self):
        if self.sound_status == True:
            pygame.mixer.music.pause()
            self.sound_status = False
        else:
            pygame.mixer.music.unpause()
            self.sound_status = True
