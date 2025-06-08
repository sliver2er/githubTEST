# tetris.py
import pygame
import random
from shapes import SHAPES
from config import *

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape[1]
        self.rotation = 0

    def image(self):
        return self.shape[0][self.rotation % len(self.shape[0])]

    def rotate(self):
        self.rotation += 1


def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid


def convert_shape_format(piece):
    positions = []
    shape = piece.image()

    for i, line in enumerate(shape):
        for j, column in enumerate(line):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    return positions


def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(COLS) if grid[y][x] == BLACK] for y in range(ROWS)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(5, 0, random.choice(SHAPES))


def clear_rows(grid, locked):
    inc = 0
    for i in range(ROWS - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            inc += 1
            index = i
            for j in range(COLS):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)
    return inc