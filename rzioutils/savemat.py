def savemat(filename, dict, exist_ok=False, **kwargs):
    """
    savemat(filename, **kwargs):

    load .mat file, a wrapper of scipy.io.savemat.

    This function is mainly used to save a dict into matlab matfile.

    Args:
        <filename>: a string of filename to read, e.g., 'read'
        **kwargs: kwargs for scipy.io.loadmat function, can check it
            using help(scipy.io.loadmat)

    Returns: a tuple (mat_contend, )
        <mat_contend>: a dict that scipy.io.loadmat produces to load the matfile
        <keys>: a list of keys in <mat_contend>
        <values>: a list of values in <mat_contend>

    Example:
        savemat('data01.mat', '')

    History and Notes:
        201901220


    """
    from scipy.io import savemat
    from RZutilpy.system import Path,makedirs

    # convert str to path-like object
    filename = Path(filename) if not isinstance(filename, Path) else filename

    try:
        savemat(filename.str, **kwargs)
        return True
    except:
        raise IOError('can not save the file!')