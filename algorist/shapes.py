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
from copy import deepcopy
from itertools import chain
from math import acos, asin, atan, pi, radians, sqrt
import os

import cairocffi as cairo
import numpy as np

import surfaces
import transformations
import patterns

class Shape():
    '''Objects used to draw on surfaces

    Attributes
    ----------
    '''

    VALID_ATTRS = {
        'draw_function', 'ctx', 'surface', 'xy', 'angle',
        'trans_matrix', 'fill', 'linecolor', 'lc', 'linewidth',
        'lw', 'outlinecolor', 'olc', 'outlinewidth', 'olw',
        'linestyle', 'ls', 'linecap', 'lcap', 'conn_style',
        'zorder', '_saved_attrs'
    }
    ABBREVIATIONS = {
        'lc': 'linecolor', 'lw': 'linewidth', 'olc': 'outlinecolor',
        'olw': 'outlinewidth', 'ls': 'linestyle', 'lcap': 'linecap'
    }
    DEFAULTS = {'fill': (1,1,1), 'line_color': (0,0,0), xy=(0,0), angle=0}

    def __init__(self, draw_function, *, surface=None, **kwargs):
        self.draw_function = draw_function
        self._set_kwargs(**kwargs)
        self._set_defaults(**kwargs)

    def _set_kwargs(self, **kwargs):
        for attr, value in kwargs.items():
            self._validate_attr(attr, **kwargs)
            setattr(self, attr, value)

    def _validate_attr(self, attr, **kwargs):
        # Not a valid keyword argument
        if attr not in self.VALID_ATTRS:
            raise AttributeError('Shape has no attribute {}'.format(attr))
        # Check if both a kwarg and its abbreviation were given
        if self.ABBREVIATIONS.get(attr) in kwargs:
            full = self.ABBREVIATIONS[attr]
            message = 'Received both {} and {} as parameters'.format(attr, full)
            raise AttributeError(message)

    def __setattr__(self, attr, value):
        # Set attr to the full name if it's an abbreviation - else leave it
        attr = self.ABBREVIATIONS.get(attr, attr)
        super().__setattr__(attr, value)

    def _set_defaults(self, **kwargs):
        for attr, default_value in self.DEFAULTS.items():
            if (attr in kwargs) or (self.ABBREVIATIONS.get(attr) in kwargs):
                continue
            setattr(self, attr, default_value)
        if 'trans_matrix' not in **kwargs:
            setattr(self, 'trans_matrix', self._default_trans_matrix())

    def _default_trans_matrix(self):
        R1 = transformations.rotation(self.angle)
        T1 = transformations.translation(self.xy)
        return transformations.compose([R1, T1])

    def __enter__(self):
        self.ctx.save()
        self._saved_attrs = deepcopy(self.__dict__)
        return self

    def __exit__(self, exc_type, value, traceback):
        self.ctx.restore()
        self._restore_initial_attrs()

    def _restore_initial_attrs(self):
        for attr, value in self._saved_attrs()

    def draw(self, fill=True, line=True, outline=False, order=['ol', 'l', 'f']):
        pass

    def draw_fill(self):
        pass

    def draw_line(self):
        pass

    def draw_outline(self):
        pass

    def _set_sources(self):
        pass

    def _set_fill_source(self):
        pass

    def _set_line_source(self):
        pass

class ShapeGroup():
    '''
    '''
    def __init__(self, shapes):
        self.shapes = shapes

@contextmanager
def save(drawable):


def line(start, end, **kwargs):
    '''
    '''
    def draw_function(ctx):
        ctx.move_to(*start)
        ctx.line_to(*end)

    return Shape(draw_function, **kwargs)

def polyline(points, *, close_shape=False **kwargs):
    '''
    '''
    start, *remainder = points

    def draw_function(ctx):
        ctx.move_to(*start)
        for point in remainder:
            ctx.line_to(*point)
        if close_shape:
            ctx.close_path()

    return Shape(draw_function, surface=surface, **kwargs)

def arrow(start, end, *, head_width=1/10, head_length=1/8, overhang=0,
          include_shaft=True, surface=None, **kwargs):
    '''
    '''
    (normed, perp, head_width, head_length,
     overhang, relative_head_position) = _get_arrow_params(
        start, end, head_width, head_length, overhang, **kwargs
     )

    def draw_function(ctx, inc_s=include_shaft):
        ctx.move_to(*start)
        if inc_s:
            ctx.rel_line_to(*relative_head_position)
        else:
            ctx.rel_move_to(*relative_head_position)
        _make_arrow_head(ctx, normed, perp, head_width, head_length, overhang)
        ctx.close_path()

    return Shape(draw_function, **kwargs)

def _get_arrow_params(start, end, head_width, head_length, overhang, **kwargs):
    '''
    '''
    vector = np.diff([start, end], axis=0)
    normed = _unit_vector(vector)
    length = np.linalg.norm(vector)
    perp = _get_2d_perpendicular(normed)
    head_width, head_width, overhang = length*np.array([
        head_width, head_length, overhang
    ])
    try:
        linewidth = kwargs['linewidth']
    except KeyError:
        linewidth = kwargs['lw']
    # Shift the head backwards along the length of the arrow to account
    # for the overhang due to non-zero linewidths
    linewidth_shift = sqrt(1-(2*head_length/head_width)**2)*linewidth/2
    relative_head_position = vector - (head_length + linewidth_shift)*normed

    return (
        normed, perp, head_width, head_length, overhang, relative_head_position
    )


def _make_arrow_head(ctx, normed, perp, head_w, head_l, overhang):
    '''
    '''
    ctx.rel_line_to(*(-overhang*normed + 0.5*head_w*perp))
    ctx.rel_line_to(*(head_l*normed - 0.5*head_w*perp))
    ctx.rel_line_to(*(-head_l*normed - 0.5*head_w*perp))
    ctx.rel_line_to(*(overhang*normed + 0.5*head_w*perp))

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

def arc(r, stop, start=0, *, ):
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

def bezier(points, **kwargs):
    '''
    '''
    start, *remainder = points

    def draw_function(ctx):
        ctx.move_to(*start):
        ctx.curve_to(*chain(*remainder))

    return Shape(draw_function, **kwargs)

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

def set_default_surface(surface):
    pass

def _unit_vector(arr):
    norm = np.linalg.norm(arr)
    return np.asarray(arr)/norm

def _get_2d_perpendicular(arr):
    return np.array([arr[1], -arr[0]])
