def makedirs(name, mode=None, exist_ok=True, wantassert=True):
    '''
    makedirs(name, mode=None, exist_ok=True):

    Wrapper of os.makedirs, except that we default exist_ok=True,
    In other words, do nothing if the folder exists, and create it if it
    does not.We return True or False to indicate the success of creating the folder

    Note:
        1. a name without suffixes will be treated as a folder
        2. a name with suffixes will be treated as a file
        3. The user homedir sign '~' is fine, we replace it with

    <name> can be either
        (1) a str folder name, like '/User/ruyuan/testpath'
        (2) a filename. like '/User/ruyuan/testpath/test.py'. in this case, we create
            the folder '/User/ruyuan/testpath/'
            '~/testpath' is OK
            only a filename 'test.py' is also ok, in this case we do not create any folder
            since we are already in this folder
        (3) a Path or path-like object

    <mode>: folder permission, default:None
    <exist_ok>: whether OK if it is exist, if the folder exists, we do nothing
    <wantassert>: raise error if fail

    which means we want to save something in the current folder. Then we choose
    to do nothing special.

    Example:
        # make a folder name 'here' if it does not exist
        makedirs('~/here')
        # make a folder name 'home' if it does not exist
        makedirs('/home')
        # make a folder name 'home' if it does not exist
        makedirs('/home/heihei.png')

        # This is useful when saving a file but not sure whether the folder exists
        # if not, we create the folder for this file, the usage is below
        makedirs('/home/heihei.png')

    History:

    20190117 RZ fixed the bug, create a folder for a existing file
    20180714 <name> now can be a path-like object or a string
    20180622 switch to use pathlib module

    '''
    from RZutilpy.system import Path

    # convert to rzpath object
    name = Path(name) if not isinstance(name, Path) else name

    # change name to its parent folder if it is a file or have suffixes
    name = name.parent if name.suffixes != [] or name.is_file() else name

    # we cannot set the default in the func, so using this...
    # note that we make all parent folder if they do not exist
    if mode is None:
        try:
            name.mkdir(parents=True, exist_ok=exist_ok)
            return True  # this is helpful for assert
        except:
            print('Failed to make the dir %s!' % name.str)
            if wantassert:
                raise NameError('Failed to make the dir %s!' % name.str)
            return False
    else:
        try:
            name.mkdir(mode=mode, parents=True, exist_ok=exist_ok)
            return True
        except:
            print('Failed to make the dir %s!' % name.str)
            if wantassert:
                raise NameError('Failed to make the dir %s!' % name.str)
            return False