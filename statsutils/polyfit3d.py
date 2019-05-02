def polyfit3d(x, y, z, m, deg=1, grid=True, weight=None):
    '''
    polyfit3d(x, y, z, m, deg=1, grid=True, weight=None):

    Fit a polynomial function to 3d coordiantes (x,y,z) with <deg>,
    m is target data.

    Input:
        <x>,<y>,<z>: must be 3d arrays (if <grid> is True), or 1d (if <grid> is False)
        <m>: target data value, can be 1d or 3d. If 3d, we flatten it to 1d
        <deg>: int, the highest polynomial order to use, default:1
        <grid>: boolean, optional. Whether x, y, z is a grid format. Then we
            convert it to normal array format. This is useful if we fit a polynomial
            to a 3d volume. In this case, m.size = x.size * y.size * z.size
        <weight>: same size with m, weight assigned for each data point.
                Note if <weight> then the total number of dots can not be too big, better<100
                otherwise
    Output:
        <coef>: 1d array, derived coefficients. See Note note below for the order
            of coef
        <predm>:1d array, predicted m values. or 3d arrays if <grid>=True
        <V>: power item matrix
        <residual>: a scalar, (weighted) residual of the model fitting

    We use numpy.polynomial.polynomial.polyvander to construct the polynomial
    arrays V. However, this function construct a full array that only
    constrains the highest power for individual item (x, or, y). This leads to
    highest power in V to 2*<deg>, exceeding the order constraint. For example, input <deg>=2,
    then the item with highest order will be x2*y2. The highest order is 2*2 = 4.
    We use the numpy.tril to select appropriate item for fitting.

    Then polyfit3d is equivalent to sole the linear regression
    weight. We use scipy.linalg.lstsq to solve the equation

    The order of coef is correspond to the order of power items in
    the column of V. Thus np.dot(V,coef) should give the <predz>

    Note that the order is flattened version of mask. For example.
    If <deg>=2, x,y,z power should be [0, 1, 2]. The the order (x,y,z) should be (0,0,1)
    (0,0,2), ... (2,2,0),(2,2,1),(2,2,2). Note that this is *DIFFERENT*
    from the output of numpy.polyfit, which the coefficient order is from high
    to low to their corresponding power item.

    x,y,z,m can have nan or inf value. We use np.isfinite to identify them
    and we do not include them when computing weight, We directly return nan
    values in <predm>

    Example:
    x,y,z = np.mgrid[1:100:10j, 1:100:10j, 1:100:10j]
    m = x + 2*x**2 + 3*y**2 + 4*z**2 + 5 + 10*np.random.randn(*x.shape)
    coef, predm, _, _ = rz.stats.polyfit3d(x.flatten(),y.flatten(),z.flatten(),m.flatten(),deg=2, grid=False)
    plt.subplot(121)
    plt.imshow(rz.imageprocess.makeimagestack(m))
    plt.subplot(122)
    plt.imshow(rz.imageprocess.makeimagestack(predm.reshape(*m.shape)))
    plt.subplot
    plt.scatter(m.flatten(), predm.flatten())



    History:
        20180628 RZ add weights functionality, switch to directly solve the equation
        20180510 RZ created it

    '''

    import numpy as np
    import scipy.linalg as linalg
    import scipy.sparse as sparse
    from numpy.polynomial.polynomial import polyvander3d

    # check input
    assert isinstance(x, np.ndarray) and x.ndim in (1,3), 'x is not 1d np.npdarray!'
    assert isinstance(y, np.ndarray) and y.ndim in (1,3), 'y is not 1d np.npdarray!'
    assert isinstance(z, np.ndarray) and z.ndim in (1,3), 'z is not 1d np.npdarray!'
    assert isinstance(m, np.ndarray), 'm must be an array'
    m = m.flatten()

    # convert if grid=True
    if grid:
        xsize, ysize, zsize = x.size, y.size, z.size
        xx, yy, zz = np.meshgrid(x, y, z)
        x, y, z = xx.flatten(), yy.flatten(), zz.flatten()

    # deal with nan and inf values
    valid = np.isfinite(x) & np.isfinite(y) & np.isfinite(z) & np.isfinite(m)

    # obtain polymial order array V
    V = polyvander3d(x, y, z, deg=[deg, deg, deg])

    # we want to set the lower right triangle of V to zero since those item exceeds
    # the highest order
    ii,jj,kk = np.mgrid[0:(deg+1), 0:(deg+1), 0:(deg+1)]
    tt = ii + jj + kk
    mask = tt.flatten() <= deg

    # remove the item that exceeds the order
    V = V[:, mask]  # V is a point x num power time matrix

    # set the weight matrix
    if weight:
        W = sparse.diags(weight[valid])
        # directly solve the equation
        coef = linalg.inv(V[valid,:].T @ W @ V[valid,:]) @ V[valid,:].T @ W * m[valid]
        # we reverse the order of coef and V to match output of coef
        # with power from high to low. The last one is the constant term.
        predm = np.dot(V, coef)
        residual = (weight[valid] * (predm[valid] - m[valid]) ** 2).sum()
    else:
        coef, residual, _, _= linalg.lstsq(V[valid,:], m[valid])
        predm = np.dot(V, coef)

    if grid:   # if grid case, we output a multi array
        predm = predm.reshape(xsize, ysize, zsize)

    return coef, predm, V, residual