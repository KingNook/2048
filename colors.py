import pygame

'''
hex codes for various colors
names and hex codes from https://coolors.co
'''

def from_hex(color):
    '''convert 6-digit hex code to (r, g, b) for use in pygame'''

    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:], 16))

# constants
FONT_SIZE = 32

# colors
LGRAY = from_hex('9C969A') # lighter taupe gray // unfilled boxes
DTEXT = from_hex('544F52') # davy's gray // dark text
TGRAY = from_hex('8B8589') # taupe gray // gridlines
LTEXT = from_hex('FFFAF0') # floral white // light text
IVORY = from_hex('FFFEEB') # background
AFW = from_hex('E9E9EC') # anti-flash white // 2
VANILLA = from_hex('FFFBAD') # 4
JASMINE = from_hex('F6CE79') # 8
OPEEL = from_hex('FFA000') # orange peel // 16
CRORANGE = from_hex('FF4F00') # crayola orange // 32
ASORANGE = from_hex('FF4F00') # aerospace orange // 64

DTILE = from_hex('02111B') # default tile color (for tiles larger than defined in palette)

# map each tile <value> : (color, font_color, font_size)
TILE_STYLES = {
    1:(AFW, DTEXT, FONT_SIZE),
    2:(VANILLA, DTEXT, FONT_SIZE),
    3:(JASMINE, LTEXT, FONT_SIZE),
    4:(OPEEL, LTEXT, FONT_SIZE),
    5:(CRORANGE, LTEXT, FONT_SIZE),
    6:(ASORANGE, LTEXT, FONT_SIZE)
}

DEFAULT_STYLE = (DTILE, LTEXT, FONT_SIZE)