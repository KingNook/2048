import numpy
import pygame
import sys
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_r,
    K_k,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

import asyncio

import grid_objects.colors as colors

import grid_objects
import grid_objects.renderer

pygame.init()

## ===========
## DEFINITIONS
## ===========

board = grid_objects.grid.Grid(4)
board.reset()

grid_renderer = grid_objects.renderer.GridRenderer(board)

## ==========
## GAME LOGIC
## ==========

def handle_pygame_events(board):
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                alive = False

            elif event.key == K_UP or event.key == K_w:
                board.move_up()
            elif event.key == K_LEFT or event.key == K_a:
                board.move_left()
            elif event.key == K_DOWN or event.key == K_s:
                board.move_down()
            elif event.key == K_RIGHT or event.key == K_d:
                board.move_right()

            elif event.key == K_r and board.alive == False:
                board.reset()

            # for debugging purposes
            elif event.key == K_k:
                board.alive = not board.alive

        elif event.type == QUIT:
            alive = False
            sys.exit()

## ================
## RENDER FUNCTIONS
## ================

## ==========
## GAME CYCLE
## ==========

alive = True
async def main():
    global alive, grid, screen
    global DIMENSIONS, BORDER_RADIUS, TILE_SIZE, GRID_LINE_WIDTH, GRID_BORDER_WIDTH, GRID_SIZE, GRID_LEFT, GRID_TOP, TEST_FONT, COORD_TO_PG

    while alive:

        ## ============
        ## KEY HANDLING
        ## ============

        handle_pygame_events(grid_renderer.board)

        ## ======
        ## RENDER
        ## ======

        grid_renderer.draw_background()
        grid_renderer.draw_score_text()
        grid_renderer.draw_tiles()
        grid_renderer.game_over_handler()

        pygame.display.flip()

        await asyncio.sleep(0)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    asyncio.run(main())

    print('runnin')