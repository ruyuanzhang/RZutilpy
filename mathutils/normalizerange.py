def normalizerange(m, targetmin, targetmax, sourcemin=None, sourcemax=None, chop=True, mode=0):
    '''
    normalizerange(m, targetmin, targetmax, sourcemin=None, sourcemax=None, chop=1, mode=0)

    return <m> scaled and translated such that (<sourcemin>,<sourcemax>) maps to
    (<targetmin>,<targetmax>).  if <chop>, we also threshold values below <targetmin>
    and values above <targetmax>.

    Args:
        m: is a ndaray.
        targetmin: is the minimum desired value.  can be a scalar or an array the same size as <m>.
        targetmax: is the maximum desired value.  can be a scalar or an array the same size as <m>.
        sourcemin: (optional) sets the min value of <m>.  can be a scalar or a matrix the same size as <m>.
            default is [], which means to find the actual minimum.  special case is NaN which means -nanmax(abs(m(:))).
        sourcemax: sets the max value of <m>.  can be a scalar or a matrix the same size as <m>.
            default is [], which means to find the actual maximum.  special case is NaN which means nanmax(abs(m(:))).
        chop: boolean, whether to chop off the ends such that there are no values below <targetmin> nor above <targetmax>.  default: True.
        mode: is
            0 (default) means normal operation
            1 means interpret <sourcemin> and <sourcemax> as multipliers for the std of m(:).
            in this mode, the default for <sourcemin> and <sourcemax> is -3 and 3, respectively,
            which means to use mn-3*sd and mn+3*sd for the min and max value of <m>, respectively.
            note that in this mode, <sourcemin> and <sourcemax> cannot be NaN.

        # fast: means we have a guarantee that all inputs are fully specified and <m> is not empty.

    Return:
        normalized m

    Example:
        normalizerange(np.array([1, 2, 3]),0,1) = np.array([0, 1/2, 1])
        normalizerange(np.array([1, 2, 3]),0,1,2,3,1) == [0 0 1])
        normalizerange(np.array([1, 2, NaN]),0,1,0,4)== [1/4 2/4 NaN]

    Note:
        1. note that if <sourcemin> is ever equal to <sourcemax>, then we die with an error.
        2. note that <chop> has no effect if <sourcemin> and <sourcemax> aren't specified.
        3. we deal with NaNs in <m> gracefully.
        4. if <fast>, skip stuff for speed
        5. Note that m cannot be a number, please arrayfy it
    '''

    import numpy as np
    import RZutilpy as rz

    # check input
    assert isinstance(m, np.ndarray), 'Input should be a ndarray'

    skipchop = (mode == 0 and (sourcemin is None) and (sourcemax is None)) | (mode == 0 and rz.math.isnan(sourcemin) and rz.math.isnan(sourcemax))

    if mode == 0:
        if sourcemin is None:
            sourcemin = np.nanmin(m)
        if sourcemax is None:
            sourcemax = np.nanmax(m)
        if rz.math.isnan(sourcemin) | rz.math.isnan(sourcemax):
            temp = np.nanmax(np.abs(m))
            if rz.math.isnan(sourcemin):
                sourcemin = -temp
            if rz.math.isnan(sourcemax):
                sourcemax = -temp
    elif mode == 1:
        if sourcemin is None:
            sourcemin = -3
        if sourcemax is None:
            sourcemax = 3
        mn = np.mean(m)
        sd = np.std(m)
        sourcemin = mn + sourcemin * sd
        sourcemax = mn - sourcemax * sd

    # sanity check
    assert sourcemin != sourcemax, "sourcemin and sourcemax are the same in at least one case"

    # go ahead and chop
    if chop and (not skipchop):
        #temp = rz.math.isnan(m)
        m[m < sourcemin] = sourcemin  # this can be done with nan
        m[m > sourcemax] = sourcemax  # this can be done with nan
        #m[temp] = np.nan   # preserve NaNs

    # want to do: f = (m-sourcemin) .* (targetmax-targetmin)./(sourcemax-sourcemin) + targetmin
    val = (targetmax - targetmin) / (sourcemax - sourcemin)
    return m * val - (sourcemin * val - targetmin)   # like this for speed