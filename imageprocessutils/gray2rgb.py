def gray2rgb(image):
    '''
    convert 2d image array to RGB

    <image> is:
        (1) a 2d array
        (2) a 3d array with the 3rd dimension as the image number
        (3) a list of 2d image

    We output a list if input is a list, and an array if input is an array

    Note that we keep the dtype of the input. It can be float,uint8 or anything
    '''
    from numpy import ndarray, stack, all
    from RZutilpy.array import split

    if isinstance(image, ndarray):
        if image.ndim == 2:
            return stack((image, image, image), axis=-1)
            # note that stack might be slow
        elif image.ndim == 3:
            image = split(image)  # convert it to list of images and rerun
            image = gray2rgb(image)
            return stack(image, axis=-1)
            # note that stack might be slow
        else:
            raise ValueError('Input images is wrong')

    elif isinstance(image, list):
        assert all([2 <= i.ndim <= 3 for i in image]), 'Input image list is wrong'
        return [gray2rgb(i) for i in image]
