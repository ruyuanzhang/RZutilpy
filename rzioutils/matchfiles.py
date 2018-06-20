def matchfiles(pattern, wantsort='name'):
    '''
    matchfiles(pattern, wantsort='name'):

    return a list of filename following a wildcard expression pattern. We use
    glob module here. Another option is fnmatch module. The difference is that
    glob will not match the files start with '.'

    <pattern> is a string that matches zero or more files or directories
        (wildcards '*' okay).
    <wantsort> indicates the key function (e.g., {'name', 'time'}) input for sorted function.
        search 'sorted' in python for more information. It can be {'name', 'time'},
        indicating sorting the files by name and the last-modification time
        Default: 'name'

    History:
        20180517 add reminder when no matchfiled files
        20180430 RZ adds sort arg. Original filenames returned by glob.glob
            is not sorted.

    '''
    from os import path
    from glob import glob

    filelist = glob(path.expanduser(pattern))

    if wantsort == 'name':
        filelist = sorted(filelist, key=path.basename)
    elif wantsort == 'time':
        filelist = sorted(filelist, key=path.getmtime)
    else:
        print('file names not sorted')

    if not filelist:   # no match
        print('No matched files!')

    return filelist[0] if len(filelist)==1 else filelist