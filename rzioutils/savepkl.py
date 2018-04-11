def savepkl(filename, varsdict):
    '''
    savepkl(filename, varsnamelist):

    Equivalent function as save in matlab. Save function save multiple variables
    into a .mat file. This function save several variables into a pickle file.

    <filename>: a string, filename of the pickle file, variable should be saved as 'filename.pkl'
    <varsdict>: a dict to save
    '''
    import pickle
    # open a file
    f = open('{}.pkl'.format(filename), 'wb')
    pickle.dump(varsdict, f)
    f.close()