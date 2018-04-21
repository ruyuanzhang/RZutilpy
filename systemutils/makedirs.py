def makedirs(name, mode=None, exist_ok=True):
    '''
    wrapper of os.makedirs, except that we default exist_ok=True,
    In other words, do nothing if the folder exists, and create it if it
    does not
    '''
    from os import makedirs
    if mode is None:
        makedirs(name, exist_ok=exist_ok)
    else:
        makedirs(name, mode=mode, exist_ok=exist_ok)