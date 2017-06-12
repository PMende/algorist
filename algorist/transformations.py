'''A set of functions used to transform objects

FUNCTIONS
---------
translation: returns a translation matrix
rotation: returns a rotation matrix
reflection: returns a reflection matrix
scale: returns a scaling matrix
shear: returns a chearing matrix
'''

from math import (cos, radians, sin)

import numpy as np

class DimensionError(Exception):
    '''Simple exception for
    '''
    pass

def translation(xy=(0.,0.)):
    '''Translation matrix

    Parameters
    ----------
    xy: 2-tuple of floats - x is the first element

    Returns
    -------
    translation_matrix - 3x3 numpy array. Translates a vector of the form:
        v = np.array((1., x, y)).
    '''

    if np.array(xy).shape != (2,):
        raise DimensionError('xy must be of shape (2,)')

    translation_matrix = np.array([
        [1.,    0., 0.],
        [xy[0], 1., 0.],
        [xy[1], 0., 1.]
    ])

    return translation_matrix

def rotation(angle, axis=None):
    '''Rotation matrix about a given axis (*counter-clockwise*)

    Parameters
    ----------
    angle: float (required) - angle by which to rotate in degrees.
    axis: 2-tuple of floats (optional), default None - axis about which to
        rotate. Default assumes rotation about (0,0). x, y coordinates
        of axis are axis[0], axis[1], respectively.

    Returns
    -------
    rotation_matrix: 3x3 numpy array. Rotates a vector of the form:
        v = np.array((1., x, y)). When axis is None, this will simply
        be a regular 2x2 rotation matrix with an extra 1 on the diagonal.
    '''

    angle = radians(angle)

    if axis is None:
        rotation_matrix = np.array([
            [1., 0.,         0.],
            [0., cos(angle), -sin(angle)],
            [0., sin(angle), cos(angle)]
        ])

    else:
        axis = np.array(axis)
        if axis.shape != (2,):
            raise DimensionError('axis must be of shape (2,)')

        T1 = translation(xy=-axis)
        R = rotation(angle=angle)
        T2 = translation(xy=axis)

        rotation_matrix = np.dot(T2, np.dot(R, T1))

    return rotation_matrix

def reflection(angle, point=None):
    '''Reflection matix about the plane defined by angle

    Parameters
    ----------
    angle: float (required) - angle defining the plane of reflection.
    point: 2-tuple of floats (optional), default None - point through
        which the mirror plane passes. Default assumes rotation about
        (0,0). x, y coordinates are point[0], point[1], respectively.

    Returns
    -------
    reflection_matrix: 3x3 numpy array. Reflects a vector of the form:
        v = np.array((1., x, y)). When point is None, this will simply
        be a regular 2x2 reflection matrix with an extra 1 on the diagonal.
    '''

    angle = radians(angle)

    if point is None:
        reflection_matrix = np.array([
            [1., 0.,           0.],
            [0., cos(2*angle), sin(2*angle)],
            [0., sin(2*angle), -cos(2*angle)]
        ])

    else:
        point = np.array(point)
        if point.shape != (2,):
            raise DimensionError('axis must be of shape (2,)')

        T1 = translation(xy=-point)
        R = reflection(angle=angle)
        T2 = translation(xy=point)

        reflection_matrix = np.dot(T2, np.dot(R, T1))

    return reflection_matrix

def scale(scale_x, scale_y=None):
    '''Scaling matrix that stretches according to scale_x, scale_y

    Parameters
    ----------
    scale_x: float (required) - Factor by which to scale x and y if scale_y
        is not specified
    scale_y: float (optional), default None -

    Returns
    -------
    stretch_matrix: 3x3 numpy array. Stretches a vector of the form:
        v = np.array((1., x, y)).
    '''

    if scale_y is None:
        scale_y = scale_x

    stretch_matrix = np.array([
        [1., 0.,      0.],
        [0., scale_x, 0.],
        [0., 0.,      scale_y]
    ])

    return stretch_matrix

def shear(shear_factors=(1., 0.)):
    '''Shearing matrix

    Parameters
    ----------
    shear_factors: 2-tuple of floats (required) - default (1., 0.) -

    Returns
    -------
    shear_matrix: 3x3 numpy array. Stretches a vector of the form:
        v = np.array((1., x, y)).
    '''

    scale_xy = shear_factors[0]
    scale_yx = shear_factors[1]

    shear_matrix = np.array([
        [1., 0.,       0.],
        [0., 1.,       scale_xy],
        [0., scale_yx, 1]
    ])

    return shear_matrix
