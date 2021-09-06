def polyfit1d(x, y, deg=1):
    '''
    polyfit1d(x, y, deg=1):

    Fit a polynomial function to y based on 1d data x, with order <deg>

    Input:
        <x>: 1d array
        <y>: target data value, should be 1d
        <deg>: int, the highest polynomial order to use, default:1

    Output:
        <coef>: 1d array, derived coefficients. See Note note below for the order
                    of coef
        <predy>: 1d array = y.size.
        <residual>: a scaler residual of the model fitting
        <weight>: 1d array = y.size

    This function is basically a wrapper of the numpy.polynomial.polynomial.polyfit

    The <coef> corresponds to the polynomial item with low to high order

    x,y can have nan or inf value. But we do not include them when computing weight
    We directly return nan values in x, y

    Example:


    History:
        20180629 RZ added <weight> func input
        20180616 RZ created it

    To do:
        - implement multiple x data point?

    '''
    from numpy import isfinite, ndarray
    from numpy.polynomial.polynomial import polyfit, polyval

    # check input
    assert isinstance(x, ndarray) and x.ndim == 1, 'x should be 1d ndarray!'
    assert isinstance(y, ndarray) and y.ndim == 1, 'y should be 1d ndarray!'
    
    # isfinite can check both nan and inf values
    #valid = isfinite(x) & isfinite(y)

    # now solve the equation
    coef, result = polyfit(x, y, deg=deg, full=True)
    # result is a list [residuals, rank, singular_values, rcond]
    residual = result[0]

    # get prediction
    predy = polyval(x, coef)

    return coef, predy, residual

