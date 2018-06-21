def makeimagestack3dfiles(m, outputprefix=None, skips=[5, 5, 5], k=[0, 0, 0], \
    cmap='gray', **kwargs):
    '''
    makeimagestack3dfiles(m, outputprefix=None, skips=[5, 5, 5], k=[0, 0, 0], \
        cmap='gray', **kwargs):

    Input:
        <m>: is a 3D matrix or a nibabel image object
        <outputprefix>: is a output prefix,if it is NONE, then do not write images
        <skips> (optional) is number of slices to skip in each of the 3 dimensions.
          Default: [1 1 1].
        <k> (optional) is a list with numbers containing the times to CCW rotate matrix
            rotation info. See np.rot90. Default: [(), (), ()]. <k[i]> indicates
            rotate the image when writing image stack along ith dimension
        <cmap> (optional) is colormap to use. Default: gray(256).
        <kwargs>: kwargs for makeimagestack, include <wantnorm>, <addborder>
            <csize>,<bordersize>
    Output:
        <imglist>: a 1x3 list containing the image matrix for 2,1,0 dimensions.
            note here the order is not from 0-2 dimensions. Each image is within
            range 0~1 float 64.

    We take <m> and write out three .png files, one for each slicing:
      <outputprefix>_view0.png
      <outputprefix>_view1.png
      <outputprefix>_view2.png

    The first slicing is through the first dimension with ordering [0 1 2].
    The second slicing is through the second dimension with ordering [1 3 2].
    The third slicing is through the third dimension with ordering [2 3 1].

    After slicing, rotation (if supplied) is applied within the first
    two dimensions using np.rot90

    Example:
        vol = makegaussian3d([100 100 100],[.7 .3 .5],[.1 .4 .1]);
        makeimagestack3dfiles(vol,'test',[10 10 10],[],[],[0 1])

    To do:
        1. Fix the filepath problem

    History
        20180502 RZ fix the k rotation bug, now should be more clear.
        20180412 RZ change the default cmap to 'gray'
        20180419 RZ change the functionality of outputprefix, not saving images if None..

    '''
    from matplotlib.pyplot import imsave
    from nibabel.nifti1 import Nifti1Image as nifti
    from RZutilpy import imageprocess, figure, system
    import numpy as np
    import os

    if isinstance(m, nifti):
        m = m.get_data()

    _is_writeimage = True
    if outputprefix is None:
        outputprefix = os.getcwd()  # the current directory
        outputprefix = outputprefix + os.sep
        _is_writeimage = False
    (folerpath, header) = os.path.split(outputprefix)

    # create the folder if not exist.
    assert system.makedirs(folerpath)

    # define permutes
    imglist = []
    # we make the dimension to slice to the last one
    permutes = np.array([[1, 2, 0], [0, 2, 1], [0, 1, 2]])
    for dim in range(3):
        temp = m
        if dim == 0:
            # note that the first element in the output image is along 1st dimension
            temp = temp[::skips[dim], :, :].transpose(permutes[dim, :])
        elif dim == 1:
            temp = temp[:, ::skips[dim], :].transpose(permutes[dim, :])
        elif dim == 2:
            temp = temp[:, :, ::skips[dim]].transpose(permutes[dim, :])
        # rotate image
        if k[dim]:  # note
            temp = np.rot90(temp, k=k[dim], axes=(0, 1))  # CCW rotate

        f = imageprocess.makeimagestack(temp, **kwargs)
        imglist.append(f)
        # write the image
        fname = '%s/%s_view%d.png' % (folerpath, header, dim)
        # note that plt.imsave can automatically recognize the vmin and vmax, no
        # need to convert it to uint8 like in matlab
        if is_writeimage:  # if not, only return the images of three views
            imsave(fname, f, cmap=cmap)
    return imglist  # reverse list to keep compatible the original axis