def getfilenamenii(path):
    '''
    Confirm and ext for .nii or .nii.gz file
    '''
    from os.path import splitext
    filename, ext = splitext(path)
    if ext == '.gz':
        filename, ext2 = splitext(filename)
        return filename, ext2 + ext
    elif ext == '.nii':
        return filename, ext
    else:
        print('Input is not a nifti file!')
        return (), ()
