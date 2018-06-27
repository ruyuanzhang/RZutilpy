def makedirs(name, mode=None, exist_ok=True):
    '''
    makedirs(name, mode=None, exist_ok=True):

    wrapper of os.makedirs, except that we default exist_ok=True,
    In other words, do nothing if the folder exists, and create it if it
    does not.We return True or False to indicate the success of creating the folder

    Note:
        1. if name is a dir, please add file sep in the end (i.e., '/home/folder/')
        2. The user homedir sign '~' is fine.

    <name> can be either
        (1) a folder name, like '/User/ruyuan/testpath'
        (2) a filename. like '/User/ruyuan/testpath/test.py'. in this case, we create
            the folder '/User/ruyuan/testpath/'
        '~/testpath' is OK
        only a filename 'test.py' is also ok, in this case we do not create any folder
        since we are already in this folder
    <mode>: folder permission, default:None
    <exist_ok>: whether OK if it is exist, if the folder exists, we do nothing

    We use name.suffix=='' to judge foldername of filename


    which means we want to save something in the current folder. Then we choose
    to do nothing special.

    The user homedir sign '~' is fine.

    Example:
        # make a folder name 'here' if it does not exist
        makedirs('~/here')
        # make a folder name 'home' if it does not exist
        makedirs('/home')
        # make a folder name 'home' if it does not exist
        makedirs('/home/heihei.png')

        # this is useful when saving a file but not sure whether the folder exists
        # if not, we create the folder for this file, the usage is below
        makedirs('/home/heihei.png')

    20180622 switch to use pathlib module

    '''
    from pathlib import Path

    name = Path(name)
    # replace home directory
    name = name.expanduser()

    if str(name.parent) == '.':  # make a file in the current, no need to make the dir
        return
    if name.suffix != '':  # the input is a file, we strip the filename and only keep the folder name
        name = name.parent

    # we cannot set the default in the func, so using this...
    # note that we make all parent folder if they do not exist
    if mode is None:
        try:
            name.mkdir(parents=True, exist_ok=exist_ok)
            return True  # this is helpful for assert
        except:
            print('Failed to make the dir %s!' % name)
            return False
    else:
        try:
            name.mkdir(mode=mode, parents=True, exist_ok=exist_ok)
            return True
        except:
            print('Failed to make the dir %s!' % name)
            return False