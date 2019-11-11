def imsavemulti(images, pattern, N=None, wantnorm=(0, 100), **kwargs):
    '''
    imsavemulti(images, pattern, N=None, wantnorm=(0, 100), **kwargs):

    save multiple images using str pattern and plt.imsave() function
    If input images are ndarray, we split it into a list then save it.
    Note that we convert all images to uint8 format. So be careful the value range of input images should be [0,255]

    <images> is:
        (1) a multidimensional array. Dimension 3/4/5 indicate gray/RGB/RGBA images
            since the last dimension indicates image number.
        (2) a list of 2d array image, in this case. Different images can have different size
    <pattern> is a filename pattern, e.g., 'images%02d.png'
    <N>: a 1d array, image number index, can be like [3, 4, 5, 6]. Default: use images.shape[-1] or len(images)
        Note that this vector start from 1 if it is None
    <wantnorm>: a tuple, (A,B), we clip images below A and above B percentile values
        note this operation works on all images together not just one image. Default:(0,100)
    <**kwargs>: kwargs for plt.imsave()


    History:
        20180524 RZ switch to plt.imsave function. By default,

    '''

    import numpy as np
    from RZutilpy.rzio import getmultifilename
    from RZutilpy.system import makedirs
    from RZutilpy.array import split
    from RZutilpy.math import normalizerange
    import matplotlib.pyplot as plt

    if isinstance(images, np.ndarray):
        # split image arrays into a list
        rng = np.percentile(images, (wantnorm[0], wantnorm[1]))
        images = normalizerange(images, images.min(), images.max(), rng[0], rng[1])
        images = split(images)
    elif isinstance(images, list):
        return imsavemulti(np.stack(images, axis=-1), pattern, N=N, wantnorm=wantnorm, **kwargs)
    else:
        raise ValueError('Image should be an array or a list !!')

    if N is None:
        N = np.arange(len(images)) + 1  # default 1:N
    assert isinstance(N, np.ndarray), ValueError('Input image number index is wrong!')

    nImg = len(images)
    filename = getmultifilename(pattern, N)
    for i in N:
        plt.imsave(filename[i-1], images[i-1], vmin=rng[0], vmax=rng[1], **kwargs)
        print(filename[i-1])