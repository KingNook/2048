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

import colors

import grid_objects

pygame.init()

## =========
## CONSTANTS
## =========

def get_centre_coords(pg_coords):
    '''
    given pygame (pixel) coordinates for the top-left of a square, return the coordinates of the centre of the square
    '''

    return (
        pg_coords[0] + TILE_SIZE // 2,
        pg_coords[1] + TILE_SIZE // 2
    )

## =============
## ONE OFF STUFF
## =============

def coord_to_pygame(coord):
    '''converts (x, y) grid coord to pygame coords'''

    return (
        GRID_LEFT + GRID_BORDER_WIDTH + (GRID_LINE_WIDTH + TILE_SIZE)*coord[1],
        GRID_TOP + GRID_BORDER_WIDTH + (GRID_LINE_WIDTH + TILE_SIZE)*coord[0]
    )

# dictionary containing k-v pairs grid coordinate : pygame (pixel) coordinate
COORD_TO_PG = dict()

for x in range(4):
    for y in range(4):
        COORD_TO_PG[(x, y)] = coord_to_pygame((x, y))

## ===========
## DEFINITIONS
## ===========

grid = grid_objects.grid.Grid(4)
grid.reset()

## ==========
## GAME LOGIC
## ==========

def handle_pygame_events(grid):
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

            elif event.key == K_r and grid.alive == False:
                grid.reset_grid()

            # for debugging purposes
            elif event.key == K_k:
                grid.alive = not grid.alive

        elif event.type == QUIT:
            alive = False
            sys.exit()

## ================
## RENDER FUNCTIONS
## ================

def draw_background():
    '''se'''
    screen.fill(colors.IVORY)
        
    # grid background
    pygame.draw.rect(
        screen, colors.TGRAY,
        pygame.Rect(GRID_LEFT, GRID_TOP, GRID_SIZE, GRID_SIZE),
        width = 0, border_radius = BORDER_RADIUS
    )

    # empty tiles
    for pg_coord in COORD_TO_PG.values():
        pygame.draw.rect(
            screen, colors.LGRAY,
            pygame.Rect(pg_coord[0], pg_coord[1], TILE_SIZE, TILE_SIZE),
            width = 0, border_radius = BORDER_RADIUS
        )

    return True

def draw_score_text():
    '''se'''
    score_text = TEST_FONT.render(
        str(grid.score), True, colors.AFW
    )

    screen.blit(score_text, (10, 10))

    return True

def draw_tiles(grid):
    for tile_coord, tile_value in grid.tiles.items():

        # replace with match case? seems better. or perhaps a regular check
        try:
            tile_style = colors.TILE_STYLES[tile_value]
        except KeyError:
            tile_style = colors.DEFAULT_STYLE

        pg_coord = coord_to_pygame(tile_coord)

        # draw tile
        tile = pygame.draw.rect(
            screen, tile_style[0],
            pygame.Rect(pg_coord[0], pg_coord[1], TILE_SIZE, TILE_SIZE),
            width = 0, border_radius = BORDER_RADIUS
        )

        tile_text = TEST_FONT.render(
            str(2**tile_value), True, tile_style[1]
        )

        text_rect = tile_text.get_rect(center = get_centre_coords(pg_coord))

        screen.blit(tile_text, text_rect)

def game_over_handler():
    if grid.alive == False:

        game_over_surface = pygame.Surface(
            (GRID_SIZE, GRID_SIZE), pygame.SRCALPHA
        )

        # overlay
        pygame.draw.rect(
            game_over_surface, colors.GAME_OVER,
            game_over_surface.get_rect(), border_radius=BORDER_RADIUS
        )
        

        game_over_text = TEST_FONT.render(
            'Game Over', True, colors.DTEXT
        )

        text_rect = game_over_text.get_rect(center = GRID_CENTRE)

        game_over_surface.blit(game_over_text, text_rect)

        screen.blit(game_over_surface, (GRID_LEFT, GRID_TOP))

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

        handle_pygame_events(grid)

        ## ======
        ## RENDER
        ## ======

        draw_background()
        draw_score_text()
        draw_tiles(grid)
        game_over_handler()

        pygame.display.flip()

        await asyncio.sleep(0)
        
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    asyncio.run(main())