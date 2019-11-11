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

    Note that the color order starts from 3 clock and counter-clockwise moves to
    3clock again.

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
        cmapobj = rz.figure.colormap(cmap, nColor, False)
    elif isinstance(cmap, np.ndarray):
        if cmap.shape[0] != nColor:
            cmap = rz.figure.colorinterp(cmap, nColor, False)
            # we build an object
        cmapobj = LinearSegmentedColormap.from_list('rzcolormap', cmap, N=nColor)
        cmapobj.colors = cmap
    elif isinstance(cmap, LinearSegmentedColormap) | isinstance(cmap, ListedColormap):
        cmapobj = rz.figure.colormap(cmap, nColor, False)  # update color map object

    # create angle entry
    angle = np.linspace(0, 360, nColor + 1)
    anglewidth = angle[1] - angle[0]
    angle = angle - anglewidth / 2

    r = np.linspace(0, imgradius, nColor + 1)
    width = r[1] - r[0]

    fig, ax = plt.subplots()
    if mode == 'angle':
        for i in np.arange(nColor):
            # note that this figure starts from 3 clock, let's make it starts from 0 clock
            #coloridx = i + 90 if i < 270 else i-270
            coloridx=i
            ax.add_patch(Wedge((0, 0), imgradius, angle[i], angle[i + 1], color=cmapobj(coloridx)))
    elif mode == 'ecc':
        for i in np.arange(nColor):
            ax.add_patch(Wedge((0, 0), r[i + 1], 0, 360, width=width, color=cmapobj(i)))
    else:
        raise ValueError('We can only plot angle and ecc map')
    # set the ax
    plt.setp(ax, ylim=[-imgradius * 1.1, imgradius * 1.1], xlim=[-imgradius * 1.1, imgradius * 1.1])
    ax.axis('equal')
    return ax, cmapobj