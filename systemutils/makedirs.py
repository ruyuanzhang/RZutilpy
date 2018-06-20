def makedirs(name, mode=None, exist_ok=True):
    '''
    makedirs(name, mode=None, exist_ok=True):

    wrapper of os.makedirs, except that we default exist_ok=True,
    In other words, do nothing if the folder exists, and create it if it
    does not.We return True or False to indicate the success of creating the folder

    Note:
        1. if name is a dir, please add file sep in the end (i.e., '/home/folder/')
        2. The user homedir sign '~' is fine.

    <name> can be either a folder name or a filename. If a filename, we create
        a folder for this file. This is useful when saving the file to an unknown path.
    <mode>:
    <exist_ok>: whether OK if it is exist, if the folder exists, we do nothing

    We use os.path.dirname to extract the folder name from <name>.

    So, if name is a dir, please add file sep in the end (i.e., '/home/folder/'),

    A file name is fine.  We also check whether dirname is empty,
    which means we want to save something in the current folder. Then we choose
    to do nothing special.

    The user homedir sign '~' is fine.

    Example:
        makedirs('~/here/')
        makedirs('/home/')

        # this is useful when saving a file but not sure whether the folder exists
        makedirs('/home/heihei.png')

    '''
    from os import makedirs
    from os.path import dirname, expanduser

    name = dirname(expanduser(name))
    print(name)

    if name is '':  # we are in the current folder
        return

    # we cannot set the default in the func, so using this...
    if mode is None:
        try:
            makedirs(name, exist_ok=exist_ok)
            return True
        except:
            print('Failed to make the dir!')
            return False
    else:
        try:
            makedirs(name, mode=mode, exist_ok=exist_ok)
            return True
        except:
            print('Failed to make the dir!')
            return False