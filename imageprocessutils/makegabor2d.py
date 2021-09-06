def makegabor2d(res=100, r=None, c=None, cpfov=5, ori=0, phase=0, bandwidth=-1, xx=None, yy=None, thresh=0):
    '''
    makegabor2d(res, r, c, cpfov, phase, bandwidth, xx, yy)
    
    <res> is the number of pixels along one side
    <r> 
        is the row associated with the peak of the Gaussian envelope (can be a decimal).
        if None, default to the exact center of the image along the vertical dimension.
    <c> 
        is the column associated with the peak of the Gaussian envelope (can be a decimal).
        if None, default to the exact center of the image along the horizontal dimension.
    <cpfov> is the number of cycles per field-of-view
    <ori> is the orientation in [0,2*pi).  0 means a horizontal Gabor.
    <phase> is the phase in [0,2*pi)
    <bandwidth> is
        +A where A is the number of cycles per 4 std dev of the Gaussian envelope
        -B where B is the spatial frequency bandwidth in octave units (FWHM of amplitude spectrum)
        0 indicate no spatial envelope, become a grating
        note that cases +A and -B imply an isotropic Gaussian envelope.
    <xx>,<yy> (optional) are speed-ups (dependent on <res>)
    <thresh>: default: 0 (no croping)
        if <thresh> > 0, we crop pixels whose intensity falls below <thresh> in the Gaussian envelope
    
    return <f>, an image where values are in [-1,1].
    we don't normalize the matrix for power or anything like that.
    also return <g>, an image where values are in [0,1].  this is the Gaussian
    envelope used to construct <f>.
    also return <sd>, the standard deviation(s) that we used (in pixel units)
    
    example:
    plt.figure(); imagesc(makegabor2d(32,[],[],4,pi/6,0,2),[-1 1]);
    
    here's an example to check the -B bandwidth case:
    a = makegabor2d(101,[],[],10,pi/2,0,-1);
    b = fftshift(abs(fft2(a)));
    plt.figure(); plt.plot(log2(1:50),b(51,52:end),'ro-');
    
    '''
    from numpy import sqrt, log, exp, cos, sin, pi, array, where, any, ones
    from RZutilpy.math import normalizerange
    from RZutilpy.imageprocess import calcunitcoordinates 
    
    if r is None:
        r = (1+res)/2
    if c is None:
        c = (1+res)/2
    if xx is None:
        [xx,yy] = calcunitcoordinates(res)

    # convert to the unit coordinate frame
    r = normalizerange(array(r), 0.5, -.5, 0.5, res+0.5)
    c = normalizerange(array(c), 0.5, -.5, 0.5, res+0.5)

    # calculate sd based on bandwidth
    if bandwidth > 0:
        sd = bandwidth/cpfov/4
        g = exp(((xx-c)**2+(yy-r)**2)/-(2 * sd**2))
    elif bandwidth < 0:
        # sd in pixels
        sd = 1/pi*sqrt(log(2)/2)*(2.**(-bandwidth)+1)/(2.**(-bandwidth)-1) # how many times of wavelength
        sd = sd * 1/cpfov # convert to pixel unit
        g = exp(((xx-c)**2+(yy-r)**2)/-(2 * sd**2))
    elif bandwidth == 0: # no spatial envelope, just grating
        sd = 0
        g = ones(xx.shape)

    f = g * cos(2*pi*cpfov*(-cos(ori)*(xx-c) + sin(ori)*(yy-r)) + phase)

    # crop if 
    if thresh > 0:
        goodrow,  = where(any(g >= thresh, axis=0))
        goodcol,  = where(any(g >= thresh, axis=1))
        g = g[goodrow[0]:goodrow[-1]+1, goodcol[0]:goodcol[-1]+1]
        f = f[goodrow[0]:goodrow[-1]+1, goodcol[0]:goodcol[-1]+1]
    # export the sd
    sd = sd * res

    return f, g, sd, xx, yy
