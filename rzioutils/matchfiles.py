def matchfiles(pattern, wantsort='name'):
    '''
    matchfiles(pattern, wantsort='name'):

    return a list of filename following a wildcard expression pattern. We use
    glob module here. Another option is fnmatch module. The difference is that
    glob will not match the files start with '.'

    <pattern> is
        (1)a string that matches zero or more files or directories (wildcards '*' okay).
        (2) or a list of strings of (1)

    <wantsort> indicates the key function (e.g., {'name', 'time'}) input for sorted function.
        search 'sorted' in python for more information. It can be {'name', 'time'},
        indicating sorting the files by name and the last-modification time
        Default: 'name'

    If only one match pattern is supplied, we output
    (1) a string, if only one file is matched
    (2) a list of string, if multiple files are matched

    If multiple match patterns are supplied, we output a list of cases of output
    for one match pattern

    History:
        20180621 implement multiple input patterns as a string list
        20180517 add reminder when no matchfiled files
        20180430 RZ adds sort arg. Original filenames returned by glob.glob
            is not sorted.

    '''
    from os import path
    from glob import glob

    if isinstance(pattern, str):
        pattern = [pattern]

    # do it
    filelist = [glob(path.expanduser(p)) for p in pattern]

    #
    if not filelist:   # no match
        print('No matched files for this pattern!')

    if wantsort == 'name':
        filelist = [sorted(f, key=path.basename) for f in filelist]
    elif wantsort == 'time':
        filelist = [sorted(f, key=path.getmtime) for f in filelist]
    else:
        print('filenames not sorted')

    if len(pattern) == 1: # only one match input
        return filelist[0][0] if len(filelist[0])==1 else filelist[0]
    else:  # multiple match input
        return [f[0] if len(f)==1 else f for f in filelist]