import pytest
from unittest.mock import MagicMock
from sprites import LifeSprites
import pygame
from constants import *

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.display.set_mode((800, 600)) 
    yield
    pygame.quit()  

@pytest.fixture
def life_sprites():
    num_lives = 3  # Початкова кількість життів
    return LifeSprites(num_lives)

class TestLifeSprites:
    def test_init(self, life_sprites):
        assert isinstance(life_sprites.images, list)
        assert len(life_sprites.images) == 3  

    def test_remove_image(self, life_sprites):
        initial_count = len(life_sprites.images)
        life_sprites.remove_image()
        assert len(life_sprites.images) == initial_count - 1 

    def test_reset_lives(self, life_sprites):
        life_sprites.reset_lives(5)  
        assert len(life_sprites.images) == 5  

    def test_get_image(self, life_sprites):
        image = life_sprites.get_image(0, 0)
        assert image is not None  # Зображення повинне бути отримане

    def test_remove_image_until_empty(self, life_sprites):
        for _ in range(3):
            life_sprites.remove_image()
        assert len(life_sprites.images) == 0 

    def test_reset_lives_after_removal(self, life_sprites):
        for _ in range(3):
            life_sprites.remove_image()
        assert len(life_sprites.images) == 0 
        life_sprites.reset_lives(2)  
        assert len(life_sprites.images) == 2  