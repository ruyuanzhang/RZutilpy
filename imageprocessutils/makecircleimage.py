def makecircleimage(res=100, r=None, r2=None, xx=None, yy=None, mode=0, center=None):
    '''
    makecircleimage(res, r, xx, yy, r2, mode, center)

    Args:
    <res> is the number of pixels along one side
    <r> is size of radius in pixels
    <r2> (optional) is size of next radius in pixels.  default: <r> .
    <xx>, <yy> (optional) are speed-ups (dependent on <res> )
    <mode> (optional) is
        0 means normal
        1 means use absolute value of x-direction for the "radius"
        2 means use absolute value of y-direction for the "radius"
        3 means use x-direction for the "radius". in this case,
            you can interpret <r> and <r2> as signed coordinate values.
        4 means use y-direction for the "radius". in this case,
            you can interpret <r> and <r2> as signed coordinate values.
        default: 0.
    <center> 
        (optional) is [R C] with the row and column indices of the center.  can be decimal.  default: [(1+<res >)/2 (1+<res > )/2].

    the image is a white circle(1) on a black background(0).
    (when < mode > is 1-4, the image is a white rectangle(1)
        on a black background(0).)
    if < r2 > is not supplied, we return a binary image.
    if < r2 > is supplied, we gradually ramp from white to black
    using a cosine function.  note that < r2 > being not supplied
    is equivalent to supplying < r > for < r2 > .

    example:
    plt.figure()
    plt.imshow(makecircleimage(100, 20, [], [], 40))
    axis equal tight
    '''
    from RZutilpy.imageprocess import calcunitcoordinates
    from numpy import sqrt, zeros, cos, pi, array
    
    # construct coordinates
    if r is None:
        r = (res+1)/2
    if r2 is None:
        r2 = r        
    if xx is None:
        [xx, yy] = calcunitcoordinates(res)
    if center is None:
        center = array([(1+res)/2, (1+res)/2])

    # calc
    r = r/res
    r2 = r2/res
    center = (center-(1+res)/2) * 1 / res
    center[0] = -center[0]

    # figure out regions
    if mode == 0:
        radius = sqrt((xx-center[1])** 2 + (yy-center[0]) ** 2)
    elif mode == 1:
        radius = abs((xx-center[1]))
    elif mode == 2:
        radius = abs((yy-center[0]))
    elif mode == 3:
        radius = xx-center[1]
    elif mode == 4:
        radius = yy-center[0]

    
    region1 = (radius <= r)
    region2 = (radius > r) & (radius <= r2)
    region3 = (radius > r2)

    # do it
    f = zeros((res, res))
    f[region1] = 1
    f[region2] = cos((radius[region2]-r) * pi/(r2-r))/2 + 0.5
    f[region3] = 0

    return f
