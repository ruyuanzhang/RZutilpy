def loadmat(filename, **kwargs):
    """
    loadmat(filename, **kwargs):

    load .mat file, a wrapper of scipy.io.loadmat.

    This function is mainly used to load in matlab matfile, we remove some
    redundant information, i.e. _header_ and only keep valid saved data.

    Args:
        <filename>: a string of filename to read, e.g., 'read'
        **kwargs: kwargs for scipy.io.loadmat function, can check it
            using help(scipy.io.loadmat)

    Returns: a tuple (mat_contend, )
        <mat_contend>: a dict that scipy.io.loadmat produces to load the matfile
        <keys>: a list of keys in <mat_contend>
        <values>: a list of values in <mat_contend>

    Example:
        mat,keys,values = loadmat('data01.mat')

    History and Notes:
        20180720 <filename> can accept Path object
        20170802 RZ add more input
        20170326 RZ created it


    """
    import scipy.io as spio
    from RZutilpy.system import Path

    # convert str to path-like object
    filename = Path(filename) if not isinstance(filename, Path) else filename

    print('read in' + filename.str + '...')
    mat_contend = spio.loadmat(filename.str, **kwargs)
    keys = list(mat_contend.keys())  # we read keys as a list
    values = list(mat_contend.values())
    del keys[0:3]  # remove first 3 information keys.
    del values[0:3]  # delete first 3 values
    return mat_contend, keys, values