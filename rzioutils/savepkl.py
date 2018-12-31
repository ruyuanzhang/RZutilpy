def savepkl(filename, varsdict):
    '''
    savepkl(filename, varsnamelist):

    Equivalent function as save in matlab. Save function save multiple variables
    into a .pkl file. This function save several variables into a pickle file.

    <filename>: a string 'test.pkl', or 'test'
        with .pkl extension, filename of the pickle file, variable should be saved as 'filename.pkl'
    <varsdict>: a dict to save

    '''

    from json import dumps
    from RZutilpy.system import Path

    filename = Path(filename) if ~isinstance(filename, Path) else filename

    # open a file
    f = open('{}.json'.format(filename.strnosuffix), 'wb')
    dump(varsdict, f)
    f.close()