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


class TestPacmanSprites:
    def test_init(self, pacman_sprites):
        assert pacman_sprites.entity is not None
        assert isinstance(pacman_sprites.animations, dict)
        assert pacman_sprites.stop_image == (8, 0)

    def test_get_start_image(self, pacman_sprites):#стартове зображення 
        with patch.object(pacman_sprites, "get_image", return_value="mock_image") as mock_get_image:
            image = pacman_sprites.get_start_Image()
            assert image == "mock_image"
            mock_get_image.assert_called_once_with(8, 0)

    def test_define_animations(self, pacman_sprites):#наявність ані
        directions = [LEFT, RIGHT, UP, DOWN, DEATH]
        for direction in directions:
            assert direction in pacman_sprites.animations
            assert isinstance(pacman_sprites.animations[direction], Animation)

    def test_update_moving(self, pacman_sprites, mock_pacman):#анімація під час руху
        mock_pacman.direction = LEFT
        with patch.object(pacman_sprites.animations[LEFT], "update", return_value=(0, 2)) as mock_update, \
             patch.object(pacman_sprites, "get_image", return_value="mock_image") as mock_get_image:
            pacman_sprites.update(0.1)
            mock_update.assert_called_once_with(0.1)
            mock_get_image.assert_called_once_with(0, 2)
            assert mock_pacman.image == "mock_image"

    def test_update_stop(self, pacman_sprites, mock_pacman):#зупинка анімації 
        mock_pacman.direction = STOP
        with patch.object(pacman_sprites, "get_image", return_value="mock_image") as mock_get_image:
            pacman_sprites.update(0.1)
            mock_get_image.assert_called_once_with(8, 0)
            assert mock_pacman.image == "mock_image"

    def test_update_death(self, pacman_sprites, mock_pacman):#анімація смерті
        mock_pacman.alive = False
        with patch.object(pacman_sprites.animations[DEATH], "update", return_value=(0, 12)) as mock_update, \
             patch.object(pacman_sprites, "get_image", return_value="death_image") as mock_get_image:
            pacman_sprites.update(0.1)
            mock_update.assert_called_once_with(0.1)
            mock_get_image.assert_called_once_with(0, 12)
            assert mock_pacman.image == "death_image"

    def test_reset(self, pacman_sprites):
        with patch.object(pacman_sprites.animations[LEFT], "reset") as mock_reset:
            pacman_sprites.reset()
            mock_reset.assert_called_once()