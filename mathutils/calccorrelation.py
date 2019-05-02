def calccorrelation(x, y):
    '''
    calculate correlation. use scipy.stats.linregresss.

    Note that we output the full result from scipy.stats.linregresss function, including
    slope,intercept, rvalue, pvalue and stderr.

    to do:
        1. normalize data
    '''

    from scipy import stats
    return stats.linregress(x, y)