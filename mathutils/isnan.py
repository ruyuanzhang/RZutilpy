def isnan(a):
    '''
    wrapper for np.isnan
    a can be number, list, np.array, none
    '''
    import numpy as np
    if a is None:
        return False
    else:
        return np.isnan(a)