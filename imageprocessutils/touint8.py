def touint8(img, sourcemin=None, sourcemax=None, chop=1, mode=0):
    '''
    touint8(img, sourcemin=None, sourcemax=None, chop=1, mode=0)

    convert a single image with any intensity range to uint8 format so it can be saved or used to make a video

    We use RZutilpy.match.normalizerange function to normalize image to 0~1. then multiple 255
    to convert to uint8

    <img> is a 2d gray image or 3d rgb image, no RGBA format
    see <sourcemin>,<sourcemax>,<chop>,<mode> in RZutilpy.match.normalizerange function

    return a image as uint8 format 0~255

    '''

    from numpy import ndarray
    from RZutilpy.math import normalizerange

    # check input
    assert isinstance(img,ndarray), 'Please input a ndarray image'
    if img.ndim == 3:
        assert img.shape[-1]==3, 'Color image must be rgb format'

    # do it
    # convert to uint8
    return (255 * normalizerange(img, 0, 1, sourcemin=sourcemin, sourcemax=sourcemax,\
        chop=chop, mode=mode)).astype('uint8')