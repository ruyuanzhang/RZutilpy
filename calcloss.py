#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:44:25 2017

@author: ruyuan
"""


def calccod(x, y, dim, wantgain=0, wantmeansub=1):
    """
    function f = calccod(x,y,dim,wantgain,wantmeansub)

    Args:

    x,y: are both np.array with the same dimensions
    dim (optional) is the dimension of interest.
      default to 2 if <x> is a (horizontal) vector and to 1 if not.
      special case is 0 which means to calculate globally.
    wantgain (optional) is
      0 means normal
      1 means allow a gain to be applied to each case of <x>
        to minimize the squared error with respect to <y>.
        in this case, there cannot be any NaNs in <x> or <y>.
      2 is like 1 except that gains are restricted to be non-negative.
        so, if the gain that minimizes the squared error is negative,
        we simply set the gain to be applied to be 0.
      default: 0.
    wantmeansub (optional) is
      0 means do not subtract any mean.  this makes it such that
        the variance quantification is relative to 0.
      1 means subtract the mean of each case of <y> from both
        x and y before performing the calculation.  this makes
        it such that the variance quantification
        is relative to the mean of each case of <y>.
        note that wantgain occurs before wantmeansub.
      default: 1.

    Notes:
    calculate the coefficient of determination (R^2) indicating
    the percent variance in <y> that is explained by <x>.  this is achieved
    by calculating 100*(1 - sum((y-x).^2) / sum(y.^2)).  note that
    by default, we subtract the mean of each case of <y> from both <x>
    and <y> before proceeding with the calculation.

    the quantity is at most 100 but can be 0 or negative (unbounded).
    note that this metric is sensitive to DC and scale and is not symmetric
    (i.e. if you swap <x> and <y>, you may obtain different results).
    it is therefore fundamentally different than Pearson's correlation
    coefficient (see calccorrelation.m).

    NaNs are handled gracefully (a NaN causes that data point to be ignored).

    if there are no valid data points (i.e. all data points are
    ignored because of NaNs), we return NaN for that case.

    note some weird cases:
      calccod([],[]) is []

    Hstory:
        2017/05/04 - RZ turn it in to python
        2013/08/18 - fix pernicious case where <x> is all zeros and <wantgain>
                    is 1 or 2.
        2010/11/28 - add <wantgain>==2 case
        2010/11/23 - changed the output range to percentages.  thus, the range
                is (-Inf,100].also, we removed the <wantr> input since it was
                dumb.

    Example:
    x = randn(1,100);
    calccod(x,x+0.1*randn(1,100))

    """
    #
    import numpy as np

    # check input
    assert all(x.shape == y.shape), 'x and y are not in same dimension!'

    # handle weird case
    if a.size:
        f = []
        return f

    if dim == 0:
        x = x.vflatten()
        y = y.vflatten()
    print(x)
    print(y)

    # do it
    # below is from Kendrick, we should first implement div0
    # f = f = 100*(1 - zerodiv(np.nansum((y-x).^2,dim),np.nansum(y.^2,dim),NaN,0))
    f = 100 * (1 - np.nansum((y - x)**2, dim) / np.nansum(y**2, dim))
    return f
def calccod(x, y, dim, wantgain=0, wantmeansub=1):
    """
    function f = calccod(x,y,dim,wantgain,wantmeansub)

    Args:

    x,y: are both np.array with the same dimensions
    dim (optional) is the dimension of interest.
      default to 2 if <x> is a (horizontal) vector and to 1 if not.
      special case is 0 which means to calculate globally.
    wantgain (optional) is
      0 means normal
      1 means allow a gain to be applied to each case of <x>
        to minimize the squared error with respect to <y>.
        in this case, there cannot be any NaNs in <x> or <y>.
      2 is like 1 except that gains are restricted to be non-negative.
        so, if the gain that minimizes the squared error is negative,
        we simply set the gain to be applied to be 0.
      default: 0.
    wantmeansub (optional) is
      0 means do not subtract any mean.  this makes it such that
        the variance quantification is relative to 0.
      1 means subtract the mean of each case of <y> from both
        x and y before performing the calculation.  this makes
        it such that the variance quantification
        is relative to the mean of each case of <y>.
        note that wantgain occurs before wantmeansub.
      default: 1.

    Notes:
    calculate the coefficient of determination (R^2) indicating
    the percent variance in <y> that is explained by <x>.  this is achieved
    by calculating 100*(1 - sum((y-x).^2) / sum(y.^2)).  note that
    by default, we subtract the mean of each case of <y> from both <x>
    and <y> before proceeding with the calculation.

    the quantity is at most 100 but can be 0 or negative (unbounded).
    note that this metric is sensitive to DC and scale and is not symmetric
    (i.e. if you swap <x> and <y>, you may obtain different results).
    it is therefore fundamentally different than Pearson's correlation
    coefficient (see calccorrelation.m).

    NaNs are handled gracefully (a NaN causes that data point to be ignored).

    if there are no valid data points (i.e. all data points are
    ignored because of NaNs), we return NaN for that case.

    note some weird cases:
      calccod([],[]) is []

    Hstory:
        2017/05/04 - RZ turn it in to python
        2013/08/18 - fix pernicious case where <x> is all zeros and <wantgain>
                    is 1 or 2.
        2010/11/28 - add <wantgain>==2 case
        2010/11/23 - changed the output range to percentages.  thus, the range
                is (-Inf,100].also, we removed the <wantr> input since it was
                dumb.

    Example:
    x = randn(1,100);
    calccod(x,x+0.1*randn(1,100))

    """
    #
    import numpy as np

    # check input
    assert all(x.shape == y.shape), 'x and y are not in same dimension!'

    # handle weird case
    if a.size:
        f = []
        return f

    if dim == 0:
        x = x.vflatten()
        y = y.vflatten()
    print(x)
    print(y)

    # do it
    # below is from Kendrick, we should first implement div0
    # f = f = 100*(1 - zerodiv(np.nansum((y-x).^2,dim),np.nansum(y.^2,dim),NaN,0))
    f = 100 * (1 - np.nansum((y - x)**2, dim) / np.nansum(y**2, dim))
    return f

# %% example
# a = np.random.rand(3, 4)
# b = np.random.rand(3, 4)

# f = calccod(a, b, [], [], 0)
# print(f)
