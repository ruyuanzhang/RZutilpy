def ttest(x, y=None, fmt='ind', equal_var=True, nan_policy='propagate', popmean=0):
    '''
    Run ttest on 1d array x and y

    This function is based on scipy.stats functions ttest_ind, ttest_1sample, ttest_rel
    We also included degree of freedom and effect size, cohen's d

    Input:
        <x><y>: 1D array, <y> is optinal if 1sample ttest
        <fmt>: format of ttest, optinal
            'ind': independent sample ttest
            'rel': related or paired sample ttest
            '1samp': one-sample test
        <equal_var>: bool, in independent-sample ttest, whether variance are equal
        <nan_policy>: {‘propagate’, ‘raise’, ‘omit’}, in paired-ttest, optional
            Defines how to handle when input contains nan. ‘propagate’ returns nan, ‘raise’ throws an error, ‘omit’ performs the calculations ignoring nan values. Default is ‘propagate’.
        <popmean>: population mean of null hypothesis in 1samp ttest    

    Output: tuple(rslt, df, cohend)

        <rslt>: ttest structure
        <df>: degree of freedom
        <cohend>: cohend effect size


    '''
    import numpy as np
    from scipy.stats import ttest_ind, ttest_1samp, ttest_rel
    from RZutilpy.stats import cohend

    if not isinstance(x, np.ndarray):
        raise ValueError('Please input a np.ndarray')

    if fmt=='ind': # independent two sample ttest
        if not isinstance(y, np.ndarray):
            raise ValueError('Please input a np.ndarray')
        rslt = ttest_ind(x, y, equal_var=equal_var)
        df = x.size + y.size - 2
        ef = cohend(x, y)
    elif fmt=='rel': # paired ttest
        if not isinstance(y, np.ndarray):
            raise ValueError('Please input a np.ndarray')
        rslt = ttest_rel(x, y, nan_policy=nan_policy)
        assert x.size == y.size, ValueError('two array should have the same size for paired ttest')
        df = x.size - 1
        ef = cohend(x, y)
    elif fmt=='1samp': # one sample ttest
        rslt = ttest_1samp(x, popmean=popmean)
        df = x.size - 1
        ef = cohend(x, popmean*np.ones(x.size))
    else:
        raise ValueError("fmt can only be 'ind', 'rel', '1samp' ")
    return (rslt, df, ef)

