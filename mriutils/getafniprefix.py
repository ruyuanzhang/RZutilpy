def getafniprefix(filename):
    '''
    Extract afni dataset prefix. Afni dataset typically contains '+', we extract
    the name before '+' file. Assume only one '+' exists in the filename
    '''
    assert isinstance(filename,str), 'filename should be a string'
    import re
    from RZutilpy.system import Path

    p = re.compile(r'(.*)\+')
    matchgroup = p.match(filename)
    assert matchgroup is not None, 'no match!'
    fullprefix = matchgroup.group(1)
    # strip path information
    shortprefix = Path(fullprefix).pstem

    return shortprefix, fullprefix



