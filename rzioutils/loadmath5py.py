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