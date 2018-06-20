def cmapang():
    '''
    cmapang():

    same as cmapang in knkutil/colormap. we make a colormap of angle data but force
    it only has 64 entries.

    will return <cmapobj> object based on LinearSegmentedColormap class

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