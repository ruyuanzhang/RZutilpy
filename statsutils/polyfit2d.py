def polyfit2d(x, y, z, deg=1, grid=True, weight=None):
    '''
    polyfit2d(x, y, z, deg=1, grid=True):

    Fit a polynomial function to 2d data (x,y) with order <deg>, z is target data.

    Input:
        <x>,<y>: are 1d arrays
        <z>: target data value, can be 1d or 2d. If 2d, we flatten it to 1d
        <deg>: int, the highest polynomial order to use, default:1
        <grid>: boolean, optional. Whether x, y, z is a grid format. Then we
            convert it to normal array format. This is useful if we fit a polynomial
            to a 2d surface. In this case, z.size = x.size * y.size
        <weight>: same size with z, weight assigned for each data point
    Output:
        <coef>: 1d array, derived coefficients. See Note note below for the order
                    of coef
        <predz>: 1d array = z.size.
        <V>: power item design matrix.
        <residual>: residual of the model fitting

    We use numpy.polynomial.polynomial.polyvander to construct the polynomial
    design matrix V. However, this function construct a full array that only
    constrains the highest power for individual item (x, or, y). This leads to
    highest power in V to 2*deg, exceeding the <deg>. For example, if the input highest <deg>=2,
    then the item with highest order will be x2*y2 = 4.
    We use the numpy.tril to select appropriate item for fitting.

    Then polyfit2d is equivalent to solve the linear regression
    weight. We use scipy.linalg.lstsq to solve the equation

    The order of coef is correspond to the order of power items in
    the column of V. Thus np.dot(V,coef) should give the <predz>

    Note that the order is flattened version of mask. For example.
    If <deg>=2, x and y power should be [0, 1, 2]. The the order (x,y) should be (0,0)
    (0,1), (0.2), ... (2,0),(2,1),(2,2). Hence, the coef[0] is the coefficient for the
    constant item in the regression.Note that this is *DIFFERENT* from the output
    of numpy.polyfit, which the coefficient order is from high to low to their
    corresponding power item.

    x,y,z can have nan or inf value. But we do not include them when computing weight
    We directly return nan values in x, y, z

    Example:
        x, y = np.arange(10), np.arange(10)
        xx,yy = np.meshgrid
        z = 2* x^2 + x + 3*y^2
        plt.subplot(121)
        plt.imshow(z)

    History:
        20180628 RZ add <weight> input
        20180616 RZ double checked the function, it works very well.
        20180510 RZ created it

    To do:
        1. implement multi linear regression

    '''

    import numpy as np
    import scipy.linalg as linalg
    import scipy.sparse as sparse
    from numpy.polynomial.polynomial import polyvander2d

    # check input
    assert isinstance(x, np.ndarray) and x.ndim == 1, 'x is not 1d np.npdarray!'
    assert isinstance(y, np.ndarray) and y.ndim == 1, 'y is not 1d np.npdarray!'
    assert isinstance(z, np.ndarray), 'z must be an array'
    z = z.flatten()

    if weight is None:
        weight = np.ones(m.size)

    # convert if grid=True
    if grid:
        xsize, ysize = x.size, y.size
        xx, yy = np.meshgrid(x, y)
        x, y = xx.flatten(), yy.flatten()

    # deal with nan and inf values
    valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)

    # obtain polymial order array V
    V = polyvander2d(x, y, deg=[deg, deg])

    # we want to set the lower right triangle of V to zero since those item exceeds
    # the highest order
    ii,jj = np.meshgrid(np.arange(deg + 1), np.arange(deg + 1))
    tt = ii + jj
    mask = tt.flatten() <= deg

    # remove the item that exceeds the order
    V = V[:, mask]

    # set the weight matrix
    if weight:
        W = sparse.diags(weight[valid])
        # directly solve the equation
        coef = linalg.inv(V[valid,:].T @ W @ V[valid,:]) @ V[valid,:].T @ W * m[valid]
        predz = np.dot(V, coef)
        residual = (weight[valid] * (predm[valid] - m[valid]) ** 2).sum()
    else:
        coef, residual, _, _= linalg.lstsq(V[valid,:], m[valid])
        predz = np.dot(V, coef)

    if grid:   # if grid case, we output a multi array
        predz = predz.reshape(xsize, ysize)

    return coef, predz, V, residual

