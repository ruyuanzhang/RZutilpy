def savejson(filename, varsdict):
    '''
    def savejson(filename, varsdict):

    <filename>: a string 'test.json', or 'test', can have full path
    <varsdict>: a dict to save


    '''

    from json import dump
    from RZutilpy.system import Path, makedirs

    filename = Path(filename)
    makedirs(filename)

    # open a file
    f = open('{}.json'.format(filename.strnosuffix), 'w')
    dump(varsdict, f, indent=4)
    f.close()