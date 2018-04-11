def multifilename(pattern, N):
    '''
    multifilename(patterns, N)

    create multiple file names into a list. Filenames are labeled by numbers Useful when saving multiple files,e.g., multiple images

    <pattern>: a file pattern, e.g., 'image%02d'
    <N>: is :
        (1) int, 100.
        (2) a number array, like [1,2,3,4,5]

    '''
    from RZutilpy.rzio import replacehomepath
    import numpy as np

    pattern = replacehomepath(pattern)  # replace '~' to home directory

    filename = list()
    if isinstance(N, int):
        N = np.arange(N) + 1
    assert isinstance(N, np.ndarray), 'Input N is wrong, double check'

    try:
        for i in N:
            filename.append(pattern % i)
    except ValueError:
        raise ValueError('The pattern seems wrong...check it')

    return filename