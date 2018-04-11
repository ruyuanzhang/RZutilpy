def calccorrelation(x, y):
    '''
    calculate correlation. use stats.linregresss
    '''
    from scipy import stats
    return stats.linregress(x, y)