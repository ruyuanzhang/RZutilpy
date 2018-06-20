def processmulti(fun, imgs, *args):
    '''

    processmulti(fun, imgs, *args)


    #==========================
    deprecated from 20180616
    #==========================

    processing multiple image
    process multiple images, input images should be 3D ndarray

    Args:
        fun: is a function handle object that expects a 2D image as the first
            argument
        images: is : an nd array, with last dimenstion indicating images
        args: is a set of arguments that are expected by <fun>

    Return
        apply <fun> to each image and concatenate the results together.

    Example:
        f = processmulti(np.resize, np.random.rand(100,100,3),(50,50))
        f.shape
        or
        fun = lambda x: np.resize(x, (50,50))
        f = processmulti(fun, np.random.rand(100,100,3)))

    '''
    import numpy as np
    import RZutilpy as rz

    # if only 1 image , we expand to 3 dimension
    if imgs.ndim == 2:
        imgs.reshape(*imgs.shape, 1)

    # split ndarray into a list
    imgs = np.split(imgs, imgs.shape[-1], axis=-1)
    imgs = [ele.squeeze() for ele in imgs]  # squeeze all images

    # do it
    imgs = [fun(ele, *args) for ele in imgs]

    # concatenate images
    imgs = np.stack(imgs, axis=-1)
    return imgs