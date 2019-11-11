def loadpkl(filename,varname=None):
    '''
    loadpkl(filename):

    Equivalent function as load in matlab. Return a dict load from pkl file

    20180814 add only load one varname
    20180714 <filename> accept path-like obj, use dill replace pickle
    '''
    from dill import load
    from RZutilpy.system import Path

    # convert to path-like object
    filename = Path(filename) if not isinstance(filename, Path) else filename

    # open a file
    f = open(filename.str, 'rb')
    data = load(f)
    f.close
    return data[varname] if varname is not None else data