# image processing module by rz

# all functions
'''
makegaussian2d(res, r, c, sr, sc, xx=None, yy=None, ang=0, omitexp=False):
imreadmulti(pattern, mode='array'):
imsavemulti(images, pattern):
processmulti(fun, *args):
'''

# ==============================================================================
# make variours filters
# =====================
def makegaussian2d(res, r, c, sr, sc, xx=None, yy=None, ang=0, omitexp=False):
    '''
    function f,xx,yy = makegaussian2d(res,r,c,sr,sc,xx,yy,ang=0,omitexp=False)
    # <res> is the number of pixels along one side
    # <r> is the row associated with the peak of the Gaussian (can be a decimal).
    #   if [], default to the exact center of the image along the vertical dimension.
    # <c> is the column associated with the peak of the Gaussian (can be a decimal).
    #   if [], default to the exact center of the image along the horizontal dimension.
    # <sr> is the standard deviation in the vertical direction
    # <sc> is the standard deviation in the horizontal direction
    # <xx>,<yy> (optional) are speed-ups (dependent on <res>)
    # <ang> (optional) is the CCW rotation to apply in [0,2*pi).  0 means no rotation.
    #   it's okay for <ang> to go out of range.  default: 0.
    # <omitexp> (optional) is whether to omit the final exp operation.  default: 0.
    #
    # return an image where values are in [0,1].
    #
    # if you want an L1-normalized image, divide the image by 2*pi*<sr>*<sc>.
    # note that this is in reference to the ideal case where the Gaussian has
    # enough room to extend out.  so, if you are constructing a Gaussian that
    # does not fit very well within the image, the actual L1 length of the image
    # that is constructed will not be exactly 1.
    #
    # note that it doesn't matter if <sr> or <sc> are negative, since they
    # are always squared in function evaluation.
    #
    # history:
    # - 2013/08/28 - implement speed-up
    #
    # example:
    # figure; imagesc(makegaussian2d(32,8,8,4,2),[0 1]);
    '''
    import numpy as np
    import RZutilpy as rz
    # construct coordinate
    if not(r):
        r = np.array((1 + res) / 2)
    if not(c):
        c = np.array((1 + res) / 2)
    if not(sr):
        sr = np.array((1 + res) / 6)
    if not(sc):
        sc = np.array((1 + res) / 6)
    if not(xx) or not(yy):
        xx, yy = rz.imageprocess.calcunitcoordinates(res)
    # convert to the unit coordinate frame
    # r = normalizerange(r,.5,-.5,.5,res+.5,0,0,1);  # note the signs
    # c = normalizerange(c,-.5,.5,.5,res+.5,0,0,1);
    r = (-1 / res) * r + (.5 + .5 / res)  # this is faster
    c = (1 / res) * c + (-.5 - .5 / res)  # this is faster
    sr = np.array(sr) / res
    sc = np.array(sc) / res

    # construct coordinates (see makegabor2d.m)
    coord = np.dot(
        [[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]],
        [(xx - c).flatten(), (yy - r).flatten()])

    # handle equal std dev as a separate case for speed reasons
    if sc == sr:
        f = (coord[0, :] ** 2 + coord[1, :] ** 2) / -(2 * sc ** 2)
    else:
        f = coord[0, :] ** 2 / -(2 * sc ** 2) + coord[1, :] ** 2 / -(2 * sr ** 2)
    if not(omitexp):
        f = np.exp(f)
    f = f.reshape(xx.shape)
    return f, xx, yy


# ==============================================================================
# read/save/process multiple images
# ==============================================================================
def imreadmulti(pattern, mode='array'):
    '''
    imreadmulti(pattern, mode='array'):

    read in multiple images, we use rz.system.matchfiles to. We use PIL package as python IO

    <pattern>: wildercart to match files, input for rz.figure.matchfiles. You can use '~' to replace home directory
    <mode> should be
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


def imsavemulti(images, pattern, N=None):
    '''
    msavemulti(images, pattern):

    save multiple images using str pattern. If input images are ndarray, we split it into a list then save it. Note that we convert all imagesto uint8 format. So be careful the value range of input images should be [0,255]

    <images> is:
        (1) a multidimensional array. Dimension 3/4/5 indicate gray/RGB/RGBA images since the last dimension indicates image number.
        (2) a list of 2d array image, in this case. Different images can have different size
    <pattern> is a filename pattern, e.g., 'images%02d.png'
    <N> image number index, can be like [3, 4, 5, 6]. Default: use images.shape[-1] or len(images)
    '''
    import matplotlib.pyplot as plt
    import numpy as np
    from RZutilpy.rzio import multifilename
    from PIL import Image

    if isinstance(images, np.ndarray):
        # split image arrays into a list
        images = np.split(images, images.shape[-1], axis=images.ndim - 1)
        images = list(map(np.squeeze, images))
    elif isinstance(images, list):
        pass
    else:
        raise ValueError('Image should be an array or a list !!')
    if N is None:
        N = np.arange(len(image)) + 1  # default 1:N
    if ~isinstance(N, np.ndarray):
        raise ValueError('Input image number index is wrong!')

    # change all images in list to uin8.
    images = [ele.astype('uint8') for ele in images]
    # convert all images into a PIL.Image object
    images = [Image.fromarray(ele) for ele in images]

    nImg = len(images)
    filename = multifilename(pattern, N)
    for i, ele in enumerate(images):
        ele.save(filename[i])
        print(filename[i])


def processmulti(fun, imgs, *args):
    ''' processing multiple image
    process multiple images, input images should be 3D ndarray

    Args:
        fun: is a function handle object that expects a 2D image as the first
            argument
        images: is : an nd array, with last dimenstion indicating images
        args: is a set of arguments that are expected by <fun>

    Return
        apply <fun> to each image and concatenate the results together.

    Example:
        f = processmulti(np.resize, np.random.rand(100,100,3),(50,50))
        f.shape
        or
        fun = lambda x: np.resize(x, (50,50))
        f = processmulti(fun, np.random.rand(100,100,3)))

    '''
    import numpy as np
    import RZutilpy as rz

    # if only 1 image , we expand to 3 dimension
    if imgs.ndim == 2:
        imgs.reshape(*imgs.shape, 1)

    # split ndarray into a list
    imgs = np.split(imgs, imgs.shape[-1], axis=-1)
    imgs = [ele.squeeze() for ele in imgs]  # squeeze all images

    # do it
    imgs = [fun(ele, *args) for ele in imgs]

    # concatenate images
    imgs = np.stack(imgs, axis=-1)
    return imgs

# ==============================================================================
# coordinate
# ==============================================================================


def calcunitcoordinates(res=100):
    '''
    function [xx,yy] = calcunitcoordinates(res=100)

    <res> is the number of pixels on a side,default 100

    return <xx> and <yy> which contain x- and y-coordinates corresponding
    to equally spaced points within the space bounded by -.5 and .5.
    these points can be treated as centers of pixels.

    example:
    xx, yy = rz.imageprocess.calcunitcoordinates(100);
    isequal(xx,[-.25 .25; -.25 .25]) & isequal(yy,[.25 .25; -.25 -.25])

    notice that the second argument proceeds from .5 to -.5.
    this ensures that the results match the usual coordinate axes
    where the top is the positive y-axis.
    '''
    import numpy as np
    from RZutilpy import index
    return np.meshgrid(index.linspacepixels(-.5, .5, res),
                       index.linspacepixels(.5, -.5, res))


def makeimagestack(m, wantnorm=None, addborder=1, csize=None, bordersize=1):
    '''
    makeimagestack(m, wantnorm=None, addborder=1, csize=None, bordersize=1)

    make a board that can show multiple images at the same time.

    Args:
        m: is a 3D array.  if more than 3D, we reshape to be 3D. We automatically
            convert to double format for the purposes of this function.
        wantnorm: is
           0 means no normalization
           [A, B], list, means normalize and threshold values such that A and B map to 0 and 1.
           X means normalize and threshold values such that X percentile
             from lower and upper end map to 0 and 1.  if the X percentile
             from the two ends are the same, then map everything to 0.
           -1 means normalize to 0 and 1 using -max(abs(m(:))) and max(abs(m(:)))
           -2 means normalize to 0 and 1 using 0 and max(m(:))
           -3 means normalize to 0 and 1 using min(m(:)) and max(m(:))
           default: 0.
        addborder is
            0 means do not add border
            1 means add border at the right and bottom of each image.
              the border is assigned the maximum value.
            2 means like 1 but remove the final borders at the right and bottom.
           -1 means like 1 but assign the border the middle value instead of the max.
           -2 means like 2 but assign the border the middle value instead of the max.
            j means like 1 but assign the border a value of 0.
            2*j means like 2 but assign the border a value of 0.
            NaN means plot images into figure windows instead of returning a matrix.
              each image is separated by one matrix element from surrounding images.
              in this case, <wantnorm> should not be 0.
            default: 1.
        csize: is a list [X, Y], a 2D matrix size according
           to which we concatenate the images (row then column).
           default is [], which means try to make as square as possible
           (e.g. for 16 images, we would use [4 4]).
           special case is -1 which means use [1 size(m,3)].
           another special case is [A 0] or [0 A] in which case we
           set 0 to be the minimum possible to fit all the images in.
        bordersize: is number of pixels in the border in the case that
           addborder is not None.  default: 1.

    Return:
        we combine and return all return values from plt.errorbar with three
        ndarray of artist collections, with line object, cap object and line
        collections

    Example:

         a = np.random.randn[10,10,12]
         plt.imshow(rz.imageprocess.makeimagestack(a,-1))
         plt.imshow(rz.imageprocess.makeimagestack(a,-1, nan))

    Note:
    '''
    import numpy as np
    import RZutilpy as rz

    assert isinstance(m, np.ndarray), 'm is not a numpy array'

    ncols = m.shape[0]  # for an array, cols is 1st dimension
    nrows = m.shape[1]

    # make it double
    m.astype('float64')  # make it float
    wantnorm = float(wantnorm)

    # make m 3D if neccessary
    m = m[:, np.newaxis]

    if len(wantnorm) == 2:
        m = rz.math.normalizerange(m, 0, 1, wantnorm[0], wantnorm[1])
        mn = 0
        mx = 1
    elif wantnorm == 0:
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
    md = (mn + mx) / 2

    # number of images
    numim = m.shape[2]

    # calculate csize if necessary
    if rz.math.isempty(csize):
        rows = np.floor(np.sqrt(numim))   # MAKE INTO FUNCTION?
        cols = np.ceil(numim / rows)
        csize = [rows, cols]
    elif csize == -1:
        csize = [1, numim]
    elif csize[0] == 0:
        csize[0] = np.ceil(numim / csize[1])
    elif csize[1] == 0:
        csize[1] = np.ceil(numim / csize[0])

    # calc
    chunksize = np.prod(csize)
    numchunks = np.ceil(numim / chunksize)

    # convert to cell vector, add some extra matrices if necessary
    m = np.split(m, m.shape[-1], 3)
    # m = [m repmat({repmat(mn, size(m{1}))}, 1, numchunks * chunksize - numim)]

    # figure case
    # if rz.math.isnan(addborder):
    #     # pass for p in range(numchunks):

    # else:
    #     # add border?
    #     if np.imag(addborder) | addborder:
    #         for p in range(len(m))

    #     # combine images


    #     # remove final

