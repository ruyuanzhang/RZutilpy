def imagesequencetovideo(images, videoname, imagepercnt=1, videocodec=None, fps=15):
    '''
    imagesequencetovideo(images, videoname, imagepercnt=1, videocodec=None, fps=15):

    write a image sequence to video. We use utility from moviepy module. We normalize
    all images and convert it to uint8

    Input:
        <images>: can be:
            (1), a 3d or 4d array. Assume the last dimension is time. We convert
                the array to uint8 type.
                if 3d, assuming it is gray scale, we will convert it to RGB format
                if 4d, assume the 3rd dimension is RGB.
                Also, for 3d and 4d, we split them to imagelist
            (2), a wildcard pattern for glob module, we use rz.rzio.matchfiles
                to read it.
            (3), a list of images, in this case each element must 3d (RGBimage)
                image. Note that all images should have equal size.
        <videoname>: output pathname, need to specify the type. If the filename
            is has extension ‘.mp4’, ‘.ogv’, ‘.webm’, the codec will be set accordingly,
            but you can still set it if you don’t like the default.
            For other extensions, the output filename must be set accordingly.
        <imagepercnt>: int, intensities most lower and upper percent will be clipped
            default: 1
        <code>: video code, check, write_videofile method of moviepy Clip object
        <fps>: # of frames per second
    Output:
        a clip object from moviepy module

    To do:
        1. input a frame function

    Example:
        images = np.random.rand(100,100,20)
        rz.imageprocess.imagesequencetovideo(images, 'video.mp4')

    '''
    from RZutilpy.imageprocess import imreadmulti, touint8
    from RZutilpy.array import split
    from RZutilpy.math import normalizerange
    from numpy import ndarray, stack, percentile, all
    from moviepy.editor import ImageSequenceClip
    from os.path import splitext

    # check input
    if isinstance(images, ndarray):
        ndim = images.ndim
        if ndim == 3:
            images = stack((images, images, images), axis=2)
            return imagesequencetovideo(images, videoname, videocodec, fps)
        elif ndim == 4:
            assert images.shape[2] == 3, 'wrong RGB images input!'
        else:
            raise ValueError('image dimension is wrong !')
        # split to image list
        images = split(images)
    elif isinstance(images, str):  # glob wildcard pattern
        images = imreadmulti(images)
        return imagesequencetovideo(images, videoname, videocodec, fps)
    elif isinstance(images, list):
        # ensure all element is rgb images
        assert all([i.ndim == 3 and i.shape[2]==3 for i in images]), \
        'make sure all images are RGB images'
    else:
        raise ValueError('Input images format is wrong!')

    # normalize convert all images to uint8
    images = list(map(touint8, images))

    # do it
    clip = ImageSequenceClip(images, fps=fps)
    _, ext = splitext(videoname)
    if ext in ['.mp4', '.ogv', '.webm']:
        clip.write_videofile(videoname)
    else:
        assert videocodec is not None, 'for this video format, please input videocodec'
        clip.write_videofile(videoname, codec=videocodec)
    return clip

