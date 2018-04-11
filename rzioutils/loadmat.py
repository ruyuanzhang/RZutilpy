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