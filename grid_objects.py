import numpy as np

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
        
    
class Grid:
    '''
    2048 (n x n grid)
    '''

    def __init__(self, size):

        self.size = size

        self.grid_points = set([(i, j) for i in range(size) for j in range(size)])
        tile_list = [Tile(0)]*size**2

        self.grid = dict(zip(
            self.grid_points, tile_list
        ))

        self.filled_cells = set()

        self.initial_cell_value = 1

    @property
    def empty_cells(self):
        return self.grid_points - self.filled_cells
    
    def add_cell(self, row, col):
        new_cell = (row, col)

        # check cell is empty
        if new_cell in self.filled_cells:
            raise KeyError
        
        # set cell value to 1 (or whatever initial cell value we want - can add randomness later)
        self.grid[new_cell] += self.initial_cell_value
        self.filled_cells.add(new_cell)

    def move_left(self):
        '''
        say we press the left button
        we need to move all the tiles as far to the left as possible
        start from the left side
        '''
        
        for row in range(self.size):
            new_row = []

            for col in range(1, self.size):
                '''
                we don't need to do anything to the first one
                we want to move each cell to the left
                '''

                cell = (row, col)
                if cell in self.filled_cells:
                    '''
                    we need to check all the cells to the left of this
                    '''
