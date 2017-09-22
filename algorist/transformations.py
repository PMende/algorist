'''A set of functions used to transform objects

FUNCTIONS
---------
translation: returns a translation matrix
rotation: returns a rotation matrix
reflection: returns a reflection matrix
scale: returns a scaling matrix
shear: returns a chearing matrix
'''

from functools import reduce
from math import (cos, radians, sin)

import cairocffi as cairo
import numpy as np

class DimensionError(ValueError):
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
        v = np.array((x, y, 1)).
    '''

    if np.asarray(xy).shape != (2,):
        raise DimensionError('xy must be of shape (2,)')

    dx, dy = xy
    translation_matrix = np.array([
        [1., 0., dx,
        [0., 1., dy,
        [0., 0., 1.]
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
        v = np.array((x, y, 1)). When axis is None, this will simply
        be a regular 2x2 rotation matrix with an extra 1 on the diagonal.
    '''

    angle = radians(angle)

    if axis is None:
        rotation_matrix = np.array([
            [cos(angle), -sin(angle), 0.],
            [sin(angle),  cos(angle), 0.],
            [0.,          0.,         1.]
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
        v = np.array((x, y, 1)). When point is None, this will simply
        be a regular 2x2 reflection matrix with an extra 1 on the diagonal.
    '''

    angle = radians(angle)

    if point is None:
        reflection_matrix = np.array([
            [cos(2*angle),  sin(2*angle), 0.],
            [sin(2*angle), -cos(2*angle), 0.],
            [0.,           0.,            1.]
        ])

    else:
        point = np.asarray(point)
        if point.shape != (2,):
            raise DimensionError('axis must be of shape (2,)')

        T1 = translation(xy=-point)
        R = reflection(angle=angle)
        T2 = translation(xy=point)

        reflection_matrix = np.dot(T2, np.dot(R, T1))

    return reflection_matrix

def relative_translation(source, target, distance):
    '''Translation matrix that moves a given target a distance from sources

    Parameters
    ----------
    source: 2-tuple of floats (required) - The point to be translated
        relative to
    target: 2-tuple of floats (required) - A representative point of the
        object to be translated (e.g., the center of a circle, or the
        centroid of a polygon)
    distance float (required) - How far to move target from source

    Returns
    -------
    translation_matrix: 3x3 numpy array. A translation matrix
    '''

    vector = np.asarray(target) - source
    unit_vector = _unit_vector(vector)
    return translation(distance*unit_vector)

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
        v = np.array((x, y, 1)).
    '''

    if scale_y is None:
        scale_y = scale_x

    stretch_matrix = np.array([
        [scale_x, 0.,      0.],
        [0.,      scale_y, 0.],
        [0.,      0.,      1.]
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
        v = np.array((x, y, 1)).
    '''

    scale_xy, scale_yx = shear_factors

    shear_matrix = np.array([
        [1.,       scale_xy, 0.],
        [scale_yx, 1.,       0.],
        [0.,       0.,       1.]
    ])

    return shear_matrix

def compose(matrices):
    '''Multiplies an arbitrary list of transformation matrices together

    Parameters
    ----------
    matrices: List of 3x3 transformation matrices. The 0th element of
        is the first transformation to be applied, the 1st is the second,
        etc.

    Returns
    -------
    result: 3x3 numpy array. This is the result of sequentially multiplying
        each matrix in the matrices argument
    '''
    # Reverse the order of the matrices so that the last element is
    # multiplied on the second to last is multiplied on the third to
    # last, etc.
    result = reduce(np.dot, matrices[::-1])
    return result

def create_cairo_matrix(matrix):
    '''Creates a cairo Matrix object from the supplied matrix

    Parameters
    ----------
    matrix: Affine transformation matrix (3x3 NumPy array)

    Returns
    -------
    cairo_matrix: Cario.Matrix instance
    '''
    columns_first_2_rows = zip(*matrix[:2,:])
    return cairo.Matrix(*chain(*columns_first_2_rows))

def _unit_vector(arr):
    norm = np.linalg.norm(arr)
    return np.asarray(arr)/norm

def _get_2d_perpendicular(arr):
    return np.array([arr[1], -arr[0]])
