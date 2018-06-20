def imreadmulti(pattern, mode='array'):
    '''
    imreadmulti(pattern, mode='array'):

    read in multiple images, we use rz.system.matchfiles to derive the filenames
    We use PIL package to read in images.
    Default is to return an array.

    <pattern>: wildercart to match files, input for rz.figure.matchfiles. Y
        ou can use '~' to replace home directory
    <mode> the mode of the returned object should be
        'array': concatenate all images into 3rd dimension and return an array. If images have different size, then report error
        'list': return a list containing all images as np.array
        'PIL': return a list containing all PIL.Image object
    '''
    from RZutilpy.rzio import matchfiles
    from PIL import Image
    from numpy import array, stack

    # match file names
    filenamelist = matchfiles(pattern)
    assert filenamelist, 'No image is found!'

    # load the images
    img_list = [Image.open(file) for file in filenamelist]

    # output
    if mode == 'PIL':
        return img_list
    elif mode == 'list':
        return [array(ele) for ele in img_list]
    elif mode == 'array':
        img_list = [array(ele) for ele in img_list]
        return stack(img_list, axis=-1)