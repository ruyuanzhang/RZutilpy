def mycd(dir='util'):
    """
    funname(a,b,*c,**d)
    quickly switch working directory

    full explanation

    Args:
        dir: target dir. currently supprt
            'util': utility folder in RZ's laptop


    Return:


    Notes:


    Example:
        import rzutilpy as rzpy
        rzpy.mycd('util')

    History:
        4/6/17   RZ created it

    """
    import os
    if dir is 'util':
        os.chdir('/Users/ruyuan/Documents/Code_git/CodeRepositories/RZutilpy')
    elif dir is 'main':
        os.chdir('/Users/ruyuan')


def restart():
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("reset")

    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("run /Users/ruyuan/.ipython/profile_default/scientific_startup.py")
