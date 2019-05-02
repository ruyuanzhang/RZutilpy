def getdefaultcolorlist():
    # get the default color cycle list for plot
    import matplotlib.pyplot as plt
    return plt.rcParams['axes.prop_cycle'].by_key()['color']