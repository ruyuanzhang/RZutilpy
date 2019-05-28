def splitniftiname(file):
    '''
    get nift file names. Assume nifti files is
    xxx.nii.gz or xxx.nii, we want to extract xxx
    <file> is a string of nifti file.

    We return ('xxx', '.nii') or ('xxx', '.nii.gz')
    '''
    from RZutilpy.system import Path

    suffix = Path(file).suffixes
    if suffix[-1] == '.gz':  #.nii.gz format
        return file[:-7], '.nii.gz'
    elif suffix[-1] == '.nii':
        return file[:-4], '.nii'
    else:
        return None
