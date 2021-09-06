def makemultiscalespatiotemporalfilters(**kwargs):
    '''
    This function is used to generate multiscale spatiotemporal gabor filters for motion detection. The input is a dict.

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

    # temporal parameters
    <TF>: temporal frequency, how many circles per frame
        Note that the size along the temporal domain (tsize) is round(1/TF), we only contrast one full cycle along the temporal domain

    <tflip>: boolean, default:False
        whether to flip temporal kernel (for full convolution) or keep (for cross-correlation)
    
    # We output spatiotemporal filters
    <gabor>: a list of spatial temporal filters, 
        if we have multiple TF and SF, the order should be [TF1SF1, TF1SF2,... TF2SF1....]
    <gauss>: a list with the same length of <gabor>, gaussian envelope in spatial domain
    <tKernel>: a list wiht the same length <gabor>, temporal kernals
    <sd>: a list with the same length as <sd>. Standard deviation of spatial gaussian envelopes in pixels
    

    Notes:
    1. We use multiscalegaborfilters to create all spatial gabor Kernels.
    2. Note that <ksize> and <cpfov> determine the spatial frequency of the gabor.
    3. Currently we assume square kernel size and isotropic Gaussian envelope
    '''
    from RZutilpy.imageprocess import makegabor2d
    from numpy import stack, round, arange, pi, sin, ceil, sign

    # update the default parameters
    params = {
        'ksize': 101, # the ksize better use odd number
        'cpfov': 5,
        'bandwidth': -1,  # how wavelength
        'ori': 0,
        'phi': 0,
        'thresh': 0.01,
        'TF':0.05,
        'tflip': False
    }
    # update kwargs
    params.update(kwargs)

    ksize = params['ksize']
    cpfov = params['cpfov']
    bandwidth = params['bandwidth']
    ori = params['ori']
    phi = params['phi']
    thresh = params['thresh']
    TF = params['TF']

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

    if isinstance(TF, int) or isinstance(TF, float):
        TF = [TF]
    params['TF'] = TF

    direction = [sign(i) for i in TF] # direction represent two opposite directions
    TF = [abs(i) for i in TF] # convert 
    
    # construct temporal kernel
    tsize = [int(ceil(1/i) // 2 * 2 + 1) for i in TF]  # how many frames in temporal domain, we always give odd value
    params['tsize'] = tsize
    tK = []
    for iTF, vTF in enumerate(TF):
        tt = arange(0, 1, 1/tsize[iTF])
        tker = sin(tt*2*pi) * direction[iTF]
        if params['tflip']:
            tker = tker[::-1]
        tK.append(tker)
    

    # calculate the wavelength in pixels
    wavelength = [round(iksize / icp) for iksize in ksize for icp in cpfov]
    params['wavelength'] = wavelength

    gabor, gauss, sd, tKernel = [], [], [], []
    for iTF, vTF in enumerate(TF): # loop temporal frequency
        tker = tK[iTF] # derive temporal kernel
        for iSF, vSF in enumerate(cpfov):  # loop spatial frequency
            gbrtmp1, gautmp1 = [], []
            xx, yy = None, None  # to speed up
            for iPhi, vPhi in enumerate(phi):  # loop phase
                for iOri, vOri in enumerate(ori):  # loop orientation
                    gbrtmp, gautmp, sd1, xx, yy = makegabor2d(
                        res=ksize[iSF], cpfov=cpfov[iSF], bandwidth=bandwidth[iSF], ori=vOri, phase=vPhi, thresh=thresh, xx=xx, yy=yy)
                    
                    # add temporal domain, convert to 3d
                    gbrtmp = [gbrtmp * i for i in tker]
                    gbrtmp = stack(gbrtmp, axis=-1)

                    # save gabor and gauss
                    gbrtmp1.append(gbrtmp.copy())
                    gautmp1.append(gautmp.copy())

            gabor.append(stack(gbrtmp1, axis=-1))
            gauss.append(stack(gautmp1, axis=-1))
            sd.append(sd1)
            tKernel.append(tker)

    params['gabor'], params['gauss'], params['sd'], params['tKernel'] = gabor, gauss, sd, tKernel

    return params
