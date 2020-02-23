def list2arrayobj(lst):
    '''
    Here we convert a list into an numpy array but set each element as an object in this array
    This is useful when perform cell-matlab like manipulation in python. 
    A standard np.array() will some how convert multiple dimensional list into different data type. 
    You can see the difference using the example below

    Example:
        a = [(2,3), (2,3), (2,3)]
        prit(np.array(a).shape)

        a = [(2,3), (2,3), (2,3)]
        prit(list2arrayobj(a))
    '''
    from numpy import empty
    assert isinstance(lst, list), 'Input is not a list!'
    
    tmp = empty(len(lst), dtype=object)
    tmp[:] = lst
    
    return tmp
    
