def zerodiv(x, y, val=0):
    '''
    zerodiv(x, y, val=0)

    <x><y> are same dimension. divide if <y> is 0 or nan, then use <val>.

    <val> default is 0

    '''
    from numpy import isnan

    valid = ~(isnan(y) | (y == 0))
    f = x.copy().astype('float')
    f[valid] = x[valid] / y[valid]
    f[~valid] = val
    return f