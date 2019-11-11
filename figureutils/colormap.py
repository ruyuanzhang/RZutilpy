def colormap(cmap, nColor=256, vmin=0, vmax=1, keeplast=False):
    '''
    colormap(cmap, nColor=256, vmin=0, vmax=1):

    Create a colormap object using matplotlib colormaps or update a colormap
    object. Output is a LinearSegmentedColormap or a ListedColormap object. Note
    that the LinearSegmentedColormap object does not contain RGBA colors array.
    Thus we deliberately add a color array as an attribute if the return is a
    LinearSegmentedColormap.

    Note that we first truncate the color map range from [0, 1] to [vmin, vmax].
    We then linearly interpolate colormap to <nColor> entries

    Input:
        <cmap>: is
            (1) a string, e.g.,'hsv'. Name of the matplotlib colormap. for the
                whole colormap name list, see
                https://matplotlib.org/examples/color/colormaps_reference.html
            (2) a LinearSegmentedColormap or a ListedColormap object. In this case
                we update the input colormap object
            (3) a list of colors
            (4) a m x 3 or m x 4 color array

            when cmap is a color list (case 3) and ndarray (case 4), please set nColor
            to the number of color input. Otherwise the function will interpolate it into 256
            colors by default

        <nColor>: int, number of color entries,default:256
        <min>, <mix>: real numbers between [0, 1], We want to set the min and
            max of the range of the color. e.g., if the original colormap range
            is between [0, 1] and have n colors. We proportionally truncate color
            range to [vmin, vmax], e.g. [0.2, 0.8]
        <keeplast>:whether to keep last entry when interpolate color, default:False
    Output:
        <lcmap>: return a LinearSegmentedColormap or a ListedColormap object
            since in most cases we need linear interpolation.
            For LinearSegmentedColormap object, we add a 'color' attribute to store all colors

    Examples:
        # create a colormap from default matplotlib colormaps
        cmap = rz.figure.colormap('jet', 64)
        cmap = rz.figure.colormap('hot', 64)
        # update a colormap
        cmap = rz.figure.colormap('jet', 64)
        cmap = rz.figure.colormap(cmap, 256)

    '''
    from matplotlib import cm
    from matplotlib import colors
    from numpy import arange, ndarray
    from RZutilpy.figure import colorinterp

    if isinstance(cmap, str):
        lcmap = cm.get_cmap(cmap, 1000)
        # get all colors
        allcolors = lcmap(arange(1000))  # obtain a 1000 x 4 color list
        vmin = round(vmin * 1000)
        vmax = round(vmax * 1000)
        # get the color range
        allcolors = allcolors[vmin:vmax, :]
        newcolors = colorinterp(allcolors, nColor, keeplast)
    elif isinstance(cmap, colors.LinearSegmentedColormap) | isinstance(cmap, colors.ListedColormap):
        lcmap = cmap
        allcolors = lcmap(arange(lcmap.N))
        vmin = round(vmin * lcmap.N)
        vmax = round(vmax * lcmap.N)
        newcolors = colorinterp(allcolors, nColor, keeplast)
    elif isinstance(cmap, list) | isinstance(cmap, ndarray):
        # first convert the color list to colormap object
        lcmap = colors.ListedColormap(cmap, name='fromlist')
        allcolors = lcmap(arange(lcmap.N))
        vmin = round(vmin * lcmap.N)
        vmax = round(vmax * lcmap.N)
        newcolors = colorinterp(allcolors, nColor, keeplast)
    else:
        raise ValueError('input cmap is incorrect')

    # For LinearSegmentedColormap object, we use .from_list function to create
    # a map between input n and output color. so basically we can call
    # e.g. lcmap(0),lcmap(1) to get rgba color.
    # No need to do this for ListedColormap. We simply update the ListedColormap use the newcolors

    if isinstance(lcmap, colors.LinearSegmentedColormap):
        lcmap = lcmap.from_list(lcmap.name, newcolors, nColor)
        lcmap.colors = newcolors
    elif isinstance(lcmap, colors.ListedColormap):
        lcmap = colors.ListedColormap(newcolors)
    else:
        raise ValueError('hm...something wrong...')
    # refresh the colormap
    return lcmap