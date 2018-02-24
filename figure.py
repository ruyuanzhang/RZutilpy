# -*- coding: utf-8 -*-
"""
RZutilpy figure module

@author: ruyuan
"""

'''
default_img_set()
plot()
regplot()
colormap()
colorinterp()
cmapang()
drawcolorbarcircular()

'''


def default_img_set():
    import matplotlib as mpl

    # figure
    mpl.rcParams['figure.frameon'] = False
    mpl.rcParams['figure.titleweight'] = 'regular'
    mpl.rcParams['figure.titlesize'] = 'xx-large'
    mpl.rcParams['figure.autolayout'] = True
    mpl.rcParams['figure.facecolor'] = 'None'
    mpl.rcParams['figure.edgecolor'] = 'None'
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['savefig.frameon'] = False
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['savefig.facecolor'] = 'None'
    mpl.rcParams['savefig.edgecolor'] = 'None'
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    # axes
    mpl.rcParams['axes.facecolor'] = 'None'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.labelsize'] = 'large'
    mpl.rcParams['axes.titleweight'] = 'regular'
    mpl.rcParams['axes.titlesize'] = 'x-large'
    mpl.rcParams['axes.linewidth'] = 2
    mpl.rcParams['xtick.major.width'] = 1.5
    mpl.rcParams['xtick.major.size'] = 6
    mpl.rcParams['xtick.labelsize'] = 'medium'
    mpl.rcParams['ytick.major.width'] = 1.5
    mpl.rcParams['ytick.major.size'] = 6
    mpl.rcParams['ytick.labelsize'] = 'medium'
    mpl.rcParams['lines.linewidth'] = 1.5
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    # Character
    mpl.rcParams['font.family'] = 'Arial'
    mpl.rcParams['font.weight'] = 'bold'
    # legend
    mpl.rcParams['legend.frameon'] = False

    # line


def plot(
    x, y, yerr=None, xerr=None, fmt='', axes=None, lcolor=None, ecolor=None,
    elinewidth=None, capsize=None, barsabove=False, lolims=False,
    uplims=False, xlolims=False, xuplims=False, errorevery=1,
    capthick=None, rtrnum=1, **kwargs):
    '''
    Plot multiple lines and errrobars together.
    Combine plt.plot and plt.errorbar, to make the plot and errorbar whithin
    the same function since plt.errorbar function cannot plot multiple line
    together

    Args:
        We keep all args in plt.errorbar, except that:
        x: a 1D array or 2D array. if 1D, the size should be same as column
            size of y, x.shape[0]= y.shape[0]; if x is 2D, x.shape = y.shape
        y: a 2D array, with each column is a line e.g., y[:,0] is a line
        xerr, yerr: should be dot x line or, dot x line x 2 errorbar. the 3rd
            dimension represent the lower [0] and upper [1] errorbar. when
            x, y is a single line, xerr and yerr can be 1D array
        axes: axes to plot
        lcolor: line color, can be:
            (1) a color map name (e.g., 'gray')
            (2) a color map object
            (3) a list of color list to input for multiple lines. a number of
                colors is default to line numbers.
            (4) a mx3 or mx4 ndarray

            Note that we use rz.figure.colormap to convert color list to a colormap
            object.
            Default: default color prop_cycle

    Return:
        we combine and return all return values from plt.errorbar with three
        ndarray of artist collections, with line object, cap object and line
        collections

    Example:

    plt.close('all')
    x = np.arange(10)
    y = np.random.rand(10)
    yerr = np.random.rand(10,1,2) / 10
    a = rz.figure.plot(x,y,yerr=yerr, fmt='-o')

    plt.close('all')
    x = np.arange(10)
    y = np.random.rand(10, 3)
    yerr = np.random.rand(10,3,2) / 10
    a = rz.figure.plot(x,y,yerr=yerr, fmt='-o')

    Note:
    1. how to check single input data type. Single number should
        still be an array

    History
    2017/12/05 rz add color list function to multiple lines.a

    To do: 1. tease apart line properties

    '''
    import numpy as np
    import matplotlib.pyplot as plt
    import RZutilpy as rz

    # check input, if a single number ,we convert it to array
    # deal with y
    if not isinstance(y, np.ndarray):
        y = np.array(y)
    if y.ndim == 0:
        y = np.array([y])
    # deal with x
    if x is None:
        x = np.arange(y.shape[0])
    else:
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        if x.ndim == 0:
            x = np.array([x])
    # deal with yerr
    if yerr is not None:
        if not isinstance(yerr, np.ndarray):
            yerr = np.array(yerr)
        if yerr.ndim == 0:
            yerr = np.array([yerr])
    # deal with xerr
    if xerr is not None:
        if not isinstance(xerr, np.ndarray):
            xerr = np.array(xerr)
        if xerr.ndim == 0:
            xerr = np.array([xerr])

    # derive axes
    if not axes:
        axes = plt.gca()

    # format x, y, yerr, xerr dimension.
    # We want x,y are dot x lines arrays
    # We want yerr, xerr are dot x lines x 2 arrays
    if y.ndim == 1:  # we only one line
        y = y[:, np.newaxis]
        x = x[:, np.newaxis]
        if yerr is not None:
            if yerr.ndim == 1:
                yerr = yerr[:, np.newaxis, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)  # yerror
            if yerr.ndim != 3:
                raise ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 1:
                xerr = xerr[:, np.newaxis, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            if xerr.ndim != 3:
                raise ValueError('might check xerr dimension')
    else:  # we have multiple lines
        if x.ndim == 1:  # expand x to match size of y
            x = np.tile(x, (y.shape[1], 1)).T
        if yerr is not None:
            if yerr.ndim == 2:
                yerr = yerr[:, :, np.newaxis]
                yerr = np.concatenate((yerr, yerr), 2)
                # now yerror is a dotxlinex2 matrix
            if yerr.ndim != 3:
                raise ValueError('might check yerr dimension')
        if xerr is not None:
            if xerr.ndim == 2:
                xerr = xerr[:, :, np.newaxis]
                xerr = np.concatenate((xerr, xerr), 2)
            if xerr.ndim != 3:
                raise ValueError('might check xerr dimension')

    nline = y.shape[1]
    # now check the x, y shape
    if x.shape != y.shape:
        raise ValueError('incompatible dimension of x,y')
    # check errorbar size
    if yerr is not None and yerr.shape[1] != nline:
        raise ValueError('incompatible dimension of yerr,y')
    if xerr is not None and xerr.shape[1] != nline:
        raise ValueError('incompatible dimension of xerr,y')

    # deal with color
    if lcolor is None:
        lcolor = rz.figure.getdefaultcolorlist()  # get default color cycle
        # convert color list to colormap object
        lcolor = rz.figure.colormap(lcolor, 10 if nline < 10 else nline)
    else:  # input could be a list or a char
        lcolor = rz.figure.colormap(lcolor, nline)

    if ecolor is None:
        ecolor = lcolor
    else:
        ecolor = rz.figure.colormap(ecolor, nline)
    # now ecolor and lcolor should be colormap object

    # initialize lists of return
    line_object = []
    cap_object = []
    linecollection_object = []
    # do it
    for i in range(nline):
        if yerr is None:
            yerrtmp = None
        else:
            yerrtmp = np.transpose(yerr[:, i, :])  # yerr input should be 2xN
        if xerr is None:
            xerrtmp = None
        else:
            xerrtmp = np.transpose(xerr[:, i, :])

        # some keyward variables can receive a list as input to specify individual lines
        errout = axes.errorbar(
            x[:, i], y[:, i], yerrtmp, xerrtmp, fmt=fmt, ecolor=ecolor(i),
            elinewidth=elinewidth, capsize=capsize, barsabove=barsabove,
            lolims=lolims, uplims=uplims, xlolims=xlolims, xuplims=xuplims,
            errorevery=errorevery, capthick=capthick, **kwargs
        )

        # set line color
        errout[0].set_color(lcolor(i))

        line_object.append(errout[0])
        cap_object.append(errout[1])
        linecollection_object.append(errout[2])

    if rtrnum == 1:
        return np.array(line_object)
    elif rtrnum == 2:
        return np.array(line_object), np.array(cap_object)
    if rtrnum == 3:
        return np.array(line_object), np.array(cap_object), \
            np.array(linecollection_object)


def regplot(x, y, axes=None, rtrnum=1, **kwargs):
    '''
    rz's wrapper for the seaborn.regplot function, we add the output for the regression result.
    We return regression result, like p values
    To obtain the objects of lines, shading, scatters, please use axes.get_children() function
    Scatters are PathCollection objects
    Lines are Lines objects
    Shading are PolyCollection objects

    '''
    import seaborn.apionly as sns
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    sns.reset_orig()

    if axes is None:
        axes = plt.gca()
    # do it
    p = sns.regplot(x, y, ax=axes, **kwargs)

    # figure out the statistical model
    if 'order' in kwargs:
        order = kwargs['order']
    else:
        order = 1

    if order > 1:
        regressresult = np.polyfit(x=x, y=y, deg=order)
    else:
        regressresult = stats.linregress(x=x, y=y)

    if rtrnum == 1:
        return regressresult
    elif rtrnum == 2:
        return regressresult, p
    # get the predict data point


def colormap(cmap, nColor=256, vmin=0, vmax=1):
    '''
    colormap(cmap, nColor=256, min=0, max=1):

    function to create a colormap using matplotlib colormaps or update a colormap
    object. We output a LinearSegmentedColormap or a ListedColormap object. Note
    that the LinearSegmentedColormap object does not provide RGBA color array.
    Thus we deliberately add a color array as an attribute if the return is a
    LinearSegmentedColormap.

    Note that we first truncate the color map range from [0, 1] to [vmin, vmax].
    We then linearly interpolate colormap to <nColor> entries

    Input:
        <cmap>: is
            (1) a string, e.g.,'hsv'. Name of the matplotlib colormap. for the
                whole colormap name list, see
                https://matplotlib.org/examples/color/colormaps_reference.html
            (2) a LinearSegmentedColormap or a ListedColormap object
            (3) a list of colors
            (4) a m x 3 or m x 4 color ndarray

            when cmap is a color list and ndarray, please set nColor to the number
            of color input. Otherwise the function will interpolate it into 256
            colors by default

        <nColor>: int, number of color entries
        <min>, <mix>: real numbers between [0, 1], We want to set the min and
            max of the range of the color. e.g., if the original colormap range
            is between [0, 1] and have n colors. We proportionally truncate color
            range to [vmin, vmax], e.g. [0.2, 0.8]
    Output:
        <lcmap>: return a LinearSegmentedColormap or a ListedColormap object since in most cases we need linear interpolation. For LinearSegmentedColormap object, we add a color attribute to store all colors

    Example:
        cmap = rz.figure.colormap('jet', 64)
        cmap = rz.figure.colormap('hot', 64)
        % update a colormap
        cmap = rz.figure.colormap('jet', 64)
        cmap = rz.figure.colormap(cmap, 256)
        % create a colormap

    '''
    from matplotlib import cm
    from matplotlib import colors
    import numpy as np
    import RZutilpy as rz

    if isinstance(cmap, str):
        lcmap = cm.get_cmap(cmap, 1000)
        # get all colors
        allcolors = lcmap(np.arange(1000))  # obtain a 1000 x 4 color list
        vmin = round(vmin * 1000)
        vmax = round(vmax * 1000)
        # get the color range
        allcolors = allcolors[vmin:vmax, :]
        newcolors = rz.figure.colorinterp(allcolors, nColor)
    elif isinstance(cmap, colors.LinearSegmentedColormap) | isinstance(cmap, colors.ListedColormap):
        lcmap = cmap
        allcolors = lcmap(np.arange(lcmap.N))
        vmin = round(vmin * lcmap.N)
        vmax = round(vmax * lcmap.N)
        newcolors = rz.figure.colorinterp(allcolors, nColor)
    elif isinstance(cmap, list) | isinstance(cmap, np.ndarray):
        # first convert the color list to colormap object
        lcmap = colors.ListedColormap(cmap, name='fromlist')
        allcolors = lcmap(np.arange(lcmap.N))
        vmin = round(vmin * lcmap.N)
        vmax = round(vmax * lcmap.N)
        newcolors = rz.figure.colorinterp(allcolors, nColor)
    else:
        raise ValueError('input cmap is not correct')

    # For LinearSegmentedColormap object, we use .from_list function to create a map between input n and output color. so basically we can call e.g. lcmap(0),lcmap(1) to get rgba color. No need to do this for ListedColormap. We simply update the ListedColormap use the newcolors
    if isinstance(lcmap, colors.LinearSegmentedColormap):
        lcmap = lcmap.from_list(lcmap.name, newcolors, nColor)
        lcmap.colors = newcolors
    elif isinstance(lcmap, colors.ListedColormap):
        lcmap = colors.ListedColormap(newcolors)
    else:
        raise ValueError('hm...something wrong...')
    # refresh the colormap
    return lcmap


def getdefaultcolorlist():
    # get the default color cycle list for plot
    import matplotlib.pyplot as plt
    return plt.rcParams['axes.prop_cycle'].by_key()['color']


def colorinterp(cmap, nColor=256):
    '''
    colorinterp(cmap, nColor=256):

    given a colormap <cmap> to resample it and create a new color map. Note that we always include the 1st and last entry of input cmap to newcmap

    Input:
        <cmap>: m x 3 or m x 4 array
        <nColor>: int, number of colors
    Output:
        <newcmap>: m x 3 or m x 4 array, new colormap

    '''
    from scipy import interpolate
    import numpy as np

    if nColor == 1:
        return cmap

    # linearly interpolate these colors
    newcmap = np.zeros((nColor, 4))
    newcmap[:, 3] = 1  # default alpha value is 1
    for i in np.arange(cmap.shape[1]):
        fun = interpolate.interp1d(np.arange(cmap.shape[0]), cmap[:, i])
        newcmap[:, i] = fun(np.linspace(0, cmap.shape[0] - 1, nColor))

    # refresh the colormap
    return newcmap


def drawcolorbarcircular(cmap, nColor=360, mode='angle', imgradius=360):
    '''
    drawcolorbarcircular(cmap, nColor=360, width=1, mode='angle')

    draw a circular colorbar. This is useful when making retinotopic mapping

    <cmap>: is
        (1) a string, which should be a cmap name, e.g.'hsv'
        (2) a m x 3 or m x 4 color array
    <nColor>: int, how many entry you want to draw
    <mode>: a string, should be either 'angle', or 'ecc' indicating circular angle colormap or eccentricity colormap. When drawing angle/eccentricity colormap, consider use circular/sequential colororder
    <imgradius>: the size of the image would be imgsize * 2, default:360

    Example:
    # draw circular angle colormap
    cmap = rz.figure.cmapang();
    rz.figure.drawcolorbarcircular(cmap.colors, 64)
    # draw eccentricity colormap
    rz.figure.drawcolorbarcircular('jet', 64, mode='ecc')

    '''
    import RZutilpy as rz
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Wedge
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap

    # get the colormap
    if isinstance(cmap, str):
        cmapobj = rz.figure.colormap(cmap, nColor)
    elif isinstance(cmap, np.ndarray):
        if cmap.shape[0] != nColor:
            cmap = rz.figure.colorinterp(cmap, nColor)
            # we build an object
        cmapobj = LinearSegmentedColormap.from_list('rzcolormap', cmap, N=nColor)
        cmapobj.colors = cmap
    elif isinstance(cmap, LinearSegmentedColormap) | isinstance(cmap, ListedColormap):
        cmapobj = rz.figure.colormap(cmap, nColor)  # update color map object

    angle = np.linspace(0, 360, nColor + 1)
    r = np.linspace(0, imgradius, nColor + 1)
    width = r[1] - r[0]

    fig, ax = plt.subplots()
    if mode == 'angle':
        for i in np.arange(nColor):
            ax.add_patch(Wedge((0, 0), imgradius, angle[i], angle[i + 1], color=cmapobj(i)))
    elif mode == 'ecc':
        for i in np.arange(nColor):
            ax.add_patch(Wedge((0, 0), r[i + 1], 0, 360, width=width, color=cmapobj(i)))
    else:
        raise ValueError('We can only plot angle and ecc map')
    # set the ax
    plt.setp(ax, ylim=[-imgradius * 1.1, imgradius * 1.1], xlim=[-imgradius * 1.1, imgradius * 1.1])
    ax.axis('equal')
    return ax, cmapobj


def cmapang():
    '''
    cmapang():

    same as cmapang in knkutil/colormap. we make a circular colormap but force it only has 64 entries. will retun a m x 4 color matrix

    TODO: consider return an colormap object

    '''
    import numpy as np
    from RZutilpy.figure import colorinterp
    from matplotlib.colors import hsv_to_rgb, LinearSegmentedColormap

    n = 64
    colors = [[0 / 360, 1, 1],  # red
        [30 / 360, 1, 1],      # orange
        [60 / 360, 1, .92],    # yellow
        [105 / 360, 1, .9],    # green
        [180 / 360, 1, .9],    # light-blue
        [240 / 360, 1, .9],    # blue
        [280 / 360, 1, .75],   # purple
        [305 / 360, 1, .82],   # magenta
        [1, 1, 1]]  # red
    colors = np.array(colors)  # convert to np.array

    # upsample
    cmap = colorinterp(colors, n + 1)
    cmap = cmap[:-1, :]  # remove the last entry

    # do some fine-scale adjustment
    cmap[1:9, :] = colorinterp(np.vstack((cmap[2, :], cmap[8, :])), 8)

    # 1+8+8+8 = 25
    cmap[24:33, :] = np.vstack((cmap[24, :], cmap[25, :], colorinterp(np.vstack((cmap[28, :], cmap[32, :])), 7)))

    # % %1+8+8+8+8+8 = 41
    cmap[40:49, :] = np.vstack((cmap[40, :], colorinterp(
        np.vstack((np.mean(cmap[41:43, :], 0), cmap[48, :])), 8)))
    # % %1+8+8+8+8+8+8 = 49
    cmap[48:57, :] = np.vstack((colorinterp(np.vstack((cmap[48, :], cmap[54, :])), 8), cmap[56, :]))

    cmap[:, :3] = hsv_to_rgb(cmap[:, :3])

    if cmap.ndim == 3:
        cmap = np.hstack(cmap, np.ones((cmap.shape[0])).T)

    # turn it a LinearSegmentedColormap object
    cmapobj = LinearSegmentedColormap.from_list('cmapang', cmap, N=64)
    cmapobj.colors = cmap

    return cmapobj


def cmapang2(nColor=360):
    '''
    cmapang2():

    rz's second circular colormap. We use cmocean package and use cmocean.cm.phase as the base. We update this object and return it
    '''
    from cmocean.cm import phase
    from RZutilpy.figure import colormap

    return colormap(phase, nColor=nColor)



