import numpy as np
import random
    
class Grid:
    '''
    2048 (n x n grid)
    '''

    ## ===============
    ## CLASS FUNCTIONS
    ## ===============

    def __init__(self, size, ltc=0.2):
        '''
        size = size of grid (nxn square grid)
        ltc = 'large tile chance' ie chance of spawning a 4 tile instead of a 2
        '''

        self.size = size

        # will be coord: Tile
        self.tiles = dict()

        self.score = 0

        self.initial_cell_value = 1
        self.large_tile_chance = ltc

        self.alive = True

    def __repr__(self):

        grid = np.zeros((self.size, self.size))
        for cell in self.tiles.keys():
            grid[*cell] = self.tiles[cell]

        return grid.__repr__()
    
    def reset_grid(self):
        
        self.tiles = dict()
        self.score = 0
        
        self.alive = True
        self.add_random_cell()
        self.add_random_cell()

        return self.tiles
    
    ## ==============
    ## MISC FUNCTIONS
    ## ==============

    def list_to_row(self, lst, row, reversed=False):
        new_row = dict()
        for col in range(len(lst)):
            if reversed:
                new_row[(row, self.size - len(lst) + col)] = lst[col]
            else:
                new_row[(row, col)] = lst[col]

        return new_row
    
    def list_to_col(self, lst, col, reversed=False):
        new_col = dict()
        for row in range(len(lst)):
            if reversed:
                new_col[(self.size - len(lst) + row, col)] = lst[row]
            else:
                new_col[(row, col)] = lst[row]

        return new_col
    
    ## ====== 
    ## CHECKS
    ## ======

    def any_valid_moves(self):
        '''check to see if any viable moves are possible; returns bool'''
        # return not self.move_down(update=False) or self.move_left(update=False) or self.move_up(update=False) or self.move_right(update=False)
        # ok so i could just add a requirement for all tiles to be full first but this is 

        up_possible = self.move_up(update=False)

        if self.move_up(update=False):
            return True
        elif self.move_left(update=False):
            return True
        elif self.move_down(update=False):
            return True
        elif self.move_right(update=False):
            return True
        else:
            print('no valid moves')
            print(self.__repr__())
            return False
        

    ## =========
    ## ADD TILES
    ## =========

    def new_tile_size(self):
        '''
        returns either initial_cell_value or double that depending on self.large_tile_chance
        '''

        p = random.random()
        
        if p <= self.large_tile_chance:
            return self.initial_cell_value + 1
        else:
            return self.initial_cell_value

    def add_cell(self, row, col):
        '''
        note this is not used anymore in the code, but i have left it here for debugging purposes
        '''

        new_cell = (row, col)

        # check cell is empty
        if new_cell in self.tiles.keys():
            raise KeyError
        
        # set cell value to 1 (or whatever initial cell value we want - can add randomness later)
        self.tiles[new_cell] = self.new_tile_size()

    def get_empty_cells(self):

        filled_cells = self.tiles.keys()
        empty_cells = []

        for row in range(self.size):
            for col in range(self.size):
                if not (row, col) in filled_cells:
                    empty_cells.append((row, col))

        return empty_cells
    
    def add_random_cell(self):
        '''fill random empty cell with a cell of value <self.initial_cell_value>'''
        choices = self.get_empty_cells()

        if len(choices) == 0:
            # should replace with more descriptive exception
            raise NotImplementedError
        
        choice = random.choice(list(choices))

        self.tiles[choice] = self.new_tile_size()
        
        return self.tiles
        

    ## ============
    ## GRID UPDATES
    ## ============

    def condense_row(self, arr, reversed=False, update_score=True):
        '''condenses as if moving to the left, can reverse the array_like object beforehand if needed'''

        if reversed:
            old_arr = arr[::-1]
        else:
            old_arr = arr

        new_arr = []
        pointer = 0
        while pointer < len(old_arr):

            if pointer != len(old_arr) - 1:
                if old_arr[pointer] == old_arr[pointer + 1]:
                    new_arr.append(old_arr[pointer] + 1)
                    pointer += 2
                    if update_score:
                        self.score += 2**new_arr[-1]
                else:
                    new_arr.append(old_arr[pointer])
                    pointer += 1
            else:
                new_arr.append(old_arr[pointer])
                pointer += 1

        if reversed:
            new_arr = new_arr[::-1]
        
        return new_arr

    def move_vertical(self, reversed=False, update_score=True):
        '''
        by default moves tiles down

        reversed=True moves tiles up
        '''

        new_tiles = dict()
        
        for col in range(self.size):
            current_col = []

            for row in range(self.size):

                cell = (row, col)
                if cell in self.tiles.keys():
                    current_col.append(self.tiles[cell])
            
            # now we combine   
            new_col = self.condense_row(current_col, reversed=reversed, update_score=update_score)

            # then create row dict from new_row
            new_row_tiles = self.list_to_col(new_col, col, reversed)
            new_tiles.update(new_row_tiles)

        return new_tiles

    def move_horizontal(self, reversed=False, update_score=True):
        '''
        by default this moves tiles left

        reversed=True moves tiles right
        '''

        new_tiles = dict()
        
        for row in range(self.size):
            current_row = []

            for col in range(self.size):

                cell = (row, col)
                if cell in self.tiles.keys():
                    current_row.append(self.tiles[cell])
            
            # now we combine   
            new_row = self.condense_row(current_row, reversed, update_score)

            # then create row dict from new_row
            new_row_tiles = self.list_to_row(new_row, row, reversed)
            new_tiles.update(new_row_tiles)

        return new_tiles
    
    def update_grid(self, tile_set):
        '''updates and adds new tile if there is a change, otherwise returns False'''
        if tile_set != self.tiles:
            self.tiles = tile_set
            self.add_random_cell()

            valid_moves = self.any_valid_moves()
            if valid_moves:
                return True
            else:
                self.alive = False
        else:
            return False
            
    
    def move_left(self, update=True):
        '''
        makes left move

        if update = True, this updates self.tiles and adds a tile if there is a change
        
        if update = False, this just returns True / False depending on whether the grid changes or not
        '''
        new_grid = self.move_horizontal(reversed=False)

        if update == True:
            return self.update_grid(new_grid)
        else:
            return self.tiles != new_grid
    
    def move_right(self, update=True):

        new_grid = self.move_horizontal(reversed=True)

        if update == True:
            return self.update_grid(new_grid)
        else:
            return self.tiles != new_grid

    def move_up(self, update=True):

        new_grid = self.move_vertical(reversed=False)

        if update == True:
            return self.update_grid(new_grid)
        else:
            return self.tiles != new_grid
    
    def move_down(self, update=True):

        new_grid = self.move_vertical(reversed=True)

        if update == True:
            return self.update_grid(new_grid)
        else:
            return self.tiles != new_grid