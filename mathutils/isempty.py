def isempty(a):
    '''
    wrapper of np.isnan, np.isnan cannot take None object

    a can be number, string, list, dict, set, np.array, None

    Note that if a is none, we return true
    '''
    import numpy as np
    if isinstance(a, np.ndarray):
        return a.size == 0
    else:
        if a:
            return False
        else:
            return True