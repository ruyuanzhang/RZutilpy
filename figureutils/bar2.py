def bar2(x, height, errfmt='line', **kwargs):
    '''
    bar function deal with multiple input height
    '''


    '''
    Plot multiple lines and errrobars together.
    Combine plt.plot and plt.errorbar, to make the plot and errorbar whithin
    the same function since plt.errorbar function cannot plot multiple line
    together

    Note this function accept all input as plt.plot and plt.errorbar

    Args:
        We keep all args in plt.errorbar, except that:
        x: a 1D array or 2D array. if 1D, the size should be same as column
            size of height, x.shape[0]= height.shape[0]; if x is 2D, x.shape = height.shape
        height: a 2D array, with each column is a line e.g., height[:,0] is a line
    errfmt:

    Return:
        we combine and return all return values from plt.errorbar with three
        ndarray of artist collections, with line object, cap object and line
        collections

    Example:


    History
        20180928 now accept a list for all kwargs for individual lines
        20171205 rz add color list function to multiple lines.a

    '''
    import numpy as np
    import matplotlib.pyplot as plt

    # check input, if a single number ,we convert it to array
    # deal with height
    height = np.array(height) if not isinstance(height, np.ndarray) else height
    height = np.array([height]) if height.ndim == 0 else height

    # deal with x
    if x is None:
        x = np.arange(height.shape[0])
    else:
        x = np.array(x) if not isinstance(x, np.ndarray) else x
        x = np.array([x]) if x.ndim == 0 else x

    # deal with yerr
    xerr=kwargs['xerr'] if 'xerr' in kwargs else None
    yerr=kwargs['yerr'] if 'yerr' in kwargs else None

    if yerr is not None:
        yerr = np.array(yerr) if not isinstance(yerr, np.ndarray) else yerr
        yerr = np.array([yerr]) if yerr.ndim == 0 else yerr
    # deal with xerr
    if xerr is not None:
        xerr = np.array(xerr) if not isinstance(xerr, np.ndarray) else xerr
        xerr = np.array([xerr]) if xerr.ndim == 0 else xerr

    # derive axes
    axes = plt.gca() if 'axes' not in kwargs else kwargs['axes']

    # format x, height, yerr dimension.
    # We want x,height are dot x lines arrays
    # We want yerr are dot x lines x 2 arrays
    if height.ndim == 1:  # we only have one line
        height = height[:, np.newaxis]
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
        x = np.tile(x, (height.shape[1], 1)).T if x.ndim==1 else x
        if yerr is not None:
            if yerr.ndim == 2:
                yerr = yerr[:, :, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)
                # now yerror is a dotxlinex2 matrix
            assert yerr.ndim == 3, ValueError('might check yerr dimension')

    nBars = height.shape[1]
    # deal with the x position and height
    groupWidth = min(0.8, nBars/(nBars+1.5));
    barWidth = groupWidth / nBars
    xLoc_tmp = np.arange(-groupWidth / 2 + barWidth / 2, groupWidth / 2, barWidth)
    xLoc_tmp = np.tile(xLoc_tmp[np.newaxis, :],(height.shape[0],1))
    x = x + xLoc_tmp;
    barWidth = barWidth * 0.8

    # now check the x, height shape
    assert x.shape == height.shape, ValueError('incompatible dimension of x,height')
    # check errorbar size
    if yerr is not None and yerr.shape[1] != nBars:
        raise ValueError('incompatible dimension of yerr,height')
    if xerr is not None and xerr.shape[1] != nBars:
        raise ValueError('incompatible dimension of xerr,height')

    # deal with other *kwarges
    for k,v in kwargs.items():
        if not isinstance(v, list):
            kwargs[k] = [v] * nBars
        else:
            errmsg = '{}, Number of input should be consistent with lines'.format(k)
            assert len(v)==nBars, errmsg

    #ecolor = [ecolor] * nBars if not isinstance(ecolor, list) else ecolor

    # initialize lists of return
    patch_list = []
    errorbar_list = []
    # do it
    for i in range(nBars):

        yerrtmp = None if yerr is None else np.transpose(yerr[:, i, :])  # yerr input should be 2xN
        xerrtmp = None if xerr is None else np.transpose(xerr[:, i, :])  # xerr input should be 2xN

        # deal with kwargs
        kwargs_tmp = dict()
        for k,v in kwargs.items():
                kwargs_tmp[k] = kwargs[k][i]
        kwargs_tmp['width'] = barWidth
        kwargs_tmp['xerr'] = xerrtmp
        kwargs_tmp['yerr'] = yerrtmp
        kwargs_tmp['axes'] = axes

        # some keyward variables can receive a list as input to specify individual lines
        bar_container = axes.bar(x[:, i], height[:, i], **kwargs_tmp)

        # set errorbar color
        bar_container.errorbar[2][0].set_color([i.get_edgecolor() for i in bar_container.patches]) if 'ecolor' not in kwargs_tmp else bar_container


        patch_list.append(bar_container.patches)
        errorbar_list.append(bar_container.errorbar)

    return patch_list, errorbar_list