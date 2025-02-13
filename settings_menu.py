import pygame
from pygame.locals import *
from constants import *

class SettingsMenu:
    def __init__(self, game_controller):
        self.game_controller = game_controller
        self.selected_option = 0
        self.font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 15)
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.background_colors = ['Black', 'Gray', 'Navy']
        self.options = [
            f"Difficulty: {self.difficulty_levels[self.game_controller.difficulty]}",
            f"Background Color: {self.background_colors[self.game_controller.bg_color]}"
        ]
        self.difficulty = self.game_controller.difficulty
        self.bg_color = self.game_controller.bg_color
        

    def render(self):
        self.game_controller.screen.fill((0, 0, 0))
        
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            option_text = self.font.render(option, True, color)
            self.game_controller.screen.blit(option_text, (100, 100 + i * 50))

        pygame.display.update()

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            
            if event.key == K_LEFT:
                if self.selected_option == 0:
                    self.difficulty = (self.difficulty - 1) % len(self.difficulty_levels)
                elif self.selected_option == 1:
                    self.bg_color = (self.bg_color - 1) % len(self.background_colors)

            if event.key == K_RIGHT:
                if self.selected_option == 0:
                    self.difficulty = (self.difficulty + 1) % len(self.difficulty_levels)
                elif self.selected_option == 1:
                    self.bg_color = (self.bg_color + 1) % len(self.background_colors)

            # Обновлюємо текст після зміни
            self.options[0] = f"Difficulty: {self.difficulty_levels[self.difficulty]}"
            self.options[1] = f"Background Color: {self.background_colors[self.bg_color]}"

            if event.key == K_RETURN:
                # Зберігаємо вибір і переходимо до гри
                self.game_controller.set_difficulty(self.difficulty)
                self.game_controller.set_background_color(self.background_colors[self.bg_color])
                self.game_controller.startGame()  # Запускаємо гру
                return True  # Повертаємо True, щоб завершити налаштування
        return False
