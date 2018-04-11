def sem(x, axis=0, ddof=0, nan_policy='omit'):
    '''
    compute standard error of a numpy array, we use scipy.stats.sem, with
    two changes
    1. we set default delta degree of freedom as 0
    2. we set nan_policy to 'ignore'

    To check the meaning of input, please help scipy.stats.sem function


    '''

    # check input
    import numpy as np
    import scipy.stats as stats
    if not isinstance(x, np.ndarray):
        raise ValueError('Please input a np.ndarray')

    # deal with nan value
    return stats.sem(x, axis=axis, ddof=ddof, nan_policy=nan_policy)