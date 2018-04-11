def loadpkl(filename):
    '''
    loadpkl(filename):

    Equivalent function as load in matlab. Return a dict
    '''
    import pickle
    # open a file
    f = open(filename, 'rb')
    data = pickle.load(f)
    f.close
    return data