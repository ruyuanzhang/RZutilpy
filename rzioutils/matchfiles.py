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
    filelist = glob.glob(replacehomepath(pattern))
    return filelist[0] if len(filelist)==1 else filelist