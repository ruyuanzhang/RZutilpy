# -*- coding: utf-8 -*-
"""
@author: ruyuan
"""

'''
loadmat(filename, **kwargs):
loadmath5py(filename)
matchfiles(patterns)
multifilename(pattern, N)
savepkl(filename, *vars)
loadpkl(filename)
'''
from .rzioutils import loadmat
loadmat = loadmat.loadmat

from .rzioutils import loadmath5py
loadmath5py = loadmath5py.loadmath5py

from .rzioutils import replacehomepath
replacehomepath = replacehomepath.replacehomepath

from .rzioutils import matchfiles
matchfiles = matchfiles.matchfiles

from .rzioutils import getmultifilename
getmultifilename = getmultifilename.getmultifilename

from .rzioutils import savepkl
savepkl = savepkl.savepkl

from .rzioutils import loadpkl
loadpkl = loadpkl.loadpkl



