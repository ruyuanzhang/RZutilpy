def checkarray(m):
    # check whether m is a ndarray
    import numpy as np
    assert isinstance(m, np.ndarray), 'Please input a ndarray'
