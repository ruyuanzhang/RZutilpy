def polyfit3d(x, y, z, m, deg=1, grid=True):
    '''
    polyfit3d(x, y, z, m, deg=1, grid=True):

    Fit a polynomial function to 3d coordiantes (x,y,z) with <deg>,
    m is target data.

    Input:
        <x>,<y>,<z>: are 1d arrays
        <m>: target data value, can be 1d or 3d. If 3d, we flatten it to 1d
        <deg>: int, the highest polynomial order to use, default:1
        <grid>: boolean, optional. Whether x, y, z is a grid format. Then we
            convert it to normal array format. This is useful if we fit a polynomial
            to a 3d volume. In this case, m.size = x.size * y.size * z.size
    Output:
        <coef>: 1d array, derived coefficients. See Note note below for the order
            of coef
        <predm>:1d array, predicted m values. or 3d arrays if <grid>=True
        <V>:power item matrix
        <residual>: residual of the model fitting

    We use numpy.polynomial.polynomial.polyvander to construct the polynomial
    arrays V. However, this function construct a full array that only
    constrains the highest power for individual item (x, or, y). This leads to
    highest power in V to 2*deg, exceeding the deg. For example, input highest deg=2,
    then the item with highest order will be x2*y2. The highest order is 2*2 = 4.
    We use the numpy.tril to select appropriate item for fitting.

    Then polyfit3d is equivalent to sole the linear regression
    weight. We use scipy.linalg.lstsq to solve the equation

    The order of coef is correspond to the order of power items in
    the column of V. Thus np.dot(V,coef) should give the <predz>

    Note that the order is flattened version of mask. For example.
    If deg=2, x,y,z power should be [0, 1, 2]. The the order (x,y,z) should be (0,0,1)
    (0,0,2), (0,0,3), ... (2,2,0),(2,2,1),(2,2,2). Note that this is *DIFFERENT*
    from the output of numpy.polyfit, which the coefficient order is from high
    to low to their corresponding power item.

    x,y,z,m can have nan or inf value. We use np.isfinite to recognize them
    But we do not include them when computing weight, We directly return nan
    values in predm

    History:
        20180510 RZ created it


    '''

    import numpy as np
    import scipy.linalg as linalg
    from numpy.polynomial.polynomial import polyvander3d

    # check input
    assert isinstance(x, np.ndarray) and x.ndim == 1, 'x is not 1d np.npdarray!'
    assert isinstance(y, np.ndarray) and y.ndim == 1, 'y is not 1d np.npdarray!'
    assert isinstance(z, np.ndarray) and z.ndim == 1, 'z is not 1d np.npdarray!'
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
    ii,jj,kk = np.meshgrid(np.arange(deg + 1), np.arange(deg + 1), np.arange(deg + 1))
    tt = ii + jj + kk
    mask = tt.flatten() <= deg

    # remove the item that exceeds the order
    V = V[:, mask]  # V is a point x num power time matrix

    # now solve the equation
    coef, residual, _, _= linalg.lstsq(V[valid,:], m[valid])

    # we reverse the order of coef and V to match output of coef
    # with power from high to low. The last one is the constant term.
    predm = np.dot(V, coef)

    if grid:   # if grid case, we output a multi array
        predm = predm.reshape(xsize, ysize, zsize)

    return coef, predm, V, residual