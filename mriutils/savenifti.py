def savenifti(arr, filename, niftiobj):
    '''
    savenii(arr, niftiobj, filename):

    save 3D or 4D <array> into a full nifti filename using <filename>. We used
    the affine and header information from <niftiobj>.

    Note that the file name can have either the ext as '.nii' or '.nii.gz'. nibabel
    can take care of it.

    '''
    from nibabel import save, Nifti1Image
    from numpy import ndarray
    from RZutilpy.system import makedirs
    from os.path import dirname

    # check input
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input an ndarray!'
    assert isinstance(niftiobj, Nifti1Image), 'Please input an correct nifti object in the third argument!'

    # make the dir if it does not exist
    assert makedirs(dirname(filename))

    # save it
    newobj = Nifti1Image(arr, niftiobj.affine, niftiobj.header)
    save(newobj, filename)

