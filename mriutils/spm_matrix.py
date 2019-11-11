def spm_matrix(P, order):

    '''
    spm_matrix(P, order)

    Return an affine transformation matrix

    <P>: a 1d array with 12 element
    <order>: a str, see below

    FORMAT [A] = spm_matrix(P [,order])
    P(1)  - x translation
    P(2)  - y translation
    P(3)  - z translation
    P(4)  - x rotation about - {pitch} (radians)
    P(5)  - y rotation about - {roll}  (radians)
    P(6)  - z rotation about - {yaw}   (radians)
    P(7)  - x scaling
    P(8)  - y scaling
    P(9)  - z scaling
    P(10) - x affine
    P(11) - y affine
    P(12) - z affine

    order - application order of transformations [Default: 'T*R*Z*S']

    A     - affine transformation matrix
    __________________________________________________________________________

    spm_matrix returns a matrix defining an orthogonal linear (translation,
    rotation, scaling or affine) transformation given a vector of
    parameters (P).  By default, the transformations are applied in the
    following order (i.e., the opposite to which they are specified):

    1) shear
    2) scale (zoom)
    3) rotation - yaw, roll & pitch
    4) translation

    This <order> can be changed by calling spm_matrix with a string as a
    second argument. This string may contain any valid MATLAB expression
    that returns a 4x4 matrix after evaluation. The special characters 'S',
    'Z', 'R', 'T' can be used to reference the transformations 1)-4)
    above. The default order is 'T*R*Z*S', as described above.

    SPM uses a PRE-multiplication format i.e. Y = A*X where X and Y are 4 x n
    matrices of n coordinates.
    __________________________________________________________________________

    See also: spm_imatrix.m
    __________________________________________________________________________
    Copyright (C) 1994-2011 Wellcome Trust Centre for Neuroimaging

    # Karl Friston
    # $Id: spm_matrix.m 4414 2011-08-01 17:51:40Z guillaume $
    '''


    from numpy import ndarray
    import numpy as np
    # check input
    assert isinstance(P, ndarray), 'Please input an ndarray!'


    #-Special case: translation only
    #--------------------------------------------------------------------------
    if P.size == 3:
        A = np.eye(4)
        A[:4,-1] = P
        return A


    #-Pad P with 'null' parameters
    #--------------------------------------------------------------------------
    q  = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0])
    P  = np.concatenate((P, q[P.size:]))


    #-Translation / Rotation / Scale / Shear
    #--------------------------------------------------------------------------
    T  =   np.array([1, 0, 0, P[0],
            0,   1,   0,   P[1],
            0,   0,   1,   P[2],
            0,   0,   0,   1]).reshape(4,4)

    R1  =  np.array([1, 0,           0,           0,
            0,   np.cos(P[3]),   np.sin(P[3]),   0,
            0,  -np.sin(P[3]),   np.cos(P[3]),   0,
            0,   0,           0,           1]).reshape(4,4)

    R2  =  np.array([np.cos(P[4]),   0,   np.sin(P[4]),   0,
            0,           1,   0,           0,
           -np.sin(P[4]),   0,   np.cos(P[4]),   0,
            0,           0,   0,           1]).reshape(4,4)

    R3  =  np.array([np.cos(P[5]),   np.sin(P[5]),   0,   0,
           -np.sin(P[5]),   np.cos(P[5]),   0,   0,
            0,           0,           1,   0,
            0,           0,           0,   1]).reshape(4,4)

    R   = R1 @ R2 @ R3

    Z   =  np.array([P[6],   0,       0,       0,
            0,      P[7],    0,       0,
            0,      0,       P[8],    0,
            0,      0,       0,       1]).reshape(4, 4)

    S   =  np.array([1,      P[9],   P[10],   0,
            0,      1,       P[11],   0,
            0,      0,       1,       0,
            0,      0,       0,       1]).reshape(4, 4)

    #-Affine transformation matrix
    #--------------------------------------------------------------------------
    if order is None:
        A = T @ R @ Z @ S
    else:
        A = eval('{};'.format(order))
        if ~np.all(np.isfinite(A)) or A.shape!=(4, 4):
            raise ValueError('Invalid order expression ''{}''.'.format(order))
    return A