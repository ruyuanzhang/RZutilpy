def loadjson(filename, varname=None):
    '''
    loadjson(filename, varname=None)

    load jsonfile

    '''
    from json import load
    from RZutilpy.system import Path

    # convert to path-like object
    filename = Path(filename) if not isinstance(filename, Path) else filename

    # open a file
    with open(filename.str) as f:
        data = load(f)

    return data[varname] if varname is not None else data