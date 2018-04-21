def splitmulti(a, targetndim):
    '''
    splitmulti(a, targetndim)

    Reshape a list when the elements in the list have the same shape.a

    List can be reshaped by np.reshape function. However, if the elements in the
    list are all ndarrays, and share the same dimension. Using np.reshape will
    automatically concatenate all elements.
    i.e.,
    a = [[1,2], [1,2], [1,2], [1,2]]

    To avoid that, we use some hack here.

    Input:
        <l>: must be a 1d list, assume the all elements are ndarrays.
        <csize>: the size to reshape to
    Output:
        a reshaped list with shape csize


    '''
    import RZutilpy as rz

    rz.array.checkarray(a)

    if a.ndim == targetndim:
        return a
    elif a.ndim > targetndim:
        a = rz.array.split(a, axis=0)
        a = [splitmulti(x, targetndim) for x in a]
        return a
    else:
        raise ValueError('dimension is wrong!')
