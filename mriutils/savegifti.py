def savegifti(arr, filename, giftiobj, intent=2005):
    '''
    savegifti(arr, filename, giftiobj, intent=2005)::

    save 1D or 2D <array> into a full gifti filename using <filename>. We used
    the affine and header information from <giftiobj>.

    Note that the file name should have '.gii'. nibabel cannot read '.gii.gz' file

    This is different from readgifti, we must supply an reference <giftiobj> to save the data


    <intent> is a list of integers with intent numbers for each column of arr. Typically
    we can treat it as a normal morph data, so default is 2005. For multiple columns
    in <arr>, you should input a list such as [2005, 2005, 2005]. For full list intent code.
    check the website below:

    https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/group__NIFTI1__INTENT__CODES.html/document_view


    20190409 RZ created it

    '''

    from nibabel import save
    from nibabel.gifti import GiftiDataArray
    from numpy import ndarray
    from RZutilpy.system import makedirs, Path
    from nibabel.gifti.giftiio import write as giftiwrite

    # check input
    assert isinstance(arr, ndarray) and (1<=arr.ndim<=2), 'Please input 1d or 2d an ndarray!'

    # make the dir if it does not exist
    filename = Path(filename) if ~isinstance(filename,Path) else filename
    # add .gii suffix if not supplied
    filename = Path(filename.str+'.gii') if filename.suffix != '.gii' else filename

    makedirs(filename) # note here we add a os.sep

    # make darrays for each column
    if arr.ndim == 1:
        giftiobj.darrays[0].data = arr
        giftiobj.darrays[0].intent = intent
    else:
        assert len(intent)==arr.shape[1], 'data column number not equal to intent number!'
        darray_list = [giftiobj.darrays[0] for _ in range(arr.shape[1])]
        for i in range(arr.shape[1]):
            darray_list[i].data = arr[:, i]
            darray_list[i].intent = intent[i]
        giftiobj.darrays = darray_list

    save(giftiobj, filename.str)

