# -*- coding: utf-8 -*-
"""
matlab file read and write module

Created on 3/26/17

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

from .rzioutils import multifilename
multifilename = multifilename.multifilename

from .rzioutils import savepkl
savepkl = savepkl.savepkl

from .rzioutils import loadpkl
loadpkl = loadpkl.loadpkl



