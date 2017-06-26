'''Module for creating shapes for use with a Surface instance

CLASSES
-------
Shape: UNIMPLEMENTED

FUNCTIONS
---------
line: UNIMPLEMENTED
polyline: UNIMPLEMENTED
arrow: UNIMPLEMENTED
polyarrow: UNIMPLEMENTED
square: UNIMPLEMENTED
rect: UNIMPLEMENTED
arc: UNIMPLEMENTED
circle: UNIMPLEMENTED
ellipse: UNIMPLEMENTED
bezier: UNIMPLEMENTED
bezier_arrow: UNIMPLEMENTED
regular_ngon: UNIMPLEMENTED
polygon: UNIMPLEMENTED
'''

__author__ = 'Patrick Mende'
__version__ = '0.1'

from itertools import chain

import cairocffi as cairo

class Shape(object):
    '''Objects used to draw on surfaces

    Attributes
    ----------
    '''

    VALID_KWARGS = {
        'fill', 'f', 'stroke_color', 's_c', 'outline_color', 'ol_c',
        'stroke_linewidth', 's_lw', 'outline_width', 'ol_w',
        'stroke_linestyle', 's_ls', 'stroke_cap', 's_cap', 'conn_style'
    }

    def __init__(self):
        pass

    def __setattr__(self, attr, value):
        if attr in self.VALID_KWARGS:
            super().__setattr__(attr, value)
        else:
            raise AttributeError('Shape has no attribute {}'.format(attr))

class ShapeGroup(object):
    '''
    '''

    def __init__(self):
        pass

def line():
    '''
    '''

    pass

def polyline():
    '''
    '''

    pass

def arrow():
    '''
    '''

    pass

def polyarrow():
    '''
    '''

    pass

def square():
    '''
    '''

    pass

def rect():
    '''
    '''

    pass

def arc():
    '''
    '''

    pass

def circle():
    '''
    '''

    pass

def ellipse():
    '''
    '''

    pass

def bezier():
    '''
    '''

    pass

def bezier_arrow():
    '''
    '''

    pass

def regular_ngon():
    '''
    '''

    pass

def polygon():
    '''
    '''

    pass
