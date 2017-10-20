
def linspacepixels(x1, x2, n=50):
    # return a vector of equally spaced points that can
    # be treated as centers of pixels whose total field-of-view
    # would be bounded by <x1> and <x2>.
    # linspacepixels(x1,x2,n)
    #
    # <x1>,<x2> are numbers
    # <n> is the number of desired points
    #
    # Example:
    # isequal(linspacepixels(0,1,2),[.25 .75])
    import numpy as np
    dif = (x2-x1)/n/2  # half the difference between successive points
    return np.linspace(x1+dif, x2-dif, num=n)


def listfy(x, axis=0):
    '''
    Make a ndarray into a list along one axis. We use np.split
    Args:
        x: input ndarray
        axis: long which axis to listfy the ndarray
    Return:
        a list of ndarray object
    Example:
        x = np.random.rand(10, 10, 5)
        y = rz.index.listfy(x, axis = 2)
        len(y)
    '''
    import numpy as np
    # axis is more than number
    assert(axis+1 <= x.ndim), 'axis number is too large'
    x_list = np.split(x, x.shape[axis], axis=axis)
    x_list = list(map(np.squeeze, x_list))  # squeeze the element in b
    return x_list
