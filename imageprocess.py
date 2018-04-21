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

from .imageprocessutils import makegaussian2d
makegaussian2d = makegaussian2d.makegaussian2d

# ==============================================================================
# read/save/process multiple images
# ==============================================================================
from .imageprocessutils import imreadmulti
imreadmulti = imreadmulti.imreadmulti

from .imageprocessutils import imsavemulti
imsavemulti = imsavemulti.imsavemulti

from .imageprocessutils import processmulti
processmulti = processmulti.processmulti

# ==============================================================================
# coordinate
# ==============================================================================
from .imageprocessutils import calcunitcoordinates
calcunitcoordinates = calcunitcoordinates.calcunitcoordinates

from .imageprocessutils import makeimagestack
makeimagestack = makeimagestack.makeimagestack

from .imageprocessutils import makeimagestack3dfiles
makeimagestack3dfiles = makeimagestack3dfiles.makeimagestack3dfiles

from .imageprocessutils import imagesequencetovideo
imagesequencetovideo = imagesequencetovideo.imagesequencetovideo

from .imageprocessutils import videotoimagesequence
videotoimagesequence = videotoimagesequence.videotoimagesequence

from .imageprocessutils import graytorgb
graytorgb = graytorgb.graytorgb
