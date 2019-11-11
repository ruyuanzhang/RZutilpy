def posrect(x):
    '''
    postive reactify the matrix number
    x is a ndarray
    '''
    from numpy import ndarray
    assert isinstance(x, ndarray), 'Input should be ndarray'

    x[x < 0] = 0
    return x