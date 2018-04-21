def imreadmulti(pattern, mode='array'):
    '''
    imreadmulti(pattern, mode='array'):

    read in multiple images, we use rz.system.matchfiles to. We use PIL package as python IO.
    Default is to return an array.

    <pattern>: wildercart to match files, input for rz.figure.matchfiles. You can use '~' to replace home directory
    <mode> the mode of the returned object should be
        'array': concatenate all images into 3rd dimension and return an array. If images have different size, then report error
        'list': return a list containing all images as np.array
        'PIL': return a list containing all PIL.Image object
    '''
    from RZutilpy.rzio import matchfiles
    from PIL import Image
    import numpy as np

    filenamelist = matchfiles(pattern)
    assert filenamelist, 'No image is found!'
    img_list = list()
    for file in filenamelist:
        img_list.append(Image.open(file))
    if mode == 'PIL':
        return img_list
    elif mode == 'list':
        return [np.array(ele) for ele in img_list]
    elif mode == 'array':
        img_list = [np.array(ele) for ele in img_list]
        return np.stack(img_list, axis=-1)