def getfilenamenii(path):
    '''
    Confirm and ext for .nii or .nii.gz file

    20180720 deprecated since we use rzpath object to deal with all path issue

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
