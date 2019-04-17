def unix_wrapper(cmd, verbose=3, wantreturn=False, wantassert=True, resultfile=None):
    '''
    unix_wrapper(cmd, verbose=3, wantassert=True, resultfile=None):

    A wrapper to run unix command, we utilize subprocess module in python 3.6.
    report <cmd> to the command window and then call <cmd>.
    after <cmd> is finished, report the status and the result to the command window.
    then, if <wantassert>, assert that the status returned is 0.
    if the status returned is not 0, we always display the
    result to the command window.
    finally, return the result.

    Args:
        <cmd>: can be two cases:
            1. a string, contains the full unix command, like
                'flirt -in input.nii.gz -ref output.nii.gz'
            2. a list of strings that decomposite individual parts of the unix
                command, such as ['firt', '-in', 'input.nii.gz', '-ref', 'output.nii.gz']
        <verbose>: report to command window (default 3),
            0: no output at all
            1: only output auxiliary info
            2: output auxiliary info, and output and return generate by the command
                This is useful for debug
            3: only output generate by the command
        <wantreturn>: boolean(default:False), whether return result or error code
        <wantassert>: is weather to assert that status==0, default:True
        <resultfile>: a string, filename to save the output
    output:
        result: the output result of the unix command

    History:
        20190415 add <wantreturn>, always return the output str
        20190414 change <verbose> to 4 levels, and default no return output
        20181110 add <resultfile> input, change report to realtime
        20180620 add return the unix result
        20180508 RZ add list input option

    To do:
        1. report error and stop but return the output status
        2. completely block output
    '''
    from subprocess import Popen, PIPE, STDOUT

    # split the cmd into a word list so that subprocess module can run it
    # split by space
    if isinstance(cmd, str):
        shell=True
        if 0<verbose<3:
            print('calling unix:\n{}\n'.format(cmd))
    elif isinstance(cmd, list):
        shell=False
        if 0<verbose<3:
            print('calling unix:\n{}\n'.format(' '.join(cmd)))
    else:
        raise ValueError('Wrong input!')

    # run the command
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=shell)
    result=bytes()
    while True:
        line = p.stdout.readline()
        if not line:
            break
        else:
            result=result+line
            if verbose==2 or verbose==3:
                print(line.decode("utf-8",'ignore').replace('\n',''))
    p.wait()

    if 0<verbose<3:
        print('\nstatus of unix command (0-succeeded otherwise failed):\n{}\n'.format(p.returncode))

    if resultfile: # save result to a files
        print(result.decode("utf-8"), file=open(resultfile, 'w'))

    if wantassert:
        if p.returncode != 0:  # command fails
            if 0<verbose<3:
                print('unix command failed. see result below:\n{}\n'.format(result.decode("utf-8")))
                if wantreturn:
                    return p
                raise Error('Execution fails!')
    if wantreturn:
        return result.decode("utf-8",'ignore').replace('\n','')

