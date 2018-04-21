def replacehomepath(pattern):
    '''
    replacehomepath(pattern):

    replace home path like '~/test' to full path name, like 'Users/ruyuan/test'. We assume the pattern input is correct

    Note:
    20180419 start to use os.path.expanduser function
    '''
    import os.path as path

    # now use the os.path.expand user
    return path.expanduser(pattern)
