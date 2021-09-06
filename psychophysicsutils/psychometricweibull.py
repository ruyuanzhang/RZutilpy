def psychometricweibull(x, threshold, slope=2, thresholdaccu=0.82, chance=0.5, lapse=0, scale='linear'):
    '''
    psychmetricweibull(x,threshold,slope,thresholdaccu,chance,lapse,scale, format)

    Compute probability of correct a sequence of independent response based on weibull
    psychometric function. 
    Please convert contrast from 0-1 to 0-100.

    Input:
    <x>: a scalar of an array. input x data, can be a scale or a array.
    <threshold>: a scalar, threshold of this psychometric function, corresponding to
                the <thresholdaccu> 
    <slope>: slope of psychmetric curve, default: 2
    <thresholdaccu>: the accuracy level corresponding to threshold, e.g. 0.82;
    <chance>: chance level probablity,e.chance. 0.5 for 2 alternative
            forcechoice,default is 0.5.
    <lapse>(optional): lapse of psychmetric function. In some cases,
            maxima of psychometric function is not 1. Consider lapse, it
            should be 1-lapse. default is 0.
    scale(optional): default: 'linear', psymetric function in linear or log scale
        'linear': linear scale
        'log': log scale, we transform threshold and all stimulus input
            to log space. We assume all threshold and stimulus
            input is bigger than 1. For some variable less than 1,
            like contrast (0,1), we use
    
    We output the <prob>, the probility of corrsponding to input x, can be a scalar and an
        array

    Example
    x=0:0.1:10;
    plt.plot(psychmetricweibull(x,5,2));
    '''

    from numpy import log, exp, all, finfo

    # check input
    assert (chance>=0 & (chance<=1)) # chance level should be within (0,1)
    assert thresholdaccu >= chance # threshold accuracy should >= chance
    assert lapse >= 0# lapse should >=0
    assert all(x > 0),'Weibull function requires that all stimulus intensities >0' # in log scale all input should be > 1, for values smaller than 1, like contrast, we use linear space.

    # transform to log space
    if scale == 'log':
        x = log(x)
        threshold = log(threshold)
    #
    k = (-log((1-thresholdaccu)/(1-chance)))**(1/slope)
    prob = 1- lapse - (1 - chance - lapse)*exp(-(k*x/threshold) ** slope) # hack here to avoid the complex number of power operation

    # avoid small negative number
    if prob.size > 1:
        prob[prob<0] = 0
        prob[prob>1] = 1

    return prob*0.99 + finfo(float).eps 
