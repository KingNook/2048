import numpy as np
import random

def merge_two_dicts(a, b):

    c = a.copy()
    c.update(b)

    return c

class Tile:
    '''
    tile in 2048 - value should be a power of 2
    '''


    def __init__(self, value):

        self.value = value

    def __eq__(self, other):
        '''where the other would also be a tile'''

        if other.value == self.value:
            return True

        return False
    
    def __repr__(self):
        return str(self.value)
    
    def __add__(self, num):
        if type(num) == int:
            return Tile(self.value + num)
        
        if type(num) == Tile:
            return Tile(self.value + num.value)
        
    def __mul__(self, other):
        if type(other) == int:
            return Tile(self.value * other)
        
    def __rmul__(self, other):
        if type(other) == int:
            return Tile(self.value * other)
        
    
class Grid:
    '''
    2048 (n x n grid)
    '''

    def __init__(self, size):

        self.size = size

        # will be coord: Tile
        self.tiles = dict()

        self.initial_cell_value = 2

    def __repr__(self):

        grid = np.zeros((self.size, self.size))
        for cell in self.tiles.keys():
            grid[*cell] = self.tiles[cell].value

        return grid.__repr__()
    
    ## MISC FUNCTIONS

    def list_to_row(self, lst, row, reversed=False):
        new_row = dict()
        for col in range(len(lst)):
            if reversed:
                new_row[(row, self.size - 1 - col)] = lst[col]
            else:
                new_row[(row, col)] = lst[col]

        return new_row
    
    def list_to_col(self, lst, col, reversed=False):
        new_col = dict()
        for row in range(len(lst)):
            if reversed:
                new_col[(self.size - 1 - row, col)] = lst[row]
            else:
                new_col[(row, col)] = lst[row]

        return new_col
    
    ## ====== 
    ## CHECKS
    ## ======

    def is_alive(self):
        '''check to see if any viable moves are possible.'''


    ## =========
    ## ADD TILES
    ## =========

    def add_cell(self, row, col):
        new_cell = (row, col)

        # check cell is empty
        if new_cell in self.tiles.keys():
            raise KeyError
        
        # set cell value to 1 (or whatever initial cell value we want - can add randomness later)
        self.tiles[new_cell] = Tile(self.initial_cell_value)

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
            raise NotImplementedError
        
        choices = list(set(choices))
        choice = choices[0]

        self.tiles[choice] = Tile(self.initial_cell_value)
        
        return self.tiles
        

    ## ========
    ## MOVEMENT
    ## ========

    def condense_row(self, arr):
        '''condenses as if moving to the left, can reverse the array_like object beforehand if needed'''

    def move_vertical(self, reversed=False):
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

            if reversed:
                current_col = current_col[::-1]
            
            # now we combine   
            new_col = []

            pointer = 0
            while pointer < len(current_col):

                if pointer != len(current_col) - 1:
                    if current_col[pointer] == current_col[pointer + 1]:
                        new_col.append(current_col[pointer] * 2)
                        pointer += 2
                    else:
                        new_col.append(current_col[pointer])
                        pointer += 1
                else:
                    new_col.append(current_col[pointer])
                    pointer += 1

            if reversed:
                new_col = new_col[::-1]

            # then create row dict from new_row
            new_row_tiles = self.list_to_col(new_col, col, reversed)
            new_tiles.update(new_row_tiles)

        self.tiles = new_tiles
        self.add_random_cell()
        return self.tiles

    def move_horizontal(self, reversed=False):
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

            if reversed:
                current_row = current_row[::-1]
            
            new_row = []

            pointer = 0
            while pointer < len(current_row):

                if pointer != len(current_row) - 1:
                    if current_row[pointer] == current_row[pointer + 1]:
                        new_row.append(current_row[pointer] * 2)
                        pointer += 2
                    else:
                        new_row.append(current_row[pointer])
                        pointer += 1
                else:
                    new_row.append(current_row[pointer])
                    pointer += 1

            if reversed:
                new_row = new_row[::-1]

            # then create row dict from new_row
            new_row_tiles = self.list_to_row(new_row, row, reversed)
            new_tiles.update(new_row_tiles)

            

        self.tiles = new_tiles
        self.add_random_cell()
        return self.tiles
    
    def move_left(self):
        return self.move_horizontal(reversed=False)
    
    def move_right(self):
        return self.move_horizontal(reversed=True)

    def move_up(self):
        return self.move_vertical(reversed=False)
    
    def move_down(self):
        return self.move_vertical(reversed=True)