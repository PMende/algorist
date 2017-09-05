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

from contextlib import contextmanager
from itertools import chain
import os

import cairocffi as cairo
import numpy as np

class Shape():
    '''Objects used to draw on surfaces

    Attributes
    ----------
    '''

    VALID_KWARGS = {
        'fill', 'f', 'linecolor', 'lc', 'linewidth', 'lw',
        'outlinecolor', 'olc', 'outlinewidth', 'olw',
        'linestyle', 'ls', 'linecap', 'lcap', 'conn_style',
        ''
    }

    DEFAULTS = {}

    def __init__(self):
        pass

    def __setattr__(self, attr, value):
        if attr in self.VALID_KWARGS:
            super().__setattr__(attr, value)
        else:
            raise AttributeError('Shape has no attribute {}'.format(attr))

    def __enter__(self):
        self.ctx.save()

    def __exit__(self, type, value, traceback):
        self.ctx.restore()

    def draw(self, fill=True, stroke=True, outline=False, order='osf'):
        pass

    def _set_sources(self):
        pass

    def set_fill_source(self):
        pass

    def draw_fill(self):
        pass

    def draw_stroke(self):
        pass

    def draw_outline(self):
        pass

class ShapeGroup(object):
    '''
    '''

    def __init__(self, shapes):
        self.shapes = shapes

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
