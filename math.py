# RZ's math module


def posrect(x):
    '''
    postive reactify the matrix number
    x is a ndarray
    '''
    x[x < 0] = 0
    return x
