# main.py
import pygame
import sys
from tetris import create_grid, get_shape, convert_shape_format, valid_space, check_lost, clear_rows
from config import *

pygame.font.init()
FONT = pygame.font.SysFont('comicsans', 30)

def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for y in range(ROWS):
        pygame.draw.line(surface, WHITE, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
    for x in range(COLS):
        pygame.draw.line(surface, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)
    draw_grid(surface, grid)

    score_text = FONT.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

    pygame.display.update()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            score += clear_rows(grid, locked_positions) * 10
            change_piece = False

        draw_window(screen, grid, score)

        if check_lost(locked_positions):
            run = False

    pygame.quit()

if __name__ == '__main__':
    main()
