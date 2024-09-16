import pygame
import typing

from .grid import Grid
import colors

from dataclasses import dataclass

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

        self.grab_config('<placeholder>')

        # add separate config file and grab these on init
        self.DIMENSIONS = (800, 600)

        self.BORDER_RADIUS = 10

        self.TILE_SIZE = 80
        self.GRID_LINE_WIDTH = 15
        self.GRID_BORDER_WIDTH = 15
        self.GRID_SIZE = self.TILE_SIZE*4 + self.GRID_LINE_WIDTH*3 + self.GRID_BORDER_WIDTH*2

        self.GRID_LEFT = (self.DIMENSIONS[0] - self.GRID_SIZE) // 2
        self.GRID_TOP = (self.DIMENSIONS[1] - self.GRID_SIZE) // 2

        self.TEST_FONT = pygame.font.SysFont('Calibri', int(self.TILE_SIZE*0.6))

        self.GRID_CENTRE = (
            self.GRID_SIZE // 2,
            self.GRID_SIZE // 2
        )

        self.setup_pg_to_coord()

        self.display = pygame.display.set_mode(self.DIMENSIONS)

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


    ## ===============
    ## DRAWING METHODS
    ## ===============

    def draw_background(self) -> None:
        '''se'''
        self.display.fill(colors.IVORY)
            
        # grid background
        pygame.draw.rect(
            self.display, colors.TGRAY,
            pygame.Rect(self.GRID_LEFT, self.GRID_TOP, self.GRID_SIZE, self.GRID_SIZE),
            width = 0, border_radius = self.BORDER_RADIUS
        )

        # empty tiles
        for pg_coord in self.COORD_TO_PG.values():
            pygame.draw.rect(
                self.display, colors.LGRAY,
                pygame.Rect(pg_coord[0], pg_coord[1], self.TILE_SIZE, self.TILE_SIZE),
                width = 0, border_radius = self.BORDER_RADIUS
            )

        return True

    def draw_tiles(self) -> None:
        for tile_coord, tile_value in self.board.tiles.items():

            # replace with match case? seems better. or perhaps a regular check (or separate function)

            tile_style = self.get_tile_style(tile_value)
            
            pg_coord = self.COORD_TO_PG[tile_coord]

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

    def draw_score_text(self) -> None:
        '''se'''
        score_text = self.TEST_FONT.render(
            str(self.board.score), True, colors.AFW
        )

        self.display.blit(score_text, (10, 10))

        return True
    
    def game_over_handler(self) -> None:
        if self.board.alive == False:

            game_over_surface = pygame.Surface(
                (self.GRID_SIZE, self.GRID_SIZE), pygame.SRCALPHA
            )

            # overlay
            pygame.draw.rect(
                game_over_surface, colors.GAME_OVER,
                game_over_surface.get_rect(), border_radius=self.BORDER_RADIUS
            )
            

            game_over_text = self.TEST_FONT.render(
                'Game Over', True, colors.DTEXT
            )

            text_rect = game_over_text.get_rect(center = self.GRID_CENTRE)

            game_over_surface.blit(game_over_text, text_rect)

            self.display.blit(game_over_surface, (self.GRID_LEFT, self.GRID_TOP))

    ## ==================
    ## ADDITIONAL METHODS
    ## ==================

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