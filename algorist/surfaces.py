'''Module of Surface objects that are the base cavas for drawing

CLASSES
-------
Surface: UNIMPLEMENTED
ImageSurface: UNIMPLEMENTED
PSSurface: UNIMPLEMENTED
SVGSurface: UNIMPLEMENTED
'''


class Surface():
    '''Base canvas-like object to be drawn on
    '''
    def __init__(self, *, name=None, shapes=None):
        if shapes is None:
            self.shapes = []
        else:
            self.shapes = shapes

    def render(self):
        pass

    def write(self):
        pass

    def add(shape):
        self.

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
