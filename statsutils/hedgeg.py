def hedgeg(x, y):
    '''
    Calculate effect size hedge's g for t-test

    x,y are two one-dimensional ndarrays

    We define hedge's g as follows

    d = (mean(x)-mean(y)) / s
        where s is the pooled variance

    nx and ny are number of elements in two arrays

    s = sqrt(((nx-1)*sXsquare + (ny-1)*sYsquare)/(nx+ny))

    s1square = 1/(n1-1) * sum(x-mean(x)) ** 2

    Note:
        1. we assume no nan values

    '''

    # check input
    import numpy as np
    if not isinstance(x, np.ndarray):
        raise ValueError('Please input a np.ndarray')
    if not isinstance(y, np.ndarray):
        raise ValueError('Please input a np.ndarray')

    nx = x.size
    ny = y.size

    return np.abs((x.mean() - y.mean())) / np.sqrt( ((nx-1) * x.var() + (ny-1) * y.var()) / (nx + ny-2))
