def writevideomri(mriarr, videoname, axis=2, k=0, stackkwargs={'wantnorm':1}, videokwargs={}):
    '''
    writevideomri(mriarr, videoname, axis=2, k=(), stackkwargs={'wantnorm':1}, videokwargs={}):

    Write mri 3d or 4d volume into a video. If 4d, we write as a video of the image
    stack. We utilize makeimagestackmri function to make the image list or image
    stack then use imagesequencetovideo function to write the video

    Input:
        <mriarr>: is a 3d or 4d array or a nibabel image object, this is for MRI
            so we assume all images are gray scale
        <videoname>: output video name
        <axis>: int ~ [0, 1, 2], indicate:
            if 3d, from which axis to make the video
            if 4d, from which axis to make imagestacks
            default is 2
        <k>: an int, how many times for CCW rotation, see np.rot90. default is 0
            see makeimagestackmri.py
        <stackkwargs>: a dict, kwargs for makeimagestack.py
            can specify <wantnorm>, <addborder>, <csize>,<bordersize>, it only works
            for the 4d array input.
        <videokwargs>: a dict, kwargs for imagesequencetovideo.py

    Output:
        <clip>: moviepy, video clip object
        also save the video

    Example:


    History:
        20180421 RZ used cv2.cvtColor to accelerate the graytorgb process in 4d
            input case
        20180419 RZ created the file

    To do:
        1. fix the bug of equal sourcemin and sourcemax in normalizerange

    '''

    from nibabel.nifti1 import Nifti1Image as nifti
    from numpy import ndarray, rot90
    from RZutilpy.imageprocess import imagesequencetovideo, graytorgb
    from RZutilpy.mri import makeimagestackmri
    from RZutilpy.array import split
    import progressbar
    from cv2 import cvtColor, COLOR_GRAY2RGB
    from numba import jit


    if isinstance(mriarr, nifti):
        mriarr = mriarr.get_data()
    elif isinstance(mriarr, ndarray):
        pass
    else:
        raise ValueError('Wrong input!')

    pbar = progressbar.progressbar

    ndim = mriarr.ndim
    if ndim == 3:
        # deal with rotation
        rotateparams = [(1, 2), (0, 2), (0, 1)]  # the plane to rotate
        mriarr = rot90(mriarr, k=k, axes=rotateparams[axis])
        imglist = split(mriarr, axis=axis)
        imglist = graytorgb(imglist)  # expand each image to 3d rgb image

    elif ndim == 4:
        imglist = split(mriarr)  # split time dimension, now each ele is a 3d file
        # deal with k
        tmpk = [(),(),()]
        tmpk[axis] = k
        k = tmpk
        # do it
        print('This is a 4d array, we make image stack ......')
        # make imagestack for every 3d mri file
        # note that imagestack is normalized to 0~1 with dtype float64
        imglist = [makeimagestackmri(i, k=k, **stackkwargs)[axis] for i in pbar(imglist)]

        print('\nimage stacks done! \n')
        # we convert it to 0~255 uint8, and call cv2.cvtColor function to rgb
        imglist = [cvtColor((i * 255).astype('uint8'), COLOR_GRAY2RGB) for i in imglist]

    # do it, write imagesequence to video
    clip = imagesequencetovideo(imglist, videoname, **videokwargs)
    return clip
