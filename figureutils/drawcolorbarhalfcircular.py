def drawcolorbarhalfcircular(cmap, nColor=180, mode='angle', imgradius=360):
    '''
    drawcolorbarhalfcircular(cmap, nColor=180, mode='angle', imgradius=360):

    draw a circular colorbar. This is useful when making retinotopic mapping

    <cmap>: is
        (1) a string, which should be a cmap name, e.g.'hsv'
        (2) a m x 3 or m x 4 color array
    <nColor>: int, how many entry you want to draw
    <mode>: a string, should be either 'angle', or 'ecc' indicating circular angle colormap or eccentricity colormap. When drawing angle/eccentricity colormap, consider use circular/sequential colororder
    <imgradius>: the size of the image would be imgsize * 2, default:360

    Note that the color order starts from 12 clock and counter-clockwise moves to
    6 clock

    Example:
    # draw circular angle colormap
    cmap = rz.figure.cmapang();
    rz.figure.drawcolorbarhalfcircular(cmap.colors, 64)
    # draw eccentricity colormap
    rz.figure.drawcolorbarhalfcircular('jet', 64, mode='ecc')

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

    angle = np.linspace(0, 180, nColor + 1)
    r = np.linspace(0, imgradius, nColor + 1)
    width = r[1] - r[0]

    fig, ax = plt.subplots()
    if mode == 'angle':   # note that Wedge, angle start (0) from 3 clock and CCW increment
        for i in np.arange(nColor):
            ax.add_patch(Wedge((0, 0), imgradius, angle[i], angle[i + 1], color=cmapobj(i)))
    elif mode == 'ecc':
        for i in np.arange(nColor):
            ax.add_patch(Wedge((0, 0), r[i + 1], 90, -90, width=width, color=cmapobj(i)))
    else:
        raise ValueError('We can only plot angle and ecc map')
    # set the ax
    plt.setp(ax, ylim=[-imgradius * 1.1, imgradius * 1.1], xlim=[-imgradius * 1.1, imgradius * 1.1])
    ax.spines['left'].set_position('center')
    ax.get_xaxis().set_visible(False)
    ax.yaxis.set_ticks_position('right')
    ax.yaxis.set_ticks([-360, 360])
    #ax.yaxis.set_ticklabels(['', '180','', '','90','','','0'])
    ax.axis('equal')
    return ax, cmapobj