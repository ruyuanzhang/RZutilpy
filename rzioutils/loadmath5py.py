def loadmath5py(filename):
    """
    Similar to loadmat function, except that this function import h5py package to read v7.3 mat file


    can only supply the <filename> and read in all datas

    Return, exmaple see loadmat function

    To do:
        1. consider to selective read in?

    """
    from h5py import File
    import numpy as np
    print('read the file' + filename)
    Fileobject = File(filename,'r')
    keys = []
    values = []
    mat_contend = {}

    for k, v in Fileobject.items():
        keys.append(k)
        values.append(v)
        mat_contend[k] = np.array(v)

    #del keys[0:3]  # remove first 3 information keys.
    #del values[0:3]  # delete first 3 values
    return mat_contend, keys, values