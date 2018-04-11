def imsavemulti(images, pattern, N=None):
    '''
    msavemulti(images, pattern):

    save multiple images using str pattern. If input images are ndarray, we split it into a list then save it. Note that we convert all imagesto uint8 format. So be careful the value range of input images should be [0,255]

    <images> is:
        (1) a multidimensional array. Dimension 3/4/5 indicate gray/RGB/RGBA images since the last dimension indicates image number.
        (2) a list of 2d array image, in this case. Different images can have different size
    <pattern> is a filename pattern, e.g., 'images%02d.png'
    <N> image number index, can be like [3, 4, 5, 6]. Default: use images.shape[-1] or len(images)
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from RZutilpy.rzio import multifilename
    from PIL import Image

    if isinstance(images, np.ndarray):
        # split image arrays into a list
        images = rz.array.split(images)
    elif isinstance(images, list):
        pass
    else:
        raise ValueError('Image should be an array or a list !!')
    if N is None:
        N = np.arange(len(image)) + 1  # default 1:N
    if ~isinstance(N, np.ndarray):
        raise ValueError('Input image number index is wrong!')

    # change all images in list to uin8.
    images = [ele.astype('uint8') for ele in images]
    # convert all images into a PIL.Image object
    images = [Image.fromarray(ele) for ele in images]

    nImg = len(images)
    filename = multifilename(pattern, N)
    for i, ele in enumerate(images):
        ele.save(filename[i])
        print(filename[i])