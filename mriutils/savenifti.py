def savenifti(arr, filename, niftiobj=None, affine=None, header=None):
    '''
    savenifti(arr, filename, niftiobj=None, affine=None, header=None):

    save 3D or 4D <array> into a full nifti filename using <filename>. We used
    the affine and header information from <niftiobj>.

    Note that the file name can have either the ext as '.nii' or '.nii.gz'. nibabel
    can take care of it.

    If <affine> or <header> is supplied, they will overwrite information from the <niftiobj>

    20180622 RZ add support for affine and header

    '''
    from nibabel import save, Nifti1Image
    from numpy import ndarray
    from RZutilpy.system import makedirs, Path

    # check input
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input 3d or 4d an ndarray!'

    # make the dir if it does not exist
    filename = Path(filename) if ~isinstance(filename,Path) else filename
    makedirs(filename) # note here we add a os.sep

    if affine is None or header is None:
        assert isinstance(niftiobj, Nifti1Image), 'affine or header is none, you must supply niftiobj'

    # get affine and header information
    affine = niftiobj.affine.copy() if affine is None else affine.copy()
    header = niftiobj.header.copy() if header is None else header.copy()

    save(Nifti1Image(arr, affine, header), filename.str)

