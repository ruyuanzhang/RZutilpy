def restart():
    '''
    restart()

    restart ipython to default state, will clean all variables in workspace

    '''
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("reset")

    from socket import gethostname
    if gethostname() == 'RuyuanMPB.cmrr.umn.edu':
        ipython.magic("run /Users/ruyuan/.ipython/profile_default/scientific_startup.py")
    elif gethostname() == 'stone' or 'stone.cmrr.umn.edu':  # on stone
        ipython.magic("run /home/stone/ruyuan/.ipython/profile_default/scientific_startup.py")