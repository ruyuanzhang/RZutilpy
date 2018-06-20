def cmapang2(nColor=360):
    '''
    cmapang2():

    rz's colormap for angular data. We use cmocean package and use cmocean.cm.phase
    as the base. We update this object and return it.

    Note this colormap differs from cmapang.py since this colormap is more standard
    as the luminance is more uniform.

    we return a colormap object
    '''
    from cmocean.cm import phase
    from RZutilpy.figure import colormap

    return colormap(phase, nColor=nColor)