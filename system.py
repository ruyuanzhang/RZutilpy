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


def restart():
    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("reset")

    from IPython import get_ipython
    ipython = get_ipython()
    ipython.magic("run /Users/ruyuan/.ipython/profile_default/scientific_startup.py")


def unix_wrapper(cmd, wantreport=True, wantassert=True):
    '''
    unix_wrapper(cmd=cmd, wantreport=True, wantassert=True):

    A wrapper to run unix command, we utilize subprocess module in python 3.6.
    report <cmd> to the command window and then call <cmd>.
    after <cmd> is finished, report the status and the result to the command window.
    then, if <wantassert>, assert that the status returned is 0.
    if the status returned is not 0, we always display the
    result to the command window.
    finally, return the result.

    Args:
        cmd: a string as a list
        wantreport: is weather to report to command window, default:True
        wantassert: is weather to assert that status==0, default:True
    output:
        result:
    '''
    import subprocess

    # split the cmd into a word list so that subprocess module can run it
    # split by space
    cmd_torun = cmd.split(' ')

    if wantreport:
        print('\ncalling unix:\n{}\n'.format(cmd))
    # run the command
    completeprocess = subprocess.run(cmd_torun, stdout=subprocess.PIPE)
    if wantreport:
        print('status of unix command:\n{}\n'.format(completeprocess.returncode))
        print('result of unix command:\n' + completeprocess.stdout.decode("utf-8") + '\n')
    if wantassert:
        if completeprocess.returncode != 0:  # command fails
            print('unix command failed. here was the result:\n{}\n', completeprocess.stdout)
        assert (completeprocess.returncode == 0)
