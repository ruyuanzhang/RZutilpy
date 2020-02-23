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

    Note that in jupyter notebook, you can just use "!" to signal a bash command
    This function is useful when using 

    Args:
        <cmd>: can be two cases:
            1. a string, contains the full unix command, like
                'flirt -in input.nii.gz -ref output.nii.gz'
            2. a list of strings that decomposite individual parts of the unix
                command, such as ['flirt', '-in', 'input.nii.gz', '-ref', 'output.nii.gz']
        <verbose>: report to command window (default 3),
            0: no verbose output at all
            1: only verbose auxiliary info
            2: verbose auxiliary info, and verbose information and return results generate by the command
                This is useful for debug
            3: only verbose the result generate by the command
        <wantreturn>: boolean(default:False), whether return result or error code
        <wantassert>: is weather to assert that status==0, stop executation when an error arises, default:True
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
        1. switch to Run??
        2. completely block output
    '''
    from subprocess import Popen, PIPE, STDOUT

    # split the cmd into a word list so that subprocess module can run it
    # check input
    if isinstance(cmd, str):       
        shell=True
        if 0<verbose<3:
            print(f'calling unix:\n{cmd}\n')
    elif isinstance(cmd, list):
        shell=False
        if 0<verbose<3:
            print(f'calling unix:\n{" ".join(cmd)}\n')
    else:
        raise ValueError('Wrong input!')

    # Run the command
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=shell)
    result=bytes()
    while True:
        line = p.stdout.readline()
        if not line:
            break
        else:
            result=result+line
            if verbose > 1:
                print(line.decode("utf-8",'ignore').replace('\n',''))
    p.wait() # wait the program complete

    if 0<verbose<3:
        print(f'\nstatus of unix command (0-succeeded otherwise failed):\n{p.returncode}\n')

    if resultfile: # save result to a files
        print(result.decode("utf-8"), file=open(resultfile, 'w'))

    if wantassert: # assert
        if p.returncode != 0:  # if return code is non-zero, command fails
            if 0<verbose<3:
                print(f'unix command failed. see result below:\n{result.decode("utf-8")}\n')
                raise Error('Execution fails!') # stop the command
                if wantreturn:
                    return p
    if wantreturn:
        return result.decode("utf-8",'ignore').replace('\n','')

