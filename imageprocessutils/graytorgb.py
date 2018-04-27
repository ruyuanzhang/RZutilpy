def graytorgb(image):
    '''
    convert 2d image array to RGB
    <image> is:
        (1) a 2d array
        (2) a 3d array with the 3rd dimension as the image number
        (3) a list of 2d image

    We output a list if input is a list or multidimensional array if it is an array
    Note that we keep the dtype of they array. It can be float,uint8 or anything
    '''
    from numpy import ndarray, stack, all
    from RZutilpy.array import split

    if isinstance(image, ndarray):
        if image.ndim == 2:
            return stack((image, image, image), axis=-1)
        elif image.ndim == 3:
            image = split(image)  # convert it to list of images and rerun
            image = graytorgb(image)
            return stack(image, axis=-1)
        else:
            raise ValueError('Input images is wrong')

    elif isinstance(image, list):
        assert all([2 <= i.ndim <= 3 for i in image]), 'Input image list is wrong'
        return [graytorgb(i) for i in image]
