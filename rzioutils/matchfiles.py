def matchfiles(pattern, wantsort='numName'):
    '''
    matchfiles(pattern, wantsort='numName'):

    return a list of filename following a wildcard expression pattern. We use
    glob module here. Another option is fnmatch module. The difference is that
    glob will not match the files start with '.'

    <pattern> is
        (1)a string that matches zero or more files or directories (wildcards '*' okay).
        (2) or a list of strings of (1)
        NOTE THAT WE DO NOT ACCEPT PATH OBJECT, ONLY STRING!!!

    <wantsort> indicates the key function (e.g., {'numName', 'name', 'time'}) input for sorted function.
        search 'sorted' in python for more information. It can be {'numName','name', 'time'},
        indicating sorting the files by name and the last-modification time. 'numName' consider
        the numerical number in a string
        Default: 'numName'

    If only one match pattern is supplied, we output
    (1) a string, if only one file is matched
    (2) a list of string, if multiple files are matched

    If multiple match patterns are supplied, we output a list of cases of output
    for one match pattern

    Note that we first convert the pattern to absolute path to ensure the output is
    also absolute path

    History:
        20181231 rz add numerical string functionality
        20180930 output list of string
        20180714 now return all paths as path-like objects, but <pattern> still need to be string
        20180626 always output absolute path
        20180624 support relative path, like '../test.py'
        20180621 implement multiple input patterns as a string list
        20180517 add reminder when no matchfiled files
        20180430 RZ adds sort arg. Original filenames returned by glob.glob
            is not sorted.
    '''
    import os
    import re
    from glob import glob
    from RZutilpy.system import Path

    # first covert them to Path object
    if isinstance(pattern, str):
        pattern = [Path(pattern)]
    else:
        pattern = [Path(p) for p in pattern]

    # do it, we still supply str to glob function
    filelist = [glob(p.str) for p in pattern]  # note filelist is a list of string

    #
    if len([p for p in filelist if len(p)==0]) > 0:   # no match
        print('Note, can not match some patterns...')

    if wantsort == 'name':
        filelist = [sorted(f, key=os.path.basename) for f in filelist]
    elif wantsort == 'time':
        filelist = [sorted(f, key=os.path.getmtime) for f in filelist]
    elif wantsort == 'numName':
        def stringSplitByNumbers(x):
            r = re.compile('(\d+)')
            l = r.split(x)
            return [int(y) if y.isdigit() else y for y in l]
        filelist = [sorted(f, key=stringSplitByNumbers) for f in filelist]
    else:
        print('filenames not sorted')


    if len(pattern) == 1: # only one match input
        return filelist[0][0] if len(filelist[0])==1 else [p for p in filelist[0]]
    else:  # multiple match input
        return [f[0] if len(f)==1 else [p for p in f] for f in filelist]