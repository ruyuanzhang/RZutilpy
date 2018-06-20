def calccod(x, y, dim=0, wantmeansub=True):
    '''
    calccod(x, y, dim=0, wantmeansub=True):

    calculate the coefficient of determination (R^2) indicating
    the percent variance in <y> that is explained by <x>.  this is achieved
    by calculating 100*(1 - sum((y-x).^2) / sum((y).^2)).  note that
    by default, we subtract the mean of each case of <y> from both <x>
    and <y> before proceeding with the calculation.

    the quantity is at most 100 but can be 0 or negative (unbounded).
    note that this metric is sensitive to DC and scale and is not symmetric
    (i.e. if you swap <x> and <y>, you may obtain different results).
    it is therefore fundamentally different than Pearson's correlation
    coefficient (see calccorrelation.m).

    NaNs are handled gracefully (a NaN causes that data point to be ignored).

    Input:
        <x>,<y>: ndarray with same dimension
        <dim>: int which dimension to work on;
        <wantmeansub>: boolean
            False means do not subtract any mean.  this makes it such that
            the variance quantification is relative to 0.
            True means subtract the mean of each case of <y> from both
            <x> and <y> before performing the calculation.  this makes
            it such that the variance quantification
            is relative to the mean of each case of <y>.
            note that occurs before <wantmeansub>.

    '''
    # deal with nan
    from numpy import isnan, nansum, nanmean,NaN
    from RZutilpy.math import zerodiv

    x[isnan(y)] = np.nan
    y[isnan(x)] = np.nan

    # handle mean substraction
    if wantmeansub:
        mn = nanmean(y, axis=dim)
        y = y - mn
        x = x - mn

    # do it
    f = 100 * (1 - zerodiv(nansum((y - x)**2, dim), nansum(y ** 2, dim), np.nan))

    return f