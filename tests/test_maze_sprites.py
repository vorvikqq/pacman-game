import pytest
import numpy as np
import pygame
from unittest.mock import MagicMock, patch
from sprites import MazeSprites
from constants import *

@pytest.fixture(autouse=True)
def init_pygame():
    pygame.init()
    pygame.display.set_mode((800, 600))  
    yield
    pygame.quit() 

@pytest.fixture
def mock_maze_files(tmp_path):
    maze_data = "1 1 1\n0 = 0\n1 0 1"  # Спрощена структура лабіринту
    rot_data = "0 1 0\n2 0 2\n1 0 1"  # Спрощені дані поворотів

    maze_file = tmp_path / "maze.txt"
    rot_file = tmp_path / "rot.txt"

    maze_file.write_text(maze_data)
    rot_file.write_text(rot_data)

    return str(maze_file), str(rot_file)

@pytest.fixture
def maze_sprites(mock_maze_files):
    maze_file, rot_file = mock_maze_files
    return MazeSprites(maze_file, rot_file)

class TestMazeSprites:
    def test_init(self, maze_sprites):
        assert maze_sprites.data.shape == maze_sprites.rot_data.shape  
        assert isinstance(maze_sprites.data, np.ndarray)
        assert isinstance(maze_sprites.rot_data, np.ndarray)

    def test_get_image(self, maze_sprites):
        image = maze_sprites.get_image(0, 0)
        assert image is not None  

    def test_read_mazeFile(self, mock_maze_files):
        maze_file, _ = mock_maze_files
        data = MazeSprites.read_mazeFile(None, maze_file)
        assert data.shape == (3, 3)  

    def test_construct_background(self, maze_sprites):
        background = pygame.Surface((NCOLS * TILEWIDTH, NROWS * TILEHEIGHT))
        updated_bg = maze_sprites.construct_background(background, 8)
        assert updated_bg is not None  

    def test_rotate(self, maze_sprites):
        sprite = pygame.Surface((TILEWIDTH, TILEHEIGHT))
        rotated_sprite = maze_sprites.rotate(sprite, 1)  # 1 означає 90 градусів
        assert rotated_sprite is not None 
        assert rotated_sprite.get_size() == (TILEWIDTH, TILEHEIGHT) 