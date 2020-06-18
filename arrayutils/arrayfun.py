def arrayfun(func, *arr):
    '''
    apply <func> function to each element in one or multiple numpy array <arr>

    This is to resemble cellfun in Matlab. Sometimes we create a numpy array with dtype as object and manipulate it as cell array in matlab.
    np.vectorize only accepts a single scale into function, which is weird

    Note that in many cases you can directly vectorize arrays to perform some computation and no need to use this function

    All <arr> should have the same shape, but we explicitly check it

    If the output of each element is a tuple, we unpack it into differnet list

    '''

    from numpy import ndarray, array, empty, shape
    from RZutilpy.array import list2arrayobj
    # check input
    assert callable(func), '1st input should be a function!'
    assert all(isinstance(i, ndarray) for i in arr), 'Input should be np arrays!'
    assert len(set([shape(i) for i in arr])) <= 1, 'all input arrays should have the same shape'

    # figure out the shape
    arrayShape = arr[0].shape  # get original shape
    result = list2arrayobj(list(map(func, *[i.flatten() for i in arr])))
    # we have to create an empry array to contain the result
    # here is the trick we have to use a 
    
    if isinstance(result[0], tuple): # multiple output, note that this might not be accurate
        nOut = len(result[0])
        return [list2arrayobj([el[i] for el in result]).reshape(arrayShape) for i in range(nOut)]
    else:
        return result.reshape(arrayShape)
