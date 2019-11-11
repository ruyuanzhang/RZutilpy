def mycd(dir='util'):
    """
    mycd(dir='util')

    quickly switch working directory

    a wrapper for quickly switching to directory of utility functions

    <dir>: a str, target dir. currently supprt
        'util': utility folder in RZ's laptop
        'main': go to user home directory

    Example:
        rz.system.mycd()
        rz.system.mycd('util')

    """
    import os
    if dir is 'util':
        os.chdir('/Users/ruyuan/Documents/Code_git/CodeRepositories/RZutilpy')
    elif dir is 'main':
        os.chdir('/Users/ruyuan')