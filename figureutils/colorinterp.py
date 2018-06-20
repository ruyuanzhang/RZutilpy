def colorinterp(cmap, nColor=256):
    '''
    colorinterp(cmap, nColor=256):

    given a colormap array <cmap>, interpolate it and create a new color map.
    Note that we always include the 1st and last entry of input cmap to <newcmap>

    Input:
        <cmap>: m x 3 or m x 4 array
        <nColor>: int, number of colors
    Output:
        <newcmap>: m x 4 array, new colormap

    '''
    from scipy import interpolate
    from numpy import zeros, arange, linspace

    if nColor == 1:
        return cmap

    # linearly interpolate these colors
    newcmap = np.zeros((nColor, 4))
    newcmap[:, 3] = 1  # default alpha value is 1
    for i in arange(cmap.shape[1]):
        fun = interpolate.interp1d(arange(cmap.shape[0]), cmap[:, i])
        newcmap[:, i] = fun(linspace(0, cmap.shape[0] - 1, nColor))

    # refresh the colormap
    return newcmap