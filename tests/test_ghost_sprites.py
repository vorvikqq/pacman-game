import pytest
from unittest.mock import Mock, patch
from sprites import GhostSprites
import pygame
from unittest.mock import MagicMock, patch
from unittest.mock import Mock, patch
from constants import *


@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((800, 600))  
    yield
    pygame.quit()  

@pytest.fixture
def mock_ghost_entity():
    ghost_entity = MagicMock()
    ghost_entity.name = BLINKY
    ghost_entity.direction = UP
    ghost_entity.mode.current_mode = CHASE
    return ghost_entity

@pytest.fixture
def ghost_sprites(mock_ghost_entity):
    return GhostSprites(mock_ghost_entity)


class TestGhostSprites:
    def test_init(self, ghost_sprites):
        assert ghost_sprites.entity is not None
        assert isinstance(ghost_sprites.x, dict)

    def test_get_start_image(self, ghost_sprites):#стартового зображення
        start_image = ghost_sprites.get_start_Image()
        assert start_image is not None

    def test_get_image(self, ghost_sprites):#за конкретними координатами
        image = ghost_sprites.get_image(0, 4)
        assert image is not None

    def test_update_freight_mode(self, ghost_sprites, mock_ghost_entity):
        mock_ghost_entity.mode.current_mode = FREIGHT
        ghost_sprites.update()
        assert mock_ghost_entity.image is not None

    def test_update_spawn_mode(self, ghost_sprites, mock_ghost_entity):
        mock_ghost_entity.mode.current_mode = SPAWN
        ghost_sprites.update()
        assert mock_ghost_entity.image is not None

    def test_update_direction(self, ghost_sprites, mock_ghost_entity):#
        mock_ghost_entity.direction = LEFT
        ghost_sprites.update()
        assert mock_ghost_entity.image is not None