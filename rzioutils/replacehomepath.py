def replacehomepath(pattern):
    '''
    replacehomepath(pattern):

    replace home path like '~/test' to full path name, like 'Users/ruyuan/test'.
    We assume the pattern input is correct

    Note:
    20180419 start to use os.path.expanduser function
    '''
    from os.path import expanduser

    # now use the os.path.expand user
    return expanduser(pattern)
