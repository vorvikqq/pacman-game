import pytest
import pygame
import numpy as np
from unittest.mock import Mock, patch
from pellets import Pellet, PowerPellet, PelletGroup
from vector import Vector

pygame.init()

@pytest.fixture
def screen():
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def pellet():
    return Pellet(1, 1)

@pytest.fixture
def power_pellet():
    return PowerPellet(1, 1)

@pytest.fixture
def pellet_group(tmp_path):
    pellet_data = """X X X X X X X X X X X X X X X X X X X X X X X X X X X X
X X X X X X X X X X X X X X X X X X X X X X X X X X X X
X X X X X X X X X X X X X X X X X X X X X X X X X X X X
0 1 1 1 1 1 1 1 1 1 1 1 1 7 8 1 1 1 1 1 1 1 1 1 1 1 1 0
1 + . . . . + . . . . . + 3 3 + . . . . . + . . . . + 1
1 . 2 3 3 2 . 2 3 3 3 2 . 3 3 . 2 3 3 3 2 . 2 3 3 2 P 1"""
    p = tmp_path / "test_pellets.txt"
    p.write_text(pellet_data)
    return PelletGroup(str(p))