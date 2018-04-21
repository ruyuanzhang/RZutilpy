def imagesequencetovideo(images, videoname, videocodec=None, fps=15):
    '''
    imagesequencetovideo(images, videoname, duration, fps=15):

    write a image sequence to video. We use utility from moviepy module

    Input:
        <images> can be:
            (1), a 3d or 4d array. Assume the last dimension is time. We convert
                the array to int8 type
                if 3d, assuming it is gray scale, we will convert it to RGB format
                if 4d, assume the 3rd dimension is RGB.
            (2), a wildcard pattern for glob module, we use rz.rzio.matchfiles
                to read it.
            (3), a list of images, each element is either a 2d (gray) or a 3d (RGB)
                image. Note that all images should have equal size.
        <videoname>: output pathname, need to specify the type. If the filename
            is has extension ‘.mp4’, ‘.ogv’, ‘.webm’, the codec will be set accordingly,
            but you can still set it if you don’t like the default.
            For other extensions, the output filename must be set accordingly.
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
    from RZutilpy.imageprocess import imreadmulti
    from RZutilpy.array import split
    from numpy import ndarray, stack
    from moviepy.editor import ImageSequenceClip
    from os.path import splitext

    # import ipdb;ipdb.set_trace()

    # check input
    if isinstance(images, ndarray):
        ndim = images.ndim
        # convert to int8
        images = images.astype('int8')

        if ndim == 3:
            images = stack((images, images, images), axis=2)
            return imagesequencetovideo(images, videoname, videocodec, fps)
        elif ndim == 4:
            assert images.shape[2] == 3, 'wrong RGB images input!'
        else:
            raise ValueError('image dimension is wrong !')
        images = split(images)  # split to image list
    elif isinstance(images, str):  # glob wildcard pattern
        images = imreadmulti(images)
        return imagesequencetovideo(images, videoname, videocodec, fps)
    elif isinstance(images, list):
        # ensure all element is rgb images
        assert np.all([i.ndim == 3 and i.shape[2]==3 for i in images]), \
        'make sure all images are RGB images'
    else:
        raise ValueError('Input images format is wrong!')

    # do it
    clip = ImageSequenceClip(images, fps=fps)
    _, ext = splitext(videoname)
    if ext in ['.mp4', '.ogv', '.webm']:
        clip.write_videofile(videoname)
    else:
        assert videocodec is None, 'for this video format, please input videocodec'
        clip.write_videofile(videoname, codec=videocodec)
    return clip

