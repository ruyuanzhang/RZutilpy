def t1warp(t1, outputDir=None, template=None, maskvol=None, skullstrip_kw=[], affine_kw=[], affonly=False):
    '''
    Nonlinear (or linear warping) warping t1 file to a template. In afni_proc, they use
    @SSwarper by default. For a standard human T1 file, @SSwarper produce similar warping files
    as this script. But this script might be useful for like unusual cases, for example, Monkey data

    Input:
        <t1>: t1 file, a string or a pathlib object
        <outputDir>: output directory, we first copy t1 file into this outputDir. if None,
            use cwd.
        <template>: the template t1 file,a string or a pathlib object. if None, we use
            afni MNI152_2009_template_SSW.nii.gz file
        <maskvol>: mask volume, a str or a pathlib object. You can supply an maskvol file
            here so the skullstrip step will be skipped. This is useful when you want to
            manually edit the mask volume and supply it to skullstrip
        <skullstrip_kw>, <affine_kw>: lists, extra options supply to '3dSkullstrip' and 'align_epi_anat.py'
            commands. This is useful for like monkey data. Default: [] (empty list)
        <affonly>: boolean (default: False), only need affine transform, no nonlinear warping.

    Output: this will produce several files in <outputDir>, they are generated in order
        **.nii.gz: copy of t1 file
        **_ss.nii.gz: skullstriped(ss) T1
        **_ssmask.nii.gz: skullstriped(ss) brain mask
        **_ssiu.nii.gz: intenstivity unifize(iu) t1 after ss
        **_ssiu_shft: shift to center of mass of the template after iu
        **_ssiu_shft_aff: affine tranformed T1 in the template space
        **_ssiu_shft_aff_mat.aff12.1D: affine transformation matrix
        **_ssui_shft_aff_matINV.aff12.1D: inverse affine transformation
        **_ssiu_shft_aff_nl.nii.gz: nonlinear warp to the template in the template space
        WARP.nii.gz: nonlinear warp file

    Note:
        1. Here we do three transform, shift-affine-nlwarp. The later two can be concatenated but
            it is not recommended to concatenate all three because combining shift into affine and nlwarp
            will make the "3dNwarpapply" take a lot of memory and very long time (and might fail).
            If you want to inversely warp an atlas from template space into native T1 space. You can do like

            # first do inverse (affine+nlwarp)
            cmd = ['3dNwarpApply', '-prefix', f'{template.strnosuffix}_nl2t1.nii.gz', \
               '-nwarp', f'inv({(outputDir/"WARP.nii.gz").str} {t1.strnosuffix}_ssiu_shft_aff2NMT_mat.aff12.1D)', \
               '-source', template.str, '-master', f'{t1.strnosuffix}_ssiu_shft.nii.gz', '-overwrite']
            unix_wrapper(cmd)
            # then inverse the shift
            # Note that here do not use 3dAllineate as it will resample the data one more time
            # Use 3drefit, it will not resample data
            cmd = f'3drefit -duporigin {t1.strnosuffix}_ssiu.nii.gz {template.strnosuffix}_nl2t1.nii.gz}'
            unix_wrapper(cmd)

        2. Be very CAREFUL about the order when concatenating affine and nlwarp!

    To do:
        1. automatically perform inversed warp atlas??

    History:
        20190413 RZ create
    '''

    from RZutilpy.system import Path, unix_wrapper, makedirs

    t1 = Path(t1)
    if template:
        template = Path(template) if ~isinstance(template, Path) else template
    else: # default template is mni template
        afnipath = unix_wrapper(f'which afni') # get the afni install Path
        template = Path(afnipath).parent / 'MNI152_2009_template_SSW.nii.gz'

    outputDir = Path.cwd() if outputDir is None else Path(outputDir)
    makedirs(outputDir) # create outputdir if not exist
    unix_wrapper(f'cp {t1} {outputDir}') # copy t1 file to outputdir
    t1 = outputDir / f'{t1.name}' # switch to new t1

    # ======= step 1, skull strip =====================
    if maskvol is None:
        # make brain mask, this step typically is good for a human brain, but tricky for a monkey brain
        cmd = ['3dSkullStrip', \
            '-input', t1.str, \
            '-prefix', f'{t1.strnosuffix}_ssmask.nii.gz', \
            '-mask_vol']
        cmd = cmd + skullstrip_kw
        unix_wrapper(cmd)
        maskvol = Path(f'{t1.strnosuffix}_ssmask.nii.gz')
    # skullstrip-based on mask
    cmd=['3dcalc', '-a', t1.str, '-b', maskvol.str, \
        '-expr', "a*step(b)", \
        '-prefix', f'{t1.strnosuffix}_ss.nii.gz']
    unix_wrapper(cmd)

    # ===== step 2, # intensity unifize ===========
    cmd = f'3dUnifize -prefix {t1.strnosuffix}_ssiu.nii.gz {t1.strnosuffix}_ss.nii.gz'
    unix_wrapper(cmd)

    # ====== step 3, affine transform to NMT template ==================

    # first we can align center of mass
    cmd=f'@Align_Centers -base {template.str} -dset {t1.strnosuffix}_ssiu.nii.gz -cm'
    unix_wrapper(cmd) # this step will generate {t1.strnosuffix}_ssiu_shft.nii.gz
    shftfile = Path.cwd() / f'{t1.pstem}_ssiu_shft.1D'
    unix_wrapper(f'mv {shftfile.str} {outputDir.str}')
    # This step will generate {t1.strnosuffix}_ssiu_shft.nii.gz
    # This step will also generate a 1D transformation file under CWD not OUTPUTDIR
    # we have to copy this 1D file into <outputDir>

    # do affine alignment, note that data will be resampled on NMT grid
    cmd = ['align_epi_anat.py', '-dset1', f'{t1.strnosuffix}_ssiu_shft.nii.gz', \
                  '-dset2', template.str, \
                  '-master_dset1', template.str,\
                  '-suffix', '_aff.nii.gz',\
                  '-dset1to2', '-dset1_strip','None','-dset2_strip','None','-overwrite',\
                  '-output_dir', outputDir.str]
    cmd = cmd + affine_kw
    unix_wrapper(cmd)

    # change transformation file name
    unix_wrapper(f'mv {t1.strnosuffix}_ssiu_shft_aff.nii.gz_mat.aff12.1D {t1.strnosuffix}_ssiu_shft_aff_mat.aff12.1D')

    # calc the inverse affine transformation
    cmd = f'cat_matvec -ONELINE {t1.strnosuffix}_ssiu_shft_aff_mat.aff12.1D -I > {t1.strnosuffix}_ssiu_shft_aff_matINV.aff12.1D'
    unix_wrapper(cmd)

    # ================= step 4, nonlinear registration ==============
    # note that this step should be run after completing affine transformation
    # Also here, input dataset is the anat dataset but put on the base grid,
    unix_wrapper(f'rm -rf {(outputDir/"awpy*").str}')
    # use superhard, to get the best alignment, but it take a long time
    cmd = ['auto_warp.py', '-base', template.str, '-skip_affine', 'yes', \
      '-input', f'{t1.strnosuffix}_ssiu_shft_aff.nii.gz', '-overwrite', \
      '-output_dir', (outputDir/'awpy').str, '-qw_opts','-iwarp','-superhard']
    unix_wrapper(cmd)
    # copy and delete redundant files
    unix_wrapper(f'cp {(outputDir/"awpy"/"anat.un.qw_WARP.nii").str} {(outputDir/"WARP.nii").str}')
    unix_wrapper(f'gzip -f {(outputDir/"WARP.nii").str}') # compress nonlinear warp file
    unix_wrapper(f'rm -rf {(outputDir/"awpy")}')

    # apply transform warp t1 to the template space
    cmd = ['3dNwarpApply', '-prefix', f'{t1.strnosuffix}_ssiu_shft_aff_nl.nii.gz', \
       '-nwarp', f'{(outputDir/"WARP.nii.gz").str} {t1.strnosuffix}_ssiu_shft_aff_mat.aff12.1D', \
       '-source', f'{t1.strnosuffix}_ssiu_shft.nii.gz', '-master', template.str, '-overwrite']
    unix_wrapper(cmd)
