import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

import colors

import grid_objects

pygame.init()

## =========
## CONSTANTS
## =========
DIMENSIONS = (800, 600)
TEST_FONT = pygame.font.SysFont('Comic Sans MS', 10)

screen = pygame.display.set_mode(DIMENSIONS)

## ===========
## DEFINITIONS
## ===========

grid = grid_objects.Grid(4)
grid.add_random_cell()

## ==========
## GAME CYCLE
## ==========

alive = True
while alive:

    ## ============
    ## KEY HANDLING
    ## ============

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                alive = False

            elif event.key == K_UP or event.key == K_w:
                grid.move_up()
            elif event.key == K_LEFT or event.key == K_a:
                grid.move_left()
            elif event.key == K_DOWN or event.key == K_s:
                grid.move_down()
            elif event.key == K_RIGHT or event.key == K_d:
                grid.move_right()

        elif event.type == QUIT:
            alive = False

    ## ======
    ## RENDER
    ## ======

    screen.fill(colors.IVORY)

    # ---------------
    # DRAW BACKGROUND
    # ---------------

    # ----------
    # DRAW TILES
    # ----------
    
    for tile_coord, tile_value in grid.tiles.items():
        tile_style = colors.TILE_STYLES[tile_value]
        # NEED TO REPLACE LEFT_TOP TO THE CORRECT TOP LEFT COORD (DONE BY GRID COORD TO PYGAME COORD)
        pygame.draw.rect(
            screen, tile_style[0],
            [50, 100, colors.TILE_SIZE, colors.TILE_SIZE], 0
        ) # [left, top, width, height]


    pygame.display.flip()