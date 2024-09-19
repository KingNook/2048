import numpy
import typing

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

from grid_objects import grid, renderer

pygame.init()

## ===========
## DEFINITIONS
## ===========

board = grid.Grid(4)
board.reset()

grid_renderer = renderer.GridRenderer(board)

## ==========
## GAME LOGIC
## ==========

def magnitude(vector: tuple) -> float:
    '''magnitude of 2d vector'''
    return numpy.sqrt(vector[0]**2 + vector[1]**2)

def handle_pygame_events(board, large_motion=[0, 0]):
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                alive = False

            elif event.key == K_UP or event.key == K_w:
                board.up()
            elif event.key == K_LEFT or event.key == K_a:
                board.left()
            elif event.key == K_DOWN or event.key == K_s:
                board.down()
            elif event.key == K_RIGHT or event.key == K_d:
                board.right()

            elif event.key == K_r and board.alive == False:
                board.reset()

            # for debugging purposes
            elif event.key == K_k:
                board.alive = not board.alive

        elif event.type == pygame.FINGERDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            large_motion = [0, 0]

        elif event.type == pygame.FINGERMOTION:
            if magnitude((event.dx, event.dy)) > 0.1:
                large_motion = [event.dx, event.dy]

        elif event.type == pygame.MOUSEMOTION:
            if magnitude(tuple(event.rel)) > 1:
                large_motion = list(event.rel)

        elif event.type == pygame.FINGERUP or event.type == pygame.MOUSEBUTTONUP:
            '''handle touch move'''

            if large_motion != [0, 0]:

                if abs(large_motion[0]) >= abs(large_motion[1]):

                    if large_motion[0] > 0:
                        board.right()

                    else:
                        board.left()

                else:
                    if large_motion[1] > 0:
                        board.down()

                    else:
                        board.up()

            large_motion = [0, 0]

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
    global alive, large_motion
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