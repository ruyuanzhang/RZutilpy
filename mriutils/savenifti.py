def savenifti(arr, filename, niftiobj):
    '''
    savenii(arr, niftiobj, filename):

    save 3D or 4D <array> into a full nifti filename using <filename>. We used
    the affine and header information from <niftiobj>.

    '''
    from nibabel import save, Nifti1Image
    from numpy import ndarray
    from RZutilpy.system import makedirs
    from os.path import dirname

    # check input
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input an ndarray!'
    assert isinstance(niftiobj, Nifti1Image), 'Please input an ndarray!'

    # make the dir if it does not exist
    makedirs(dirname(filename))

    # save it
    newobj = Nifti1Image(arr, niftiobj.affine, niftiobj.header)
    save(newobj, filename)

