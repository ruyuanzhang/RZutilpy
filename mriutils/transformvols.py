def transformvols(vols, xfm, postfix='_aff'):
    '''
    transform volumes with resampling. In this case, we only change the affine
    in head info. Note that, this function must meet two preassumption
    (1). The volumes must be align to canonical coordinates
    (2). The xfm must be defined in RAS+ space.

    We forced to save transformed volumes to new files

    Input:
        <vols>: a string or a list of string
        <xfm>: can be array
            (1) a 4x4 array
            (2) a string, can read the transform using np.loadtxt
        <postfix>: postfix to save the transformed volume, default:'aff'
    '''
    from numpy import ndarray,loadtxt
    from RZutilpy.system import Path, unix_wrapper
    from RZutilpy.mri import splitniftiname
    from nibabel import load


    if not isinstance(vols,list):
        vols = [vols]
    if isinstance(xfm, ndarray):
        pass
    elif isinstance(xfm, str):
        xfm = loadtxt(xfm)

    # judge whether nifti or +orig file
    if vols[0][-10:-5] in ['+orig', '+tlrc']:
        isafni = True
    elif splitniftiname(vols[0])[1] in ['.nii', '.nii.gz']:
        isafni = False
    else:
        raise ValueError('Input volumes should be either NIFTI or AFNI format')

    for vol in vols:
        if isafni:
            vol_tmp = vol[:-10]
            unix_wrapper(f'3dcopy {vol} {vol_tmp}.nii.gz') # convert to nifti
            vol = f'{vol_tmp}.nii.gz'
        # transform volume
        tmp = load(vol) # here vol must be a nifti file
        affine_tmp = tmp.affine.copy()
        tmp.set_qform(xfm.dot(affine_tmp))
        tmp.set_sform(xfm.dot(affine_tmp))
        tmp.to_filename(f'{splitniftiname(vol)[0]+postfix}.nii.gz') # save to nifti

        if isafni: # further convert nifti to AFNI format
            unix_wrapper(f'3dcopy {Path(vol).strnosuffix+postfix}.nii.gz {Path(vol).strnosuffix+postfix}')
            unix_wrapper(f'rm {vol} {Path(vol).strnosuffix+postfix}.nii.gz') # remove intermediate nifti file
