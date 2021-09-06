def makespatiotemporalfilter(res=100, r=None, c=None, cpfov=5, ori=0, phase=0, bandwidth=-1, xx=None, yy=None, tt=None, thresh=0.01, tres=100, flip=True):
    '''
    makespatiotemporalfilter(res=100, r=None, c=None, cpfov=5, ori=0, phase=0, bandwidth=-1, xx=None, yy=None, tt=None, tres=100, tcpfov=5, tbandwidth=-1, thresh=0, flip=True):
    
    <res> is the number of pixels along one side
    <r> is the row associated with the peak of the Gaussian envelope (can be a decimal).
        if [], default to the exact center of the image along the vertical dimension.
    <c> is the column associated with the peak of the Gaussian envelope (can be a decimal).
        if [], default to the exact center of the image along the horizontal dimension.
    <cpfov> is the number of cycles per field-of-view
    <ori> is the orientation in [0,2*pi).  0 means a horizontal Gabor.
    <phase> is the phase in [0,2*pi)
    <bandwidth> is
        +A where A is the number of cycles per 4 std dev of the Gaussian envelope
        -B where B is the spatial frequency bandwidth in octave units (FWHM of amplitude spectrum)
        note that cases +A and -B imply an isotropic Gaussian envelope.
    <xx>,<yy>,<tt> (optional) are speed-ups (dependent on <res>)
    <thresh>: 
        if <thresh> > 0, we crop pixels whose intensity falls below <thresh> in the    spatial Gaussian envelope.

    # temporal parameter
    <tres>: 
        the kernel size along temporal dimension, similar to <res> in the spatial domain, we will only construct on 1 full cycle along the temporal dimension. If we know the presentation rate (ms per frame), we then can calculate the temporal frequency.
    <flip>: 
        If True, we flipt the sin function along temporal domain such that it is truely used for convolution, if False, no flip, it is for cross-correlation. Note the difference between convolution and cross-correlation.

    return <f>, an image where values are in [-1,1].
    we don't normalize the matrix for power or anything like that.
    also return <g>, an image where values are in [0,1].  this is the Gaussian
    envelope used to construct <f>.
    We also return 1D temporal kernel <tkernel>
    also return <sd>, the standard deviation(s) that we used (in pixel units)
    
    example:
    plt.figure(); imagesc(makegabor2d(32,[],[],4,pi/6,0,2),[-1 1]);
    
    
    '''
    from numpy import sin, pi, newaxis
    from RZutilpy.imageprocess import makegabor2d, linspacepixels
    
    # first make the 2d gabor
    gbr,gau, sd, _, _ = makegabor2d(res=res, r=r, c=c, xx=xx,yy=yy,cpfov=cpfov,ori=ori,phase=phase, bandwidth=bandwidth, thresh=thresh)

    # make the temporal filter, it is a sin function
    if tt is None:
        tt=linspacepixels(0, 1,tres)
    tkernel = sin(2*pi*tt)
    if flip:
        tkernel = tkernel[::-1]
    
    # combine spatial and temporal
    f = gbr[:, :, newaxis] @ tkernel[newaxis, :]
    
    # export the sd
    sd = sd * res

    return f, gau, tkernel, sd, xx, yy, tt
