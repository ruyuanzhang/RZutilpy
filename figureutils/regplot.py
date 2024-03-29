def regplot(x, y, axes=None, rtrnum=1, **kwargs):
    '''
    rz's wrapper for the seaborn.regplot function, we add the output for the regression result.
    We return regression result, like p values
    To obtain the objects of lines, shading, scatters, please use axes.get_children() function

    Scatters are PathCollection objects
    Lines are Lines objects
    Shading are PolyCollection objects

    '''
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    sns.reset_orig() #

    if axes is None:
        axes = plt.gca()
    # do it
    p = sns.regplot(x=x, y=y, ax=axes, **kwargs)

    # figure out the statistical model
    if 'order' in kwargs:
        order = kwargs['order']
    else:
        order = 1
    
    # deal with Nan value
    nanind = np.isnan(x) | np.isnan(y)

    if order > 1:
        regressresult = np.polyfit(x=x[~nanind], y=y[~nanind], deg=order)
    else:
        regressresult = stats.linregress(x=x[~nanind], y=y[~nanind])

    if rtrnum == 1:
        return regressresult
    elif rtrnum == 2:
        return regressresult, p
    # get the predict data point