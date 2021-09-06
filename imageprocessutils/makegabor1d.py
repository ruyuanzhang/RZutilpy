def makegabor1d(res=100, c=None, cpfov=5, phase=0, bandwidth=-1, xx=None, thresh=0):
    '''
    function [f,g,xx,sd] = makegabor1d(res,c,cpfov,phase,bandwidth,xx,thresh)
     Input:
       <res>: number of pixel
       <c>: is the center pixel with the peak of the Gaussain envelope (can be a decimal)
       <cpfov>: is the number of cycles per field of view
       <phase>: is the phase in [0, 2*pi)
       <bandwidth> is :
           +A where A is the number of cycles per 4 std dev of the Gaussian
               evenlope
           -B where B is the spatial frequency bandwidth in octave units (FWHM of amplitude spectrum)
       <xx>(optional): speed-ups depends on res
       <thresh>(optional): threshold to crop,default:0, we crop gabor with
               pixels < threshold
     Output:
       f: 1D gabor signal
       g: gaussain kernal
       xx: coordiante
       sd: sd in pixels
    
    Example:
     makeimagestack(makegabor1d(32,[],4,0,-1,[],0.01),[-1 1]);
    
     here's an example to check the -B bandwidth case:
     a = makegabor1d(101,[],[],10,pi/2,0,-1);
     b = fftshift(abs(fft(a)));
     plt.figure(); plt.plot(log2(1:50),b(51,52:end),'ro-');
    '''
    from numpy import linspace, exp, pi, cos, sqrt, log, where, any, array
    from RZutilpy.imageprocess import linspacepixels
    from RZutilpy.math import normalizerange

    if c is None:
        c = (1+res)/2
    if xx is None:
        xx = linspacepixels(-0.5, 0.5, res)

    c = normalizerange(array(c), -.5, .5, .5, res+.5)

    if bandwidth > 0: 
        sd = bandwidth / cpfov / 4    
    else: 
        sd = 1/pi*sqrt(log(2)/2)*(2.**(-bandwidth)+1)/(2.**(-bandwidth)-1)

    # do it
    gauss = exp(-1/2*((xx-c)**2)/sd**2)
    grating = cos(2*pi*cpfov*(-(xx-c)) + phase)
    f = gauss * grating

    assert thresh >= 0, "please input a threshold >= 0"
    if thresh > 0: # we need crop the image
        goodrow, = where(any(gauss >= thresh))
        f = f[goodrow[0]:goodrow[-1]+1]
        gauss = gauss[goodrow[0]:goodrow[-1]+1]
    sd = sd * res
    
    return f, gauss, sd, xx
