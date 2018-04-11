def mycd(dir='util'):
    """
    funname(a,b,*c,**d)
    quickly switch working directory

    a wrapper for quickly switching to directory of utility functions

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