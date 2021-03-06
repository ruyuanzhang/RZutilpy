def split2d(arr, nrows, ncols):
    """
    split2d(arr, nrows, ncols):

    Input:
        <arr>: must be a 2d array
        <nrows>,<ncols>: rows and cols of subbricks

    Return an array of shape (nrows, ncols, n) where
    n * nrows * ncols = arr.size. We assume that arr.size can be exactly divided
    by nrows * ncols

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.

    This function is useful to decompose mosaic image read from dicom files
    """
    from numpy import ndarray
    assert isinstance(arr, ndarray) and arr.ndim == 2, 'Please input a 2d array'

    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols)).transpose([1, 2, 0])