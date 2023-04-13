def setcolorcycle(cmap):
    '''
    <cmap> is a str/list/colormap object
    '''
    import matplotlib.pyplot as plt
    from RZutilpy.figure import colormap
    from matplotlib.colors import ListedColormap
    from matplotlib import colors
    from cycler import cycler
    from RZutilpy.array import split

    if isinstance(cmap, str):
        cmap = colormap(cmap)
        colorlist = split(cmap.colors,axis=0)
        colorlist = [colors.to_hex(i) for i in colorlist]
    elif isinstance(cmap, list):
        pass
    elif isinstance(cmap, ListedColormap):
        colorlist = split(cmap.colors,axis=0)
        colorlist = [colors.to_hex(i) for i in colorlist]
    else:
        raise ValueError("input the correct cmap")

    cyc = (cycler(color=colorlist))
    plt.rc('axes', prop_cycle=cyc)
    