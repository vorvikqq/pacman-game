import pytest
import pygame
from unittest.mock import MagicMock, patch
from unittest.mock import Mock, patch
from sprites import SpritesSheet, PacmanSprites
from animation import Animation
from constants import *

@pytest.fixture
def mock_pygame_image():
    with patch("pygame.image.load") as mock_load:
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.get_at.return_value = (0, 0, 0)  # Для прозорості
        mock_surface.get_width.return_value = 100
        mock_surface.get_height.return_value = 100
        
        # Мокаємо transform.scale
        with patch("pygame.transform.scale") as mock_scale:
            mock_scale.return_value = mock_surface
            
            mock_load.return_value = mock_surface
            yield mock_surface

@pytest.fixture
def sprite_sheet(mock_pygame_image):
    return SpritesSheet(mock_pygame_image)

@pytest.fixture
def mock_pacman():
    pacman = Mock()
    pacman.alive = True
    pacman.direction = STOP
    pacman.image = None
    return pacman

@pytest.fixture
def pacman_sprites(mock_pacman, mock_pygame_image):
    return PacmanSprites(mock_pacman)

class TestSpritesSheet:

    def test_init(self, mock_pygame_image):
        sprite_sheet = SpritesSheet(image=mock_pygame_image)
        assert sprite_sheet.sheet is mock_pygame_image

    def test_get_image(self, mock_pygame_image):
        sprite_sheet = SpritesSheet(image=mock_pygame_image)
        img = sprite_sheet.get_image(1, 1, 32, 32)

        assert img is not None
        assert mock_pygame_image.set_clip.called
        assert mock_pygame_image.subsurface.called