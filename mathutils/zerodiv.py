def zerodiv(x, y, val=0):
    '''
    zerodiv(x, y, val=0)

    <x><y> are same dimension. divide if <y> is 0, then use <val>. <val> default is 0

    '''
    import RZutilpy as rz
    valid = ~(rz.math.isnan(y) | (y == 0))
    f = x[valid] / y[valid]
    f[~valid] = val
    return f