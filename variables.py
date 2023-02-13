#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

# APPLE
APPLE_IMAGES = ['images\gem.png', 'images\gem2.png']

# SNAKE
BLOCK_SIZE = 25
DEFAULT_SNAKE_BLOCK_PATH = "images/block.jpg"
INIT_LENGTH = 1

# WINDOW
WINDOW_WIDTH = 24 * BLOCK_SIZE
WINDOW_HEIGHT = 24 * BLOCK_SIZE
BACKGROUND_COLOR = (233, 196, 106)

# GAME
FPS = 20
GAME_NAME = 'AI Snake'
BACKGROUND_IMAGE_PATH = "images/yellow_background.jpg"
DATA_FILE_PATH = 'data/highest_score.txt'
LEFT_CORNER_COORDINATES = (0, 0)

# DIRECTIONS
class Directions(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


