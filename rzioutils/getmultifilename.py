def getmultifilename(pattern, N):
    '''
    getmultifilename(patterns, N)

    create multiple file names into a list <filenames>. <filenames> are labeled by numbers
    Useful when saving multiple files,e.g., multiple images

    <pattern>: a file pattern, e.g., 'image%02d'
    <N>: is :
        (1) int, 100.
        (2) a int array, like [1,2,3,4,5]

    Example:
        files = rz.rzio.getmultifilename('image%02d', N=10)

    '''
    from RZutilpy.system import Path
    from numpy import arange, ndarray

    pattern = Path(pattern).str  # replace '~' to home directory

    if isinstance(N, int):
        N = arange(N) + 1
    assert isinstance(N, ndarray), 'Input N is wrong, double check'

    try:
        filenames = [(pattern % i) for i in N]
    except ValueError:
        raise ValueError('The pattern seems wrong...check it')

    return filenames