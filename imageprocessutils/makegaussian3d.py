def makegaussian3d(arraysize, mn=(0.5,0.5,0.5), sd=(0.2,0.2,0.2), xx=None, yy=None, zz=None, n=1):
    '''
    makegaussian3d(arraysize, mn=(0.5,0.5,0.5), sd=(0.2,0.2,0.2), xx=None, yy=None, zz=None, n=1):

    Make a 3d gaussian, written as makegaussian3d.m function in knkutils

    Input:
      <matrixsize> is [X Y Z] array/list/tuple, with the number of voxels along the three dimensions
      <mn> is an array [A B C] with the peak of the Gaussian.  a value of 0 means center of
        the first voxel.  a value of 1 means center of the last voxel.
        for example, [.5 .5 .5] means to position the Gaussian exactly
        at the center of the volume. Default:(.5 .5 .5)
      <sd> is an array [D E F] with the standard deviation of the Gaussian,
        Default:(.5 .5 .5)
      <xx>,<yy>,<zz> (optional) are speed-ups (dependent on <matrixsize>)
      <n> (optional) is an exponent like in evalgaussian3d.  default: 1.

    Output:
        a 3d gaussian envelope, and three grid

    Example:
    plt.imshow(makeimagestack(makegaussian3d([20 20 9],[.2 .4 .5],[.2 .2 .2])));

    To do:
    1. figure out exponent

    '''

    from numpy import ndarray, meshgrid, inf, arange, array, exp
    from RZutilpy.math import normalizerange
    from RZutilpy.program import choose

    # check input
    assert isinstance(arraysize, (ndarray, list, tuple)), 'Wrong array size !'
    assert isinstance(mn, (ndarray, list, tuple)), 'Wrong mn input!'
    assert isinstance(sd, (ndarray, list, tuple)), 'Wrong sd input!'

    # make grid
    if xx is None:
        xx, yy, zz = meshgrid(arange(arraysize[0]) + 1, arange(arraysize[1]) + 1,\
        arange(arraysize[2]) + 1, indexing='ij')

    # prep
    xmn = normalizerange(array(mn[0]), targetmin=1, targetmax=arraysize[0], sourcemin=0, sourcemax=1, chop=0)
    ymn = normalizerange(array(mn[1]), targetmin=1, targetmax=arraysize[1], sourcemin=0, sourcemax=1, chop=0)
    zmn = normalizerange(array(mn[2]), targetmin=1, targetmax=arraysize[2], sourcemin=0, sourcemax=1, chop=0)
    xsd = choose(arraysize[0]==1, inf, sd[0]*(arraysize[0] - 1));
    ysd = choose(arraysize[1]==1, inf, sd[1]*(arraysize[1] - 1));
    zsd = choose(arraysize[2]==1, inf, sd[2]*(arraysize[2] - 1));

    # check

    # do it
    f = exp(-(xx - xmn)**2/(2*xsd**2) - (yy - ymn)**2/(2*ysd**2) -(zz - zmn)**2/(2*zsd**2))

    if n != 1:
        pass

    return f, xx, yy, zz








