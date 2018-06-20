def checkarray(m):
    '''
    #=======================
    deprecated since 20180616
    #=======================
    '''

    # check whether m is a np.ndarray
    from numpy import ndarray
    assert isinstance(m, ndarray), 'Please input a ndarray'
