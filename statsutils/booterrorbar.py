def booterrorbar(
    x, metric='mean', errorFormat='single', prcntage=68, nBoot=1000, rtrnum=1,
):
    '''
    Use bootstrap to estimate errorbar
    Args:
        x: a vector, we will flatten it a 1d vector
       metric(opt): a string, specify 'mean'(default),
            'median','nanmean','nanmedian'
       errorFormat: a string:
           'single': (default) return a single number,half of the range between
               low/up range.
           'bound': return two number, upper and lower bound
            prcntage: e.g. 95, 95% confidence interval, default:68
       nBoot: number of bootstrap samples, default:1000
       returnnum: index in return turple to return. e.g., return rtrtupler[:rtrnum]
    return
        er: a scalar, if errorFormat == 'single'
            a two element vector,if errorFormat = 'bound'. represent the lower
            and uppder offset
        samples: bootstrap samples, can be a list or a nd.array
    '''
    import numpy as np
    x = np.array(x).flatten()  # convert it to flattend array;
    if any(np.isnan(x)):
        print('detect nan value, use nanmean or nanmedian')
        if metric == 'mean':
            metric = 'nanmean'
        elif metric == 'median':
            metric = 'nanmedian'
    samples = bootresamplemulti(x, nBoot)  # get bootstrap samples
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
    # compute target prcntage
    prcntage = np.array([(100 - prcntage) / 2, 100 - (100 - prcntage) / 2])
    # get bound
    er = np.percentile(tmp, prcntage)
    if errorFormat == 'single':
        er = (np.diff(er) / 2)[0]
    elif errorFormat == 'bound':
        er = np.array([tmp2 - er[0], er[1] - tmp2])

    if rtrnum == 1:
        return er
    elif rtrnum == 2:
        return er, samples