def plot(x, y, yerr=None, xerr=None, axes=None, **kwargs):
    '''
    Plot multiple lines and errrobars together.
    Combine plt.plot and plt.errorbar, to make the plot and errorbar whithin
    the same function since plt.errorbar function cannot plot multiple line
    together

    Note this function accept all input as plt.plot and plt.errorbar

    Args:
        We keep all args in plt.errorbar, except that:
        <x>: a 1D array or 2D array. if 1D, the size should be same as column
            size of y, x.shape[0]= y.shape[0]; if x is 2D, x.shape = y.shape
        <y>: a 2D array, with each column is a line e.g., y[:,0] is a line
        <xerr>, <yerr>: should be dot x line or, dot x line x 2 errorbar. the 3rd
            dimension represent the lower [0] and upper [1] errorbar. when
            x, y is a single line, xerr and yerr can be 1D array
        <axes>: axes to plot
        <kwargs>: keyword arguments for the plt.errorbar and plt.plot function

    Return:
        we combine and return all return values from plt.errorbar with three
        ndarray of artist collections, with line object, cap object and line
        collections

    Example:

    plt.close('all')
    x = np.arange(10)
    y = np.random.rand(10)
    yerr = np.random.rand(10,1,2) / 10
    a = rz.figure.plot(x,y,yerr=yerr, fmt='-o')

    plt.close('all')
    x = np.arange(10)
    y = np.random.rand(10, 3)
    yerr = np.random.rand(10,3,2) / 10
    a = rz.figure.plot(x,y,yerr=yerr, fmt='-o')

    Note:
    1. how to check single input data type. Single number should
        still be an array

    History
    20180928 now accept a list for all kwargs for individual lines
    20171205 rz add color list function to multiple lines.

    '''
    import numpy as np
    import matplotlib.pyplot as plt

    # check input, if a single number ,we convert it to array
    # deal with y
    y = np.array(y) if not isinstance(y, np.ndarray) else y
    y = np.array([y]) if y.ndim == 0 else y

    # deal with x
    if x is None:
        x = np.arange(y.shape[0])
    else:
        x = np.array(x) if not isinstance(x, np.ndarray) else x
        x = np.array([x]) if x.ndim == 0 else x
    # deal with yerr
    if yerr is not None:
        yerr = np.array(yerr) if not isinstance(yerr, np.ndarray) else yerr
        yerr = np.array([yerr]) if yerr.ndim == 0 else yerr
    # deal with xerr
    if xerr is not None:
        xerr = np.array(xerr) if not isinstance(xerr, np.ndarray) else xerr
        xerr = np.array([xerr]) if xerr.ndim == 0 else xerr

    # derive axes
    axes = plt.gca() if axes is None else axes

    # format x, y, yerr, xerr dimension.
    # We want x,y are dot x lines arrays
    # We want yerr, xerr are dot x lines x 2 arrays
    if y.ndim == 1:  # we only have one line
        y = y[:, np.newaxis]
        x = x[:, np.newaxis]
        if yerr is not None:
            if yerr.ndim == 1:
                yerr = yerr[:, np.newaxis, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)  # yerror
            assert yerr.ndim == 3, ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 1:
                xerr = xerr[:, np.newaxis, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            assert xerr.ndim == 3, ValueError('might check xerr dimension')
    else:  # we have multiple lines
        x = np.tile(x, (y.shape[1], 1)).T if x.ndim==1 else x
        if yerr is not None:
            if yerr.ndim == 2:
                yerr = yerr[:, :, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)
                # now yerror is a dotxlinex2 matrix
            assert yerr.ndim == 3, ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 2:
                xerr = xerr[:, :, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            assert xerr.ndim == 3, ValueError('might check xerr dimension')

    nline = y.shape[1]

    # now check the x, y shape
    assert x.shape == y.shape, ValueError('incompatible dimension of x,y')
    # check errorbar size
    if yerr is not None and yerr.shape[1] != nline:
        raise ValueError('incompatible dimension of yerr,y')
    if xerr is not None and xerr.shape[1] != nline:
        raise ValueError('incompatible dimension of xerr,y')

    # deal with other *kwarges
    for k,v in kwargs.items():
        if not isinstance(v, list):
            kwargs[k] = [v] * nline
        else:
            errmsg = '{}, Number of input should be consistent with lines'.format(k)
            assert len(v)==nline, errmsg

    #ecolor = [ecolor] * nline if not isinstance(ecolor, list) else ecolor

    # initialize lists of return
    line_object = []
    cap_object = []
    linecollection_object = []
    # do it
    for i in range(nline):

        yerrtmp = None if yerr is None else np.transpose(yerr[:, i, :])  # yerr input should be 2xN
        xerrtmp = None if xerr is None else np.transpose(xerr[:, i, :])  # xerr input should be 2xN

        kwargs_tmp = dict()
        for k,v in kwargs.items():
                kwargs_tmp[k] = kwargs[k][i]

        # some keyward variables can receive a list as input to specify individual lines
        errout = axes.errorbar(
            x[:, i], y[:, i], yerr=yerrtmp, xerr=xerrtmp, axes=axes, **kwargs_tmp
        )

        line_object.append(errout[0])
        cap_object.append(errout[1])
        linecollection_object.append(errout[2])

    return np.array(line_object), np.array(cap_object), np.array(linecollection_object)