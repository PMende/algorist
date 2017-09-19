'''Module of Surface objects that are the base cavas for drawing

CLASSES
-------
Surface: UNIMPLEMENTED
ImageSurface: UNIMPLEMENTED
PSSurface: UNIMPLEMENTED
SVGSurface: UNIMPLEMENTED
'''

import cairocffi as cairo
import numpy as np

import shapes


class Surface():
    '''Base canvas-like object to be drawn on
    '''
    def __init__(self, *, name=None):
        self.name = name

    def __iter__(self):
        return self.shapes.__iter__()

    def render(self):
        pass

    def write(self):
        pass

    def add(self, shape):
        pass

    def _bind(self, shape):
        pass

class ImageSurface(Surface):
    '''
    '''
    def __init__(self, size, *, name=None, **kwargs):
        pass

class PSSurface(Surface):
    '''
    '''
    def __init__(self, size, *, name):
        pass

class SVGSurface(Surface):
    '''
    '''
    def __init__(self):
        pass
