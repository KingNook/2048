import pygame
import typing

# breaks if run directly
from .grid import Grid
from . import colors, config_reader

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
            config_subpath: str = 'main'
        ):

        self.board = board

        self.properties = dict()
        self.grab_config(config_subpath)

        self.TEST_FONT = pygame.font.SysFont('Calibri', int(self.properties['tile_size']*0.6))

        self.setup_pg_to_coord()
        self.display = pygame.display.set_mode(self.properties['dimensions'], pygame.RESIZABLE)

    def grab_config(self, subpath) -> None:
        '''grabs config from main'''
        
        config = config_reader.load_config(file_name = subpath)

        self.properties = config['default_properties']
        self.settings = config['settings']
        
        self.update_properties()

    def update_properties(self) -> None:
        '''
        updates "dependent" properties

        note: may have to add minimum sizes if this turns out to be an issue
        (for now it seems it'll be fine for reasonable screen sizes)
        '''

        # we scale the size of ui elements off of the smaller dimension
        min_dim = min(self.properties['dimensions'])

        self.properties['border_radius'] = min_dim // self.settings['border_ratio']
        self.properties['tile_size'] = min_dim // self.settings['tile_ratio']
        self.properties['grid_line_width'] = min_dim // self.settings['grid_line_ratio']
        self.properties['grid_border_width'] = min_dim // self.settings['grid_border_ratio']

        self.properties['grid_size'] = self.properties['tile_size']*4 + self.properties['grid_line_width']*3 + self.properties['grid_border_width']*2
        self.properties['grid_left'] = (self.properties['dimensions'][0] - self.properties['grid_size']) // 2
        self.properties['grid_top'] = (self.properties['dimensions'][1] - self.properties['grid_size']) // 2

        self.properties['grid_centre'] = (
            self.properties['grid_size'] // 2,
            self.properties['grid_size'] // 2
        )

        self.update_test_font()

        self.setup_pg_to_coord()

    def setup_pg_to_coord(self) -> None:

        coord_to_pygame = lambda coord: (
            self.properties['grid_left'] + self.properties['grid_border_width'] + (self.properties['grid_line_width'] + self.properties['tile_size'])*coord[1],
            self.properties['grid_top'] + self.properties['grid_border_width'] + (self.properties['grid_line_width'] + self.properties['tile_size'])*coord[0]
        )

        # dictionary containing k-v pairs grid coordinate : pygame (pixel) coordinate
        self.coord_to_pg = dict()

        for x in range(4):
            for y in range(4):
                self.coord_to_pg[(x, y)] = coord_to_pygame((x, y))

    def update_test_font(self) -> None:
        self.TEST_FONT = pygame.font.SysFont('Calibri', int(self.properties['tile_size']*0.6))

    ## ===============
    ## DRAWING METHODS
    ## ===============

    def draw_grid(self) -> None:
        #layer 0
        self.draw_background()
        #layer 1
        self.draw_score_text()
        self.draw_tiles()
        #layer 2
        self.game_over_handler()

    def draw_background(self) -> None:
        '''se'''
        self.display.fill(colors.IVORY)
            
        # grid background
        self.draw_square(
            colors.TGRAY,
            self.properties['grid_left'], self.properties['grid_top'], 
            self.properties['grid_size']
        )

        self.draw_board_backdrop()

    def draw_board_backdrop(self) -> None:
        for pg_coord in self.coord_to_pg.values():
            pygame.draw.rect(
                self.display, colors.LGRAY,
                pygame.Rect(pg_coord[0], pg_coord[1], self.properties['tile_size'], self.properties['tile_size']),
                width = 0, border_radius = self.properties['border_radius']
            )


    def draw_tiles(self) -> None:
        for tile_coord, tile_value in self.board.tiles.items():
            tile_style = self.get_tile_style(tile_value)
            pg_coord = self.coord_to_pg[tile_coord]

            tile = self.draw_tile_base(
                tile_coord, tile_style
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
        # move condition outside
        if self.board.alive == False:

            game_over_surface = pygame.Surface(
                (self.properties['grid_size'], self.properties['grid_size']), pygame.SRCALPHA
            )

            # overlay
            pygame.draw.rect(
                game_over_surface, colors.GAME_OVER,
                game_over_surface.get_rect(), border_radius=self.properties['border_radius']
            )
            

            game_over_text = self.TEST_FONT.render(
                'Game Over', True, colors.DTEXT
            )

            text_rect = game_over_text.get_rect(center = self.properties['grid_centre'])

            game_over_surface.blit(game_over_text, text_rect)

            self.display.blit(game_over_surface, (self.properties['grid_left'], self.properties['grid_top']))

    def draw_tile_base(
            self,
            tile_coord: tuple,
            tile_style: colors.TileStyle
    ) -> pygame.rect.Rect:
        
        pg_coord = self.coord_to_pg[tile_coord]

        return self.draw_square(
            tile_style[0],
            pg_coord[0], pg_coord[1],
            self.properties['tile_size']
        )

    def draw_square(
            self,
            color: tuple,
            x: int, y: int,
            size: int
    ) -> pygame.rect.Rect:
        '''draws a pygame rectangle on self.display'''

        return pygame.draw.rect(
            self.display,
            color,
            pygame.Rect(
                x, y, size, size
            ),
            width = 0, border_radius = self.properties['border_radius']
        )



    ## ==================
    ## ADDITIONAL METHODS
    ## ==================

    def resize_handler(
            self,
            event
    ) -> None:
        self.properties['dimensions'] = (event.x, event.y)

        self.update_properties()
        self.draw_grid()

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
            pg_coords[0] + self.properties['tile_size'] // 2,
            pg_coords[1] + self.properties['tile_size'] // 2
        )