#  RZ' stats


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


def bootresamplemulti(x, nBoot=1000, rtrnum=1):
    '''
    %
    % resample an vector for bootstrap. We assume input is a long vertical
    % vector,then we generate nboot columes as the result. remember. this
    % is sample with replacement.
    %
    % Args:
    %   x: we flatten the x, x can be an array or a list
    %   nboot: how many samples we want,default is 1000
    %   rtrnum: number of returned variable, default is 1,
    %        (only return 1 variable)
    % Return:
    %   sample:a x.size X nboot matrix, each column is a sample
    %   ind: x.size X nboot matrix, each columen is a sample. value is the
    %       index in original input, ind must be int
    % Note:
    %   1. it assumes sample with replacement
    %   2. cell case is OK
    %
    % Example:
    % [sample,ind] = rz.bootresamplemulti(rand(10,1),500);
    % isequal(size(sample),[10,500])
    '''
    import numpy as np
    x = np.array(x).flatten()  # convert to array and flatten
    ind = np.floor(
        np.random.rand(x.size, nBoot) * x.size
    ).astype(int)  # as index shoule be int

    sample = x[ind]

    if rtrnum == 1:
        return sample
    elif rtrnum == 2:
        return sample, ind


def sem(x, axis=0):
    '''
    compute standard error of a numpy array


    Note, we automatically deal with nans

    '''

    # check input
    import numpy as np
    if not isinstance(x, np.ndarray):
        raise ValueError('Please input a np.ndarray')
    num = x.shape[axis]

    # deal with nan value
    nanidx = np.isnan(x)
    num = num - np.sum(nanidx, axis=axis)
    return np.nanstd(x, axis=axis) / np.sqrt(num)


