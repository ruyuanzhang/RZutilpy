# RZ's math module


def posrect(x):
    '''
    postive reactify t


    he matrix number
    x is a ndarray
    '''
    x[x < 0] = 0
    return x


def normalizerange(m, targetmin, targetmax, sourcemin=None, sourcemax=None, chop=1, mode=0):
    '''
    normalizerange(m, targetmin, targetmax, sourcemin=None, sourcemax=None, chop=1, mode=0)

    return <m> scaled and translated such that [<sourcemin>,<sourcemax>] maps to
    [<targetmin>,<targetmax>].  if <chop>, we also threshold values below <targetmin>
    and values above <targetmax>.

    Args:
        m: is a 2d numpy array.
        targetmin: is the minimum desired value.  can be a scalar or an array the same size as <m>.
        targetmax: is the maximum desired value.  can be a scalar or an array the same size as <m>.
        sourcemin: (optional) sets the min value of <m>.  can be a scalar or a matrix the same size as <m>.
            default is [], which means to find the actual minimum.  special case is NaN which means -nanmax(abs(m(:))).
        sourcemax: sets the max value of <m>.  can be a scalar or a matrix the same size as <m>.
            default is [], which means to find the actual maximum.  special case is NaN which means nanmax(abs(m(:))).
        chop:is whether to chop off the ends such that there are no values below <targetmin> nor above <targetmax>.  default: 1.
        mode: is
            0 means normal operation
            1 means interpret <sourcemin> and <sourcemax> as multipliers for the std of m(:).
            in this mode, the default for <sourcemin> and <sourcemax> is -3 and 3, respectively,
            which means to use mn-3*sd and mn+3*sd for the min and max value of <m>, respectively.
            note that in this mode, <sourcemin> and <sourcemax> cannot be NaN.
            default: 0.
        # fast: means we have a guarantee that all inputs are fully specified and <m> is not empty.

    Return:
        normalized m

    Example:
        normalizerange([1 2 3],0,1) = np.array([0, 1/2, 1])
        isequal(normalizerange([1 2 3],0,1,2,3,1),[0 0 1])
        isequalwithequalnans(normalizerange([1 2 NaN],0,1,0,4),[1/4 2/4 NaN])

    Note:
        1. note that if <sourcemin> is ever equal to <sourcemax>, then we die with an error.
        2. note that <chop> has no effect if <sourcemin> and <sourcemax> aren't specified.
        3. we deal with NaNs in <m> gracefully.
        4. if <fast>, skip stuff for speed
    '''

    import numpy as np
    import RZutilpy as rz

    # check empty case
    if rz.math.isempty(m):
        return m

    assert isinstance(m, np.ndarray), 'Input is not a numpy array'

    skipchop = (mode == 0 & (sourcemin is None) & (sourcemax is None)) | (mode == 0 & rz.math.isnan(sourcemin) & rz.math.isnan(sourcemax))

    if mode == 0:
        if not sourcemin:
            sourcemin = np.nanmin(m)
        if not sourcemax:
            sourcemax = np.nanmax(m)
        if rz.math.isnan(sourcemin) | rz.math.isnan(sourcemax):
            temp = np.nanmax(np.abs(m))
            if rz.math.isnan(sourcemin):
                sourcemin = -temp
            if rz.math.isnan(sourcemax):
                sourcemax = -temp
    elif mode == 1:
        if not sourcemin:
            sourcemin = -3
        if not sourcemax:
            sourcemax = 3
        mn = np.mean(m)
        sd = np.std(m)
        sourcemin = mn + sourcemin * sd
        sourcemax = mn - sourcemax * sd

    # sanity check
    assert sourcemin != sourcemax, "sourcemin and sourcemax are the same in at least one case"

    # go ahead and chop
    if chop & (not skipchop):
        temp = rz.math.isnan(m)
        m[m < sourcemin] = sourcemin
        m[m > sourcemax] = sourcemax
        m[temp] = nan   # preserve NaNs

    # want to do: f = (m-sourcemin) .* (targetmax-targetmin)./(sourcemax-sourcemin) + targetmin
    val = (targetmax - targetmin) / (sourcemax - sourcemin)
    return m * val - (sourcemin * val - targetmin)   # like this for speed


def isempty(a):
    '''
    wrapper of np.isnan, np.isnan cannot take None object

    a can be number, string, list, dict, set, np.array, None
    Note that if a is none, we retur true
    '''
    import numpy as np
    if isinstance(a, np.ndarray):
        return a.size == 0
    else:
        if a:
            return False
        else:
            return True


def isnan(a):
    '''
    wrapper for np.isnan
    a can be number, list, np.array, none
    '''
    import numpy as np
    if a is None:
        return False
    else:
        return np.isnan(a)


def zerodiv(x, y, val=0):
    '''
    zerodiv(x, y, val=0)

    <x><y> are same dimension. divide if <y> is 0, then use <val>. <val> default is 0

    '''
    import RZutilpy as rz
    valid = ~(rz.math.isnan(y) | (y == 0))
    f = x[valid] / y[valid]
    f[~valid] = val
    return f


def calccod(x, y, dim=0, wantmeansub=True):
    '''
    calccod(x, y, dim=0, wantgain=False, wantmeansub=False):

    calculate the coefficient of determination (R^2) indicating
    the percent variance in <y> that is explained by <x>.  this is achieved
    by calculating 100*(1 - sum((y-x).^2) / sum(y.^2)).  note that
    by default, we subtract the mean of each case of <y> from both <x>
    and <y> before proceeding with the calculation.

    the quantity is at most 100 but can be 0 or negative (unbounded).
    note that this metric is sensitive to DC and scale and is not symmetric
    (i.e. if you swap <x> and <y>, you may obtain different results).
    it is therefore fundamentally different than Pearson's correlation
    coefficient (see calccorrelation.m).

    NaNs are handled gracefully (a NaN causes that data point to be ignored).

    Input:
        <x>,<y>: np array with same dimension
        <dim>: which dimension to work on;
        <wantmeansub>:
            0 means do not subtract any mean.  this makes it such that
            the variance quantification is relative to 0.
            1 means subtract the mean of each case of <y> from both
            <x> and <y> before performing the calculation.  this makes
            it such that the variance quantification
            is relative to the mean of each case of <y>.
            note that <wantgain> occurs before <wantmeansub>.
   different efault: 1.

    '''
    # deal with nan
    import numpy as np
    import RZutilpy as rz

    x[rz.math.isnan(y)] = np.nan
    y[rz.math.isnan(x)] = np.nan

    # handel mean substraction
    if wantmeansub:
        mn = np.nanmean(y, axis=dim)
        y = y - mn
        x = x - mn

    # do it
    f = 100 * (1 - rz.math.zerodiv(np.nansum((y - x)**2, dim), np.nansum(y ** 2, dim), np.nan))

    return f


def calccorrelation(x, y):
    '''
    calculate correlation. use stats.linregresss
    '''
    from scipy import stats
    return stats.linregress(x, y)


class fitnonlinearmodel:
    def __init__(self, fitopt):
        self.fitopt = fitopt
        self.model = fitopt['model']
        self.x = fitopt['x']
        self.y = fitopt['y']
        self.optresult = optimize(self)

    def optimize(self):   # optimize the model
        import scipy.optimize as opt
        opt.least_squares(self.model, x0, bounds=(-inf, inf))

        return

