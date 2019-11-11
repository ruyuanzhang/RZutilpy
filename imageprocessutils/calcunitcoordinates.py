def calcunitcoordinates(res=100):
    '''
    function [xx,yy] = calcunitcoordinates(res=100)

    <res> is the number of pixels on a side,default 100

    return <xx> and <yy> which contain x- and y-coordinates corresponding
    to equally spaced points within the space bounded by -.5 and .5.
    these points can be treated as centers of pixels.

    example:
    xx, yy = rz.imageprocess.calcunitcoordinates(100);
    isequal(xx,[-.25 .25; -.25 .25]) & isequal(yy,[.25 .25; -.25 -.25])

    notice that the second argument proceeds from .5 to -.5.
    this ensures that the results match the usual coordinate axes
    where the top is the positive y-axis.
    '''
    import numpy as np
    from RZutilpy import index
    return np.meshgrid(index.linspacepixels(-.5, .5, res),
                       index.linspacepixels(.5, -.5, res))