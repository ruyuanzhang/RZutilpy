def savemgz(arr, filename, mgzobj=None, affine=None, header=None):
    '''
    savemgz(arr, filename, mgzobj=None, affine=None, header=None):

    save 3D into a full mgz filename using <filename>. We used
    the affine and header information from <mgzobj>.

    If <affine> or <header> is supplied, they will overwrite information from the <mgzobj>

    '''
    from nibabel import save, MGZImage
    from numpy import ndarray
    from RZutilpy.system import makedirsquiet

    # check input
    assert isinstance(arr, ndarray) and (3<=arr.ndim<=4), 'Please input an ndarray!'

    # make the dir if it does not exist
    makedirsquiet(filename)

    assert isinstance(mgzobj, Nifti1Image) if affine is None or header is None, \
    'affine or header is none, you must supply mgzobj'

    # get affine and header information
    affine = mgzobj.affine if affine is None
    header = mgzobj.header if header is None

    # save the file
    save(MGZImage(arr, affine, header), filename)

