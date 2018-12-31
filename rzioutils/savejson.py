def savejson(filename, varsdict):
    '''
    def savejson(filename, varsdict):

    <filename>: a string 'test.pkl', or 'test'
        with .pkl extension, filename of the pickle file, variable should be saved as 'filename.pkl'
    <varsdict>: a dict to save

    20180715 RZ switch to use dill
    '''

    from json import dump
    from RZutilpy.system import Path

    filename = Path(filename) if ~isinstance(filename, Path) else filename

    # open a file
    f = open('{}.json'.format(filename.strnosuffix), 'w')
    dump(varsdict, f, indent=4)
    f.close()