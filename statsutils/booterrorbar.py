def booterrorbar(x, metric='mean', errorFormat='single', prcnt=68, nBoot=1000):
    '''
    booterrorbar(x, metric='mean', errorFormat='single', prcnt=68, nBoot=1000)

    Use bootstrap to estimate errorbar. We detect nan values and if input contains nan values
    we use np.nanmean or np.nanmedian to avoid that

    Args:
        <x>: a 1d array. If not, we will flatten it a 1d vector
        <metric>(opt): a string, specify 'mean'(default),
            'median','nanmean','nanmedian'
        <errorFormat>: a string:
           'single': (default) return a single number,half of the range between
               lower/upper bound.
           'bound': return two number, upper and lower bound
        <prcnt>: e.g. 95, 95% confidence interval, default:68
        <nBoot>: number of bootstrap samples, default:1000
    return
        <er>:
            1. a scalar, if errorFormat == 'single'
            2. a two element vector,if errorFormat = 'bound'. represent the lower
            and uppder offset

        <samples>: bootstrap samples, can be a list or a nd.array

    Examples:

    '''

    import numpy as np
    from RZutilpy.stats import bootresamplemulti

    assert isinstance(x,np.ndarray), 'Input should be a ndarray'

    x = x.flatten()  # convert it to flattend array;

    # deal with nan
    if any(np.isnan(x)):
        print('detect nan value, use nanmean or nanmedian')
        if metric == 'mean':
            metric = 'nanmean'
        elif metric == 'median':
            metric = 'nanmedian'

    samples, _ = bootresamplemulti(x, nBoot)  # get bootstrap samples

    if metric == 'mean':
        tmp = np.mean(samples, axis=0)
        tmp2 = np.mean(x, axis=0)
    elif metric == 'median':
        tmp = np.median(samples, axis=0)
        tmp2 = np.median(x, axis=0)
    elif metric == 'nanmean':
        tmp = np.nanmean(samples, axis=0)
        tmp2 = np.nanmean(x, axis=0)
    elif metric == 'nanmedian':
        tmp = np.nanmedian(samples, axis=0)
        tmp2 = np.nanmedian(x, axis=0)

    # compute target prcnt
    prcnt = np.array([(100 - prcnt) / 2, 100 - (100 - prcnt) / 2])

    # get bound
    er = np.percentile(tmp, prcnt)

    if errorFormat == 'single':
        er = (np.diff(er) / 2)[0]
    elif errorFormat == 'bound':
        er = np.array([tmp2 - er[0], er[1] - tmp2])

    return er, samples