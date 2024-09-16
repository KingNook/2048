import pygame

import colors
from grid_objects import Grid

class GridRenderer:
    '''
    contains methods used for rendering the grid into a pygame window

    grid : type Grid from grid_objects
    '''

    def __init__(self, grid):

        self.grid = grid

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