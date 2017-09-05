'''Module for creating shapes for use with a Surface instance

CLASSES
-------
Shape: UNIMPLEMENTED
ShapeGroup: UNIMPLEMENTED

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

import surfaces

class Shape():
    '''Objects used to draw on surfaces

    Attributes
    ----------
    '''

    VALID_KWARGS = {
        'draw_function', 'surface' 'fill', 'linecolor', 'lc', 'linewidth',
        'lw', 'outlinecolor', 'olc', 'outlinewidth', 'olw', 'linestyle', 'ls',
        'linecap', 'lcap', 'conn_style'
    }

    ABBREVIATIONS = {
        'lc': 'linecolor', 'lw': 'linewidth', 'olc': 'outlinecolor',
        'olw': 'outlinewidth', 'ls': 'linestyle', 'lcap': 'linecap'
    }

    DEFAULTS = {
        'surface': surfaces.ImageSurface()
    }

    def __init__(self, draw_function, **kwargs):
        for key, value in kwargs.items():
            if self.ABBREVIATIONS.get(key) in kwargs:
                full = self.ABBREVIATIONS[key]
                raise AttributeError(
                    'Received both {} and {} as parameters'.format(key, full))
            # Set key to the full attribute name if it is an abbreviation
            if key in self.ABBREVIATIONS:
                key = self.ABBREVIATIONS[key]
            setattr(self, key, value)

    def __setattr__(self, attr, value):
        if attr in self.VALID_KWARGS:
            super().__setattr__(attr, value)
        else:
            raise AttributeError('Shape has no attribute {}'.format(attr))

    def __enter__(self):
        self.ctx.save()

    def __exit__(self, exc_type, value, traceback):
        self.ctx.restore()

    def draw(self, fill=True, line=True, outline=False, order=['ol', 'l', 'f']):
        pass

    def _set_sources(self):
        pass

    def set_fill_source(self):
        pass

    def draw_fill(self):
        pass

    def draw_line(self):
        pass

    def draw_outline(self):
        pass

    @staticmethod
    _set_sour

class ShapeGroup():
    '''
    '''
    def __init__(self, shapes):
        self.shapes = shapes

def line(start, end, **kwargs):
    '''
    '''
    def draw_function(ctx):
        ctx.move_to(*start)
        ctx.line_to(*end)
    return Shape(draw_function, **kwargs)

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
