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


    20200226 RZ fixed the bug if too many images are opened
    '''
    from RZutilpy.rzio import matchfiles
    from PIL import Image
    from numpy import array, stack
    import copy

    # match file names
    filenamelist = matchfiles(pattern)
    assert filenamelist, 'No image is found!'

    # load the images
    img_list = []
    for file in filenamelist:
        tmp = Image.open(file)
        img_list.append(copy.deepcopy(tmp)) # note here, PIL object has no copy funtion, have to do manually
        tmp.close() # we need close the image otherwise too many open files

    # output
    if mode == 'PIL':
        return img_list
    elif mode == 'list':
        return [array(ele) for ele in img_list]
    elif mode == 'array':
        img_list = [array(ele) for ele in img_list]
        return stack(img_list, axis=-1)