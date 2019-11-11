def savemgz(arr, filename, mgzobj=None, affine=None, header=None):
    '''
    savemgz(arr, filename, mgzobj=None, affine=None, header=None):

    save 3D into a full mgz filename using <filename>. We used
    the affine and header information from <mgzobj>.

    If <affine> or <header> is supplied, they will overwrite information from the <mgzobj>

    20180720 <filename> can accept a path-like object

    '''
    from nibabel import save, MGZImage
    from numpy import ndarray
    from RZutilpy.system import makedirs, rzpath

    # check input, do we need this? I think mgz also accept 1d surface number??
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input an ndarray!'

    # make the dir if it does not exist
    filename = rzpath(filename) if ~isinstance(filename,rzpath) else filename

    makedirs(filename)

    assert isinstance(mgzobj, Nifti1Image) if affine is None or header is None, \
    'affine or header is none, you must supply mgzobj'

    # get affine and header information
    affine = mgzobj.affine if affine is None
    header = mgzobj.header if header is None

    # save the file
    save(MGZImage(arr, affine, header), filename.str)

