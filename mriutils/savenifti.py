def savenifti(arr, filename, niftiobj=None, affine=None, header=None):
    '''
    savenii(arr, niftiobj, filename):

    save 3D or 4D <array> into a full nifti filename using <filename>. We used
    the affine and header information from <niftiobj>.

    Note that the file name can have either the ext as '.nii' or '.nii.gz'. nibabel
    can take care of it.

    If <affine> or <header> is supplied, they will overwrite information from the <niftiobj>

    20180622 RZ add support for affine and header

    '''
    from nibabel import save, Nifti1Image
    from numpy import ndarray
    from RZutilpy.system import makedirsquiet

    # check input
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input 3d or 4d an ndarray!'

    # make the dir if it does not exist
    makedirsquiet(filename) # note here we add a os.sep

    if affine is None or header is None:
        assert isinstance(niftiobj, Nifti1Image), 'affine or header is none, you must supply niftiobj'

    # get affine and header information
    affine = niftiobj.affine if affine is None else affine
    header = niftiobj.header if header is None else header

    save(Nifti1Image(arr, affine, header), filename)

