import pytest
import pygame
from unittest.mock import Mock, patch
from nodes import Node, NodeGroup
from constants import *

pygame.init()

@pytest.fixture
def screen():
    return pygame.display.set_mode((800, 600))

@pytest.fixture
def node():
    return Node(10, 20)

@pytest.fixture
def entity():
    mock_entity = Mock()
    mock_entity.name = PACMAN
    return mock_entity

@pytest.fixture
def node_group(tmp_path):
    level_data = "X X X X\nX + . X\nX P - X\nX X X X"
    p = tmp_path / "test_level.txt"
    p.write_text(level_data)
    return NodeGroup(str(p))