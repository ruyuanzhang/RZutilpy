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


def loadmat(filename, **kwargs):
    """
    myloadmat(filename)
    Ruyuan's load matfile, wrapper of scipy.io.loadmat.

    This function is mainly used to load in matlab matfile, we remove some
    redundant information, i.e. _header_ and only keep valid saved data.

    Args:
        filename: a string of filename to read, e.g., 'read'
        **kwargs: kwargs follow same definition of scipy.io.loadmat, can check it
            using help(scipy.io.loadmat)

    Returns: a tuple
        mat_contend: the dict that scipy.io.loadmat produces to load the matfile
        keys: a list of keys in mat_c
        ontend
        values: a list of values in mat_contend

    Example:
        mat,keys,values = myloadmat('data01.mat')

    History and Notes:
        20170802 RZ add more input
        20170326 RZ created it


    """
    import scipy.io as spio
    print(filename)
    mat_contend = spio.loadmat(filename,**kwargs)
    keys = list(mat_contend.keys())  # we read keys as a list
    values = list(mat_contend.values())
    del keys[0:3]  # remove first 3 information keys.
    del values[0:3]  # delete first 3 values
    return mat_contend, keys, values


def loadmath5py(filename):
    """
    Similar to loadmat function, except that this function import h5py package to read v7.3 mat file

    Args:
        can only suppy the filename and read in all datas

    Return, exmaple see loadmat function

    Note:
        1. consider to selective read in?

    """
    import h5py
    import numpy as np
    print('read the file' + filename)
    Fileobject = h5py.File(filename,'r')
    keys = []
    values = []
    mat_contend = {}

    for v,k in Fileobject.items():
        keys.append(v)
        values.append(k)
        mat_contend[v] = np.array(k)

    #del keys[0:3]  # remove first 3 information keys.
    #del values[0:3]  # delete first 3 values
    return mat_contend, keys, values


def replacehomepath(pattern):
    '''
    replacehomepath(pattern):

    replace home path like '~/test' to full path name, like 'Users/ruyuan/test'. We assume the pattern input is correct
    '''
    import re
    from pathlib import Path  # this is new since python 3.5
    home = str(Path.home())
    reg = re.compile('~.')

    if re.match(reg, pattern):
        pattern = pattern.replace('~', home)
    return pattern


def matchfiles(pattern):
    '''
    matchfiles(pattern)

    return a list of filename following a wildcard expression pattern. We use
    glob module here. Another option is fnmatch module. The difference is that
    glob will not match the files start with '.'

    patterns is
    a string that matches zero or more files or directories (wildcards '*' okay)

    '''
    from RZutilpy.rzio import replacehomepath
    import glob
    return glob.glob(replacehomepath(pattern))


def multifilename(pattern, N):
    '''
    multifilename(patterns, N)

    create multiple file names into a list. Filenames are labeled by numbers Useful when saving multiple files,e.g., multiple images

    <pattern>: a file pattern, e.g., 'image%02d'
    <N>: is :
        (1) int, 100.
        (2) a number array, like [1,2,3,4,5]

    '''
    from RZutilpy.rzio import replacehomepath
    import numpy as np

    pattern = replacehomepath(pattern)  # replace '~' to home directory

    filename = list()
    if isinstance(N, int):
        N = np.arange(N) + 1
    assert isinstance(N, np.ndarray), 'Input N is wrong, double check'

    try:
        for i in N:
            filename.append(pattern % i)
    except ValueError:
        raise ValueError('The pattern seems wrong...check it')

    return filename


def savepkl(filename, varsdict):
    '''
    savepkl(filename, varsnamelist):

    Equivalent function as save in matlab. Save function save multiple variables
    into a .mat file. This function save several variables into a pickle file.

    <filename>: a string, filename of the pickle file, variable should be saved as 'filename.pkl'
    <varsdict>: a dict to save
    '''
    import pickle
    # open a file
    f = open('{}.pkl'.format(filename), 'wb')
    pickle.dump(varsdict, f)
    f.close()


def loadpkl(filename):
    '''
    loadpkl(filename):

    Equivalent function as load in matlab. Return a dict
    '''
    import pickle
    # open a file
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close
    return data


