def cmapang2(nColor=360):
    '''
    cmapang2():

    rz's second circular colormap. We use cmocean package and use cmocean.cm.phase as the base. We update this object and return it
    '''
    from cmocean.cm import phase
    from RZutilpy.figure import colormap

    return colormap(phase, nColor=nColor)