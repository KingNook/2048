import pygame

import colors

class GridRenderer:
    '''
    contains methods used for rendering the grid into a pygame window

    board : Grid
    '''

    def __init__(self, board):

        self.board = board
        board.reset()

        DIMENSIONS = (800, 600)

        BORDER_RADIUS = 10

        TILE_SIZE = 80
        GRID_LINE_WIDTH = 15
        GRID_BORDER_WIDTH = 15
        GRID_SIZE = TILE_SIZE*4 + GRID_LINE_WIDTH*3 + GRID_BORDER_WIDTH*2

        GRID_LEFT = (DIMENSIONS[0] - GRID_SIZE) // 2
        GRID_TOP = (DIMENSIONS[1] - GRID_SIZE) // 2

        TEST_FONT = pygame.font.SysFont('Calibri', int(TILE_SIZE*0.6))
        screen = pygame.display.set_mode(DIMENSIONS)

        GRID_CENTRE = (
            GRID_SIZE // 2,
            GRID_SIZE // 2
        )

    def draw_tiles(self):
        for tile_coord, tile_value in self.board.tiles.items():

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