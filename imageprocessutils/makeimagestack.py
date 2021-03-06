def makeimagestack(m, wantnorm=0, addborder=2, csize=None, bordersize=1):
    '''
    makeimagestack(m, wantnorm=0, addborder=2, csize=None, bordersize=1):

    make an imagestack that contains multiple images. Note that we can only create
    grayscale images

    Note:
      1. we only accept gray scale images, no color images
      2. we use reshape scheme and reshape in python follows fortran style
        not C style. That means images arrange row by row
      3. we use np.pad function to pad borders

    Input:
      <m>: is a 3D array. We automatically
          convert to double format for the purposes of this function. The 3rd
          dim is number of images.
      <wantnorm>: is
         0 means no normalization
         (A, B), an 2-elem tuple, means normalize and threshold values such that A and B map to 0 and 1.
         X means normalize and threshold values such that X percentile
           from lower and upper end map to 0 and 1.  if the X percentile
           from the two ends are the same, then map everything to 0.
         -1 means normalize to 0 and 1 using -max(abs(m(:))) and max(abs(m(:)))
         -2 means normalize to 0 and 1 using 0 and max(m(:))
         -3 means normalize to 0 and 1 using min(m(:)) and max(m(:))
         default: 0.
      <addborder> is
        0 means do not add border
        1 means add border at the right and bottom of each image.
          the border is assigned the maximum value.
        2 means like 1 but remove the final borders at the right and bottom.
       -1 means like 1 but assign the border the middle value instead of the max.
       -2 means like 2 but assign the border the middle value instead of the max.
        j means like 1 but assign the border a value of 0.
        2*j means like 2 but assign the border a value of 0.
        None means plot images into figure windows instead of returning a matrix.
          each image is separated by one matrix element from surrounding images.
          in this case, <wantnorm> should not be 0.
        default: 1.
      <csize>: is
        (1). a tuple (X, Y), an 2 ele np.array size according
          to which we concatenate the images (row then column).
        (2) None (default), which means try to make as square as possible
          (e.g. for 16 images, we would use (4 4)).
        (3) special case is -1 which means use [1 size(m,3)].
        (4) another special case is [A 0] or [0 A] in which case we
          set 0 to be the minimum possible to fit all the images in.

      <bordersize>: is number of pixels in the border in the case that
         addborder is not None.  default: 1.

    Output:
      <f>: output the gigantic image stack with range 0~1, float 64. Can use plt.imshow
        to show the image

    Example:
         a = np.random.randn(100,100,12)
         plt.imshow(rz.imageprocess.makeimagestack(a, -1))
         plt.imshow(rz.imageprocess.makeimagestack(a, -1, np.nan))

    History:
      20180621 RZ fix the bug when wantnorm is (x,y) format
      20180616 RZ remove checkarray function, change <csize> to tuple
      20180523 RZ fix addborder bug, now addbode=0 means no border. addborder
        =2 and bordersize=0 has bug.
      20180421 RZ change it
    '''
    import numpy as np
    import RZutilpy as rz

    assert isinstance(m, np.ndarray) and m.ndim == 3, 'Input is not a 3D array'

    (nrows, ncols, numim) = m.shape  # for an array, cols is 1st dimension

    # make it double
    m.astype('float')  # make it float

    if isinstance(wantnorm, tuple):
        assert len(wantnorm) == 2, 'Please input correct wantnorm values'
        m = rz.math.normalizerange(m, 0, 1, float(wantnorm[0]), float(wantnorm[1]))
        mn = 0
        mx = 1
    elif isinstance(wantnorm, int):
        if wantnorm == 0:
            mn = np.nanmin(m)
            mx = np.nanmax(m)
        elif wantnorm == -1:
            m = rz.math.normalizerange(m, 0, 1, -np.abs(m).max(), np.abs(m).max())
            mn = 0
            mx = 1
        elif wantnorm == -2:
            m = rz.math.normalizerange(m, 0, 1, 0, m.max())
            mn = 0
            mx = 1
        elif wantnorm == -3:
            m = rz.math.normalizerange(m, 0, 1, m.min(), m.max())
            mn = 0
            mx = 1
        else:
            rng = np.percentile(m, (wantnorm, 100 - wantnorm))
            if rng[1] == rng[0]:
                m = np.zeros(m.shape)
            else:
                m = rz.math.normalizerange(m, 0, 1, rng[0], rng[1])
            mn = 0
            mx = 1
    else:
      raise ValueError('check the input for <wantnorm> !')

    md = (mn + mx) / 2

    # mn, md and mx are min, middle, max pixel intensities

    # calculate csize if necessary
    if csize is None:
        rows = np.floor(np.sqrt(numim))
        cols = np.ceil(numim / rows)
        csize = np.array([rows, cols]).astype('int')
    elif isinstance(csize, tuple):
        if csize[0] == 0:
            csize[0] = np.ceil(numim / csize[1]).astype('int')
        elif csize[1] == 0:
            csize[1] = np.ceil(numim / csize[0]).astype('int')
    elif csize == -1:
        csize = np.array([1, numim]).astype('int')

    # calc
    chunksize = np.prod(csize)
    numchunks = np.ceil(numim / chunksize).astype('int')

    # convert to list, add some extra matrices if necessary
    m = rz.array.split(m)
    m = m + [mn * np.ones(m[0].shape)] * (numchunks * chunksize - numim)

    # figure case
    if addborder is None:
        pass
    else:
        # figure out the border intensity
        bordervalue = 0 if np.imag(addborder) else (mx if addborder > 0 else md)
        # add border?, we use np.pad function
        m = [np.pad(p, ((0, bordersize), (0, bordersize)), 'constant', constant_values=bordervalue) \
        for p in m]

        # combine images
        m = np.array(m).reshape(csize[0], csize[1], *(m[0].shape))
        # split first 2 dim keep last 2 dimensions into list and keep last 2 dim
        f = rz.array.splitmulti(m, targetndim=2)
        # block nparrays in multidim lists, similar to cell2mat in matlab
        f = np.block(f)

        # remove final
        if abs(addborder) == 2 and bordersize != 0:
            f = f[:-bordersize, :-bordersize]
        return f
