def makespatiotemporalgaborfilter(**kwargs):
    '''
    This function is used to generate multiscale gabor filters. The input is a dict.

    We have below keyward arguments
    <ksize>: an int, or a list of int with the same length of <sf>, where each element indicates the pixel for kernels at each scale. We assume squared kernel. But the output might not be the <ksize> if <crop> set it to true. We can typically input a large <ksize> and let the image to be cropped.
    <cpfov>: a real number of a list of real number, cycles/fov. Based on <cpfov> and <ksize> we can calculate the wavelength as <ppd>/<sf> in pixels. default: [5], i.e., 5 cycle / fov.
    <bandwidth>: can be 
        +A: where A is how many times of wavelength (Default: -1)
        -B: where B is the spatial frequency bandwidth in octave units (FWHM of amplitude spectrum)
        a list of +A or -B with the same length of <sf>.
    <ori>: radians or a list of radians in [0, pi), default:0
    <phi>: radians or a list of radians in [0, 2pi), default:0
    <thresh>: If <thresh> >0, We crop pixels that Gaussian falls below <thresh>
    
    Notes:
    1. We use makegabor2d to create all gabor Kernels.
    2. Note that <ksize> and <cpfov> determine the spatial frequency of the gabor.
    3. Currently we assume square kernel size and isotropic Gaussian envelope
    '''
    from RZutilpy.imageprocess import makegabor2d
    from numpy import stack

    # update the default parameters
    params = {
        'ksize': 100,
        'cpfov': 5,
        'bandwidth': -1,  # how wavelength
        'ori': 0,
        'phi': 0,
        'thresh': 0.01
    }
    # update kwargs
    params.update(kwargs)

    ksize = params['ksize']
    cpfov = params['cpfov']
    bandwidth = params['bandwidth']
    ori = params['ori']
    phi = params['phi']
    thresh = params['thresh']

    if isinstance(cpfov, int) or isinstance(cpfov, float):
        cpfov = [cpfov]
    params['cpfov'] = cpfov

    if isinstance(ksize, int):
        ksize = [ksize] * len(cpfov)
    params['ksize'] = ksize

    if isinstance(bandwidth, int) or isinstance(bandwidth, float):
        bandwidth = [bandwidth] * len(params['cpfov'])
    params['bandwidth'] = bandwidth

    if isinstance(ori, int) or isinstance(ori, float):
        ori = [ori] * len(params['cpfov'])
    params['ori'] = ori

    if isinstance(phi, int) or isinstance(phi, float):
        phi = [phi] * len(params['cpfov'])
    params['phi'] = phi

    # calculate the wavelength in pixels
    wavelength = [round(iksize / icp) for iksize in ksize for icp in cpfov]
    params['wavelength'] = wavelength

    gabor, gauss, sd = [], [], []
    for iSF, vSF in enumerate(cpfov):  # loop spatial frequency
        gbrtmp1, gautmp1 = [], []
        xx, yy = None, None  # to speed up
        for iPhi, vPhi in enumerate(phi):  # loop phase
            for iOri, vOri in enumerate(ori):  # loop orientation
                gbrtmp, gautmp, sd1, xx, yy = makegabor2d(
                    res=ksize[iSF], cpfov=cpfov[iSF], bandwidth=bandwidth[iSF], ori=vOri, phase=vPhi, thresh=thresh, xx=xx, yy=yy)
                # save gabor and gauss
                gbrtmp1.append(gbrtmp.copy())
                gautmp1.append(gautmp.copy())
        gabor.append(stack(gbrtmp1, axis=-1))
        gauss.append(stack(gautmp1, axis=-1))
        sd.append(sd1)

    params['gabor'], params['gauss'], params['sd'] = gabor, gauss, sd

    return params
