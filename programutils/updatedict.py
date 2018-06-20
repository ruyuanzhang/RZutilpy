def updatedict(inputdict, targetdict, mode='check'):
    '''
    updatedict(inputdict, targetdict, mode='check'):

    <inputdict>: the input dict to merge from
    <targetdict>: the dict to merge to
    <mode>: a str, can be
        1. 'check' (default), indicates must check all keys in inputdict. If a
            key exists in inputdict but not in targetdict, we report an error.
        2. 'merge'. Merge all info in <inputdict> to <targetdict>. The keys that only
            exist in <inputdict> become new keys in <targetdict>.
        3. 'extract', only extract the keys that exist in both inputdict and targetdict.
            then update them from inputdict to targetdict


    we update info in <inputdict> to <targetdict> and return a <updatedict>, depending
    on <mode>. Note that <inputdict> and <targetdict> are not interchangable.

    Examples:
    a = rz.program.updatedict({'a':2}, {'a':1,'b':2})
    a = rz.program.updatedict({'a':2, 'c':2}, {'a':1,'b':2}, mode='merge')
    a = rz.program.updatedict({'a':2, 'c':2}, {'a':1,'b':2}, mode='extract')

    '''
    # check input
    assert isinstance(inputdict, dict) and isinstance(targetdict, dict), 'Should input two dicts!'
    if mode == 'check':
        # check all keys in inputdict all also in targetdict, otherwise
        if not all([k in targetdict.keys() for k in inputdict.keys()]):
            raise KeyError('keys (%s) in inputdict not in targetdict' %\
             ', '.join([k for k in inputdict.keys() if k not in targetdict.keys()]))

        # do it
        return {**targetdict, **inputdict}
    elif mode == 'merge':
        # do it
        return {**targetdict, **inputdict}
    elif mode == 'extract':
        # extract the common item from
        tmp = dict((k, inputdict[k]) for k in inputdict.keys() & targetdict.keys())
        return {**targetdict, **tmp}
    else:
        raise ValueError('Input mode is wrong!')