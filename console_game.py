import numpy as np

from pynput import keyboard
from grid_objects import Grid

# 4x4 grid
grid = Grid(4)
# grid.tiles = {(0, 3): 1, (0, 2): 2, (0, 1): 5, (0, 0): 2, (1, 3): 1, (1, 2): 2, (1, 1): 3, (1, 0): 2, (2, 3): 1, (2, 2): 3, (2, 1): 2, (2, 0): 1, (3, 3): 1, (3, 2): 2, (3, 1): 3, (3, 0): 1}
grid.add_random_cell()

print(grid)

def on_press(key):
    try:
        if key.char == 'w':
            grid.move_up()
        elif key.char == 'a':
            grid.move_left()
        elif key.char == 's':
            grid.move_down()
        elif key.char == 'd':
            grid.move_right()

    except AttributeError:
        if key == keyboard.Key.up:
            grid.move_up()
        elif key == keyboard.Key.left:
            grid.move_left()
        elif key == keyboard.Key.down:
            grid.move_down()
        elif key == keyboard.Key.right:
            grid.move_right()

def on_release(key):

    print(grid)
    
    if key == keyboard.Key.esc:
        # Stop listener
        return False
        
    
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()