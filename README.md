uh i kinda feel like coding 2048 i guess
should be a quick project - i give this 2 weeks of serious effort

## day 1
- create repo + first files

## day 2
- create grid
- make methods to add, combine cells
- change to make cells a dictionary
- begin to implement move left (press left key)
- consider changing implementation of tiles to set / multiply instead of add

- changed my mind again on how to implement this
- make a list of all the tiles in the row (not including spaces)
- combine all pairs
- return new list as row

- probably should add typeErrors at some point
- ong probably woulda been better to just use numpy arrays but hey we're here now

- eod: now has a move-left function and a repr
- further plans: implement movement in other directions, automagically adding new tiles, clean up code
- next steps: add actual controls and potentially a score? then it's just ui work

## day 3 (short day)
- finish up move_left and move_right
- want to make a move_up and move_down using same code (DRY etc)
- will copy code over, want to find nice solution that doesn't involve copy-pasted code
- ok so move_up and move_down actually work now
- add functionality to add random cell

- eod: game now functionally works and finishes when 'attempt to add cell but no free cells' (ie move made and no free cells)
- breaks when: move is made but nothing changes. not sure why (since code should still function) but worth looking into
- next steps: prettify ie make gui

## day 4 (even shorter day)
- fixed crashing issue (forgot to implement part of move_horizontal and move_vertical lol, done now though)

- todo: add proper game end condition (when add random cell fails, check to see if there are any valid moves), prettify, make gui

## day 5
- no longer adds a new tile when invalid move is made
- now ends the game when there are no valid moves

- would like to remove tile class and replace with ints but am worried that the class may come in handy later for rendering so i'll keep it for now then once the rendering is done, if that doesn't use the tile rendering i'll remove the class

## day 6
- made pygame window, moved to using pygame for key handling
- removed Tile class, have broken something (move_right specifically seems to be broken for some reason) - will have to figure out how to fix at some point
- ok the fix now works; turns out the bug was there all along lol (i was flipping the row when doing 'reversed' movements)