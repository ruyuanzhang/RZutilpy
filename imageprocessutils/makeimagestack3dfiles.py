def makeimagestack3dfiles(m, outputprefix=None, skips=[1, 1, 1], k=[(), (), ()], \
    cmap=None, **kwargs):
    '''
    makeimagestack3dfiles(m, outputprefix, skips=[1, 1, 1], rots=[0,0,0]\
        cmap=None, *kwargs):

    Input:
        <m>: is a 3D matrix or a nibabel image file
        <outputprefix>: is a output prefix
        <m> is a 3D matrix or a NIFTI file
        <outputprefix> is a path to a file prefix, default:None, pwd
        <skips> (optional) is number of slices to skip in each of the 3 dimensions.
          Default: [1 1 1].
        <k> (optional) is a list with numbers containing the times to CCW rotate matrix
            rotation info. See np.rot90. Default: [(0,1), (0,1), (0,1)].
        <cmap> (optional) is colormap to use. Default: gray(256).
        <kwargs>: kwargs for makeimagestack,include <wantnorm>, <addborder>
            <csize>,<bordersize>

    We take <m> and write out three .png files, one for each slicing:
      <outputprefix>_view1.png
      <outputprefix>_view2.png
      <outputprefix>_view3.png

    The first slicing is through the third dimension with ordering [1 2 3].
    The second slicing is through the second dimension with ordering [1 3 2].
    The third slicing is through the first dimension with ordering [2 3 1].

    After slicing, rotation (if supplied) is applied within the first
    two dimensions using rotatematrix.m.

    example:
    vol = makegaussian3d([100 100 100],[.7 .3 .5],[.1 .4 .1]);
    makeimagestack3dfiles(vol,'test',[10 10 10],[],[],[0 1])

    To do:
        implement mkdirquite
    '''
    from matplotlib.pyplot import imsave
    from nibabel.nifti1 import Nifti1Image as nifti
    from RZutilpy import imageprocess, figure, system
    import numpy as np
    import os

    if isinstance(m, nifti):
        m = m.get_data()
    if outputprefix is None:
        outputprefix = os.getcwd()  # the current directory
        outputprefix = outputprefix + os.sep
    (folerpath, header) = os.path.split(outputprefix)

    # create the folder if not exist.
    system.makedir(folerpath)

    # define permutes
    permutes = np.array([[0, 1, 2], [0, 2, 1], [1, 2, 0]])
    for dim in range(3):
        temp = m
        if dim == 0:
            temp = temp[:, :, ::skips[dim]].transpose(permutes[dim, :])
        elif dim == 1:
            temp = temp[:, ::skips[dim], :].transpose(permutes[dim, :])
        elif dim == 2:
            temp = temp[::skips[dim], :, :].transpose(permutes[dim, :])
        # rotate image
        if k[dim]:
            temp = np.rot90(temp, k=k[dim], axes=(0, 1))  # CCW rotate

        # write the image
        fname = '%s/%s_view%d.png' % (folerpath, header, dim)
        # note that plt.imsave can automatically recognize the vmin and vmax, no
        # need to convert it to uint8 like in matlab
        imsave(fname, imageprocess.makeimagestack(temp, **kwargs), cmap=figure.colormap('gray', 256))
