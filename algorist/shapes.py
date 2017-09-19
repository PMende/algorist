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
from operator import attrgetter
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
        'draw_function', 'ctx', 'xy', 'angle',
        'trans_matrix', 'fill', 'linecolor', 'lc', 'linewidth',
        'lw', 'outlinecolor', 'olc', 'outlinewidth', 'olw',
        'linestyle', 'ls', 'linecap', 'lcap', 'conn_style',
        'zorder', '_saved_attrs'
    }
    ABBREVIATIONS = {
        'lc': 'linecolor', 'lw': 'linewidth', 'olc': 'outlinecolor',
        'olw': 'outlinewidth', 'ls': 'linestyle', 'lcap': 'linecap'
    }
    DEFAULTS = {'fill': (1,1,1), 'line_color': (0,0,0), xy=(0,0), angle=0,
                'zorder': 0
    }

    def __init__(self, draw_function, **kwargs):
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
        for attr, value in self._saved_attrs():
            if attr == 'ctx':
                continue
            setattr(self, attr, value)
        del self._saved_attrs

    def draw(self, fill=True, line=True, outline=False,
             order=['ol', 'l', 'f'], *, target):
        '''Draws the Shape to the target's surface

        Parameters
        ----------
        fill: bool (optional - default: True) - Whether to draw the fill of
            the shape object
        line: bool (optional - default: True) - Whether to draw the stroke
            (or line) of the shape object
        outline: bool (optional - default: False) - Whether to draw the
            outline of the shape object

        Returns
        -------
        None
        '''
        pass

    def _draw_fill(self):
        pass

    def _draw_line(self):
        pass

    def _draw_outline(self):
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
    def __init__(self, shapes=None, sort_by_z=False):
        self._set_shapes(shapes, sort_by_z)

    def __iter__(self):
        return self.shapes.__iter__()

    def __enter__(self):
        for shape in self:
            shape.__enter__()

    def __exit__(self):
        for shape in self:
            shape.__exit__()

    def _set_shapes(self, shapes, sort):
        if shapes is None:
            self.shapes = []
            return
        if sort:
            _shapes = sorted(shapes, key=attrgetter('zorder'), reverse=True)
        else:
            _shapes = shapes
        self.shapes = _shapes

    def draw(self, *, target):
        for shape in self.shapes:
            shape.draw(target=target)

@contextmanager
def save(drawable):
    pass

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

    return Shape(draw_function, **kwargs)

def arrow(start, end, *, head_width=1/10, head_length=1/8, overhang=0,
          include_shaft=True, **kwargs):
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

def _unit_vector(arr):
    norm = np.linalg.norm(arr)
    return np.asarray(arr)/norm

def _get_2d_perpendicular(arr):
    return np.array([arr[1], -arr[0]])
