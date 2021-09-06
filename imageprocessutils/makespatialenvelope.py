def makespatialenvelope(res=100., masktype='cosine', radius1=None, radius2=None, gaussstd=None):
    '''
    mask = makespatialenvelope(radius,varargin)

    Inputs:
    <res>: number of pixels of the image, assuming a square image
    <masktype>: (optional)
        'cosine', 2D cosine,default (default);
        'gaussian',which is 2D gaussian evenlop;
        'circular', a 2D circular envelope,
        'annulus', a 2D annulus envelope, need to specify inner res
    <radius1>: for outter radius, number of pixels, default: (res/2)
    <radius2>: for Annulus option, number of pixels, default:(0.7 * res/2)

    <gaussstd>: standard devision for Gaussian mask,number of pixels,
            default:(0.7 * res/2)


    Example;

    Note that we use makecircleimage function to generate annulus image
    '''
    from RZutilpy.imageprocess import calcunitcoordinates, makecircleimage, makegaussian2d
    from numpy import exp, zeros, cos, pi, ones, sqrt, finfo
    
    if radius1 is None:
        radius1 = res / 2
    if radius2 is None:
        radius2 = 0.7 * res /2
    if gaussstd is None:
        gaussstd = 0.7 * res / 2

    white = 254.
    background = white / 2
                
    # convert to unit length
    [xx, yy]=calcunitcoordinates(res)
    radius1 = radius1 / res # default outter radius
    radius2 = radius2 / res
    gaussstd = gaussstd / res

    # make the circular mask
    circle=radius1**2-(xx ** 2 + yy ** 2)
    circle[circle<=0] = 0
    circle[circle>0] = 1 # circular mask

    # make gaussian and cosin disk
    if masktype == 'gaussian': # Gaussian Disk, you have to specify gaussianStd
        circle,_,_ = makegaussian2d(res, sr=gaussstd * res, sc=gaussstd * res)
    elif masktype == 'cosine':
        R = (sqrt(xx**2 + yy**2) + finfo(float).eps) * circle
        R = R/R.max()
        #import ipdb;ipdb.set_trace();import matplotlib.pyplot as plt;
        cos2D = (cos(R*pi)+1) / 2 
        circle = (cos2D * circle)  
    elif masktype == 'annulus':
        circle = makecircleimage(res, radius2*res, radius1*res, xx, yy)
    
    return circle
