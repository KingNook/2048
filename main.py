import numpy as np

from grid_objects import Grid, Tile

# 4x4 grid
grid = Grid(4)

grid.add_cell(1, 3)
grid.add_cell(1, 2)

print(grid)

grid.move_left()

print(grid)