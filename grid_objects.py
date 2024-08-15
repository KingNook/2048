import numpy as np

def merge_two_dicts(a, b):

    c = a.copy()
    c.update(b)

    return c

def list_to_row(lst, row):
    new_row = dict()
    for col in range(len(lst)):
        new_row[(row, col)] = lst[col]

    return new_row

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
    
    def add_cell(self, row, col):
        new_cell = (row, col)

        # check cell is empty
        if new_cell in self.tiles.keys():
            raise KeyError
        
        # set cell value to 1 (or whatever initial cell value we want - can add randomness later)
        self.tiles[new_cell] = Tile(self.initial_cell_value)

    def move_left(self):
        '''
        say we press the left button
        we need to move all the tiles as far to the left as possible
        start from the left side
        '''

        # replace stuff in here, replace tiles with new_tiles at the end (less memory efficient, can optimise later)
        new_tiles = dict()
        
        for row in range(self.size):
            current_row = []

            for col in range(self.size):

                cell = (row, col)
                if cell in self.tiles.keys():
                    current_row.append(self.tiles[cell])
            
            # now we combine   
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

            # then create row dict from new_row
            new_row_tiles = list_to_row(new_row, row)
            new_tiles.update(new_row_tiles)

            

        self.tiles = new_tiles