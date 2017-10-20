# -*- coding: utf-8 -*-
"""
RZutilpy figure module

@author: ruyuan
"""


def default_img_set():
    import matplotlib as mpl

    # figure
    mpl.rcParams['figure.frameon'] = False
    mpl.rcParams['figure.titleweight'] = 'regular'
    mpl.rcParams['figure.titlesize'] = 'xx-large'
    mpl.rcParams['figure.autolayout'] = True
    mpl.rcParams['figure.facecolor'] = 'None'
    mpl.rcParams['figure.edgecolor'] = 'None'
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['savefig.frameon'] = False
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['savefig.facecolor'] = 'None'
    mpl.rcParams['savefig.edgecolor'] = 'None'
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    # axes
    mpl.rcParams['axes.facecolor'] = 'None'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.labelsize'] = 'large'
    mpl.rcParams['axes.titleweight'] = 'regular'
    mpl.rcParams['axes.titlesize'] = 'x-large'
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['xtick.major.width'] = 1.5
    mpl.rcParams['xtick.major.size'] = 6
    mpl.rcParams['xtick.labelsize'] = 'medium'
    mpl.rcParams['ytick.major.width'] = 1.5
    mpl.rcParams['ytick.major.size'] = 6
    mpl.rcParams['ytick.labelsize'] = 'medium'
    mpl.rcParams['lines.linewidth'] = 1.5
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    # Character
    mpl.rcParams['font.family'] = 'Arial'
    mpl.rcParams['font.weight'] = 'bold'
    # legend
    mpl.rcParams['legend.frameon'] = False

    # line


def plot(
    x, y, yerr=None, xerr=None, fmt='', axes=None, ecolor=None,
    elinewidth=None, capsize=None, barsabove=False, lolims=False,
    uplims=False, xlolims=False, xuplims=False, errorevery=1,
    capthick=None, rtrnum=1, **kwargs):
    '''
    Plot multiple lines and errrobars together.
    Combine plt.plot and plt.errorbar, to make the plot and errorbar whithin
    the same function since plt.errorbar function cannot plot multiple line
    together

    Args:
        We keep all args in plt.errorbar, except that:
        x: a 1D array or 2D array. if 1D, the size should be same as column
            size of y, x.shape[0]= y.shape[0]; if x is 2D, x.shape = y.shape
        y: a 2D array, with each column is a line e.g., y[:,0] is a line
        xerr, yerr: should be dot x line or, dot x line x 2 errorbar. the 3rd
            dimension represent the lower,[0] and upper,[1] errorbar. when
            x, y is a single line, xerr and yerr can be 1D array
        axes: axes to plot
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

    '''
    import numpy as np
    import matplotlib.pyplot as plt
    # check input, if a sigle number ,we conver it to array
    # deal with y
    if not isinstance(y, np.ndarray):
        y = np.array(y)
    if y.ndim == 0:
        y = np.array([y])
    # deal with x
    if x is None:
        x = np.arange(y.shape[0])
    else:
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        if x.ndim == 0:
            x = np.array([x])
    # deal with yerr
    if yerr is not None:
        if not isinstance(yerr, np.ndarray):
            yerr = np.array(yerr)
        if yerr.ndim == 0:
            yerr = np.array([yerr])
    # deal with xerr
    if xerr is not None:
        if not isinstance(xerr, np.ndarray):
            xerr = np.array(xerr)
        if xerr.ndim == 0:
            xerr = np.array([xerr])

    # derive axes
    if not axes:
        axes = plt.gca()

    # format x, y, yerr, xerr dimension.
    # We want x,y are dot x lines arrays
    # We want yerr,xerr are dot x lines x 2 arrays
    if y.ndim == 1:  # we only one line
        y = y[:, np.newaxis]
        x = x[:, np.newaxis]
        if yerr is not None:
            if yerr.ndim == 1:
                yerr = yerr[:, np.newaxis, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)  # yerror
            if yerr.ndim != 3:
                raise ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 1:
                xerr = xerr[:, np.newaxis, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            if xerr.ndim != 3:
                raise ValueError('might check xerr dimension')
    else:  # we have multiple lines
        if x.ndim == 1:  # expand x to match size of y
            x = np.tile(x, (y.shape[1], 1)).T
        if yerr is not None:
            if yerr.ndim == 2:
                yerr = yerr[:, :, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)
                # now yerror is a dotxlinex2 matrix
            if yerr.ndim != 3:
                raise ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 2:
                xerr = xerr[:, :, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            if xerr.ndim != 3:
                raise ValueError('might check xerr dimension')

    nline = y.shape[1]
    # now check the x, y shape
    if x.shape != y.shape:
        raise ValueError('incompatible dimension of x,y')
    # check errorbar size
    if yerr is not None and yerr.shape[1] != nline:
        raise ValueError('incompatible dimension of yerr,y')
    if xerr is not None and xerr.shape[1] != nline:
        raise ValueError('incompatible dimension of xerr,y')

    # initialize lists of return
    line_object = []
    cap_object = []
    linecollection_object = []
    # do it
    for i in range(nline):
        if yerr is None:
            yerrtmp = None
        else:
            yerrtmp = np.transpose(yerr[:, i, :])  # yerr input should be 2xN
        if xerr is None:
            xerrtmp = None
        else:
            xerrtmp = np.transpose(xerr[:, i, :])


        # some keyward variables can receive a list as input to specify individual lines


        errout = axes.errorbar(
            x[:, i], y[:, i], yerrtmp, xerrtmp, fmt=fmt, ecolor=ecolor,
            elinewidth=elinewidth, capsize=capsize, barsabove=barsabove,
            lolims=lolims, uplims=uplims, xlolims=xlolims, xuplims=xuplims,
            errorevery=errorevery, capthick=capthick, **kwargs
        )

        line_object.append(errout[0])
        cap_object.append(errout[1])
        linecollection_object.append(errout[2])

    if rtrnum == 1:
        return np.array(line_object)
    elif rtrnum == 2:
        return np.array(line_object), np.array(cap_object)
    if rtrnum == 3:
        return np.array(line_object), np.array(cap_object), \
            np.array(linecollection_object)


def regplot(x, y, axes=None, rtrnum=1, **kwargs):
    '''
    rz's wrapper for the seaborn.regplot function, we add the output for the regression result
    '''
    import seaborn.apionly as sns
    import matplotlib.pyplot as plt
    from scipy import stats

    sns.reset_orig()

    if axes is None:
        axes = plt.gca()
    # do it
    p = sns.regplot(x, y, ax=axes, **kwargs)

    # figure out the statistical model
    linregressresult = stats.linregress(x=x, y=y)

    if rtrnum == 1:
        return linregressresult
    elif rtrnum == 2:
        return linregressresult, p
    # get the predict data point
