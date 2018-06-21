def restart():
    '''
    restart()

    restart ipython to default state, will clean all variables in workspace

    '''
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("reset")

    from IPython import get_ipython
    import socket
    ipython = get_ipython()
    if socket.gethostname() == 'RuyuanMPB.cmrr.umn.edu':
        ipython.magic("run /Users/ruyuan/.ipython/profile_default/scientific_startup.py")
    elif socket.gethostname() == 'stone':  # on stone
        ipython.magic("run /home/stone/ruyuan/.ipython/profile_default/scientific_startup.py")