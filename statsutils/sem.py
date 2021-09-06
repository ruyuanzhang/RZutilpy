def sem(x, axis=0, ddof=1, nan_policy='omit'):
    '''
    compute standard error of a numpy array, we use scipy.stats.sem, with
    1 change
    we set default nan_policy to 'omit', which ignore the nan

    To check the meaning of input, please help scipy.stats.sem function


    '''

    # check input
    from numpy import ndarray
    import scipy.stats as stats

    assert isinstance(x, ndarray), ValueError('Please input a np.ndarray')
    # deal with nan value
    return stats.sem(x, axis=axis, ddof=ddof, nan_policy=nan_policy)