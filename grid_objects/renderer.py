import pygame
import typing

from grid import Grid
import colors

from dataclasses import dataclass, astuple

@dataclass
class Coord:
    x: int
    y: int

class GridRenderer:
    '''
    contains methods used for rendering the grid into a pygame window

    board : Grid
    '''
    
    ## =====
    ## SETUP
    ## =====

    def __init__(
            self,
            board: Grid,
        ):

        self.board = board
        board.reset()

        self.grab_config()

        # add separate config file and grab these on init
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

        self.display = pygame.display.set_mode(DIMENSIONS)

    def grab_config(self, path):
        '''dummy method, will grab config variables when i figure out how i want to format them'''
        pass

    def setup_pg_to_coord(self) -> None:

        coord_to_pygame = lambda coord: (
            self.GRID_LEFT + self.GRID_BORDER_WIDTH + (self.GRID_LINE_WIDTH + self.TILE_SIZE)*coord[1],
            self.GRID_TOP + self.GRID_BORDER_WIDTH + (self.GRID_LINE_WIDTH + self.TILE_SIZE)*coord[0]
        )

        # dictionary containing k-v pairs grid coordinate : pygame (pixel) coordinate
        self.COORD_TO_PG = dict()

        for x in range(4):
            for y in range(4):
                self.COORD_TO_PG[(x, y)] = coord_to_pygame((x, y))


    ## =======
    ## METHODS
    ## =======

    def draw_tiles(self):
        for tile_coord, tile_value in self.board.tiles.items():

            # replace with match case? seems better. or perhaps a regular check (or separate function)

            tile_style = self.get_tile_style()
            
            pg_coord = self.COORD_TO_PG(tile_coord)

            # draw tile
            tile = pygame.draw.rect(
                self.display, tile_style[0],
                pygame.Rect(pg_coord[0], pg_coord[1], self.TILE_SIZE, self.TILE_SIZE),
                width = 0, border_radius = self.BORDER_RADIUS
            )

            tile_text = self.TEST_FONT.render(
                str(2**tile_value), True, tile_style[1]
            )

            text_rect = tile_text.get_rect(center = self.get_centre_coords(pg_coord))

            self.display.blit(tile_text, text_rect)

    def get_tile_style(
            self,
            tile_value: int
    ):
        try:
            tile_style = colors.TILE_STYLES[tile_value]
        except KeyError:
            tile_style = colors.DEFAULT_STYLE

        return tile_style

    def get_centre_coords(
            self,
            pg_coords: Coord
    ):
        '''
        given pygame (pixel) coordinates for the top-left of a square, return the coordinates of the centre of the square
        '''

        return (
            pg_coords[0] + self.TILE_SIZE // 2,
            pg_coords[1] + self.TILE_SIZE // 2
        )