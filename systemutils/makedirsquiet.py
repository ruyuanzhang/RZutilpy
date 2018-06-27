def makedirsquiet(name, mode, exist_ok=True):
    '''
    wrapper of makedirs, we assert the success and raise an error if failure
    '''
    from RZutilpy.system import makedirs
    assert makedirs(name, mode, exist_ok), 'Failed to make the dir'