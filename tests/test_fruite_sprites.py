import pytest
from unittest.mock import MagicMock
from sprites import FruitSprites
import pygame
from constants import *

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((800, 600))  
    yield
    pygame.quit() 

@pytest.fixture
def mock_fruit_entity():
    fruit_entity = MagicMock()
    fruit_entity.name = "apple"  # Приклад фрукта
    return fruit_entity

@pytest.fixture
def fruit_sprites(mock_fruit_entity):
    level = 1  # Заданий рівень для тестів
    return FruitSprites(mock_fruit_entity, level)

class TestFruitSprites:
    def test_init(self, fruit_sprites):
        assert fruit_sprites.entity is not None
        assert isinstance(fruit_sprites.fruits, dict)

    def test_get_start_image(self, fruit_sprites):
        start_image = fruit_sprites.get_start_Image(0)  # Отримуємо перше зображення
        assert start_image is not None

    def test_get_image(self, fruit_sprites):
        image = fruit_sprites.get_image(16, 8)  # Тестуємо координати для фрукта
        assert image is not None

    def test_fruit_position_mapping(self, fruit_sprites):
        for k, (x, y) in fruit_sprites.fruits.items():
            image = fruit_sprites.get_image(x, y)
            assert image is not None

    def test_get_image_for_specific_fruit(self, fruit_sprites):
        # з координатами (18, 8)
        image = fruit_sprites.get_start_Image(1)  # тип 1
        assert image is not None