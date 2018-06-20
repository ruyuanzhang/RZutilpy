def loadpkl(filename):
    '''
    loadpkl(filename):

    Equivalent function as load in matlab. Return a dict
    '''
    from pickle import load
    # open a file
    f = open(filename, 'rb')
    data = load(f)
    f.close
    return data