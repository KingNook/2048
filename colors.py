'''
hex codes for various colors
'''

def hex_to_pygame(color):
    '''convert 6-digit hex code to (r, g, b) for use in pygame'''

    return (color[0:2], color[2:4], color[4:])

IVORY = hex_to_pygame('FFFEEB')
