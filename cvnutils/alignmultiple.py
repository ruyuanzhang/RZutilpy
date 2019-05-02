def alignmultiple(niifiles, subjectid, outputprefix, mcmask='brainmask', skips=(5, 5, 5), rots=(0, 0, 0)):

    '''
    alignmultiple(niifiles, subjectid, outputprefix, mcmask,skips,rots)

    <niifiles> is a list of NIFTI filenames
    <subjectid> is like 'C0001'
    <outputprefix> is like 'T1average'
    <mcmask>: can be
        'brainmask', a str, indicates that we use a skullstripped brain mask returned by
            afni utility and then use this mask to align multiple files
        [mn, sd], a list, with the mn and sd outputs of defineellipse3d.m.

    <skips> is number of slices to skip in each of the 3 dimensions.
        Default: (5, 5, 5).
    <rots> is a 3-vector with number of CCW rotations to apply for each slicing.
        Default: (0, 0, 0).

    The purpose of this function is to align and average all of the NIFTI files
    and write out a new NIFTI file.

    We pause for the user to manually define an binary 3D ellipse on the
    first NIFTI in order to restrict the alignment procedure to those voxels.
    Consider, for example, restricting the ellipse to cortex and maybe a little bit
    of surrounding space.

    We loop over NIFTIs after the first one to align each with the first using
    a rigid-body transformation and a correlation metric. Slices are extracted
    using cubic interpolation to derive volumes that match the first.

    Our final volume is the mean of all of the volumes (first volume plus the
    resliced versions of the remaining volumes).

    We write out a NIFTI file to <anatomicals>/<outputprefix>.nii.gz using the first NIFTI as a template.

    Inspections of results are written to a directory <ppresults>/<outputprefix>figures.

    history:
    2016/09/02 - change where files are written; fix the gzipping
    2016/07/12 - switch to _untouch_
    2016/06/10 - force non-finite values in resliced volumes to be 0 (flirt fails otherwise)
    2016/05/29 - added visualization of residuals

    #========================
    below is by RZ:
    #========================
    Note:
    We differ from XXX

    To do:
    - implement the ellipse, and alignment
    - implement the brain extraction and alignment using afni or fsl

    history:
    20180714 accept the pathlib object for niftitiles
    20180620 RZ created this file based on cvnalignmultiple.m
    '''

    from RZutilpy.cvnpy import cvnpath
    from RZutilpy.system import unix_wrapper
    from RZutilpy.imageprocess import makeimagestack3dfiles
    from RZutilpy.mri import savenifti
    import nibabel as nib
    from numpy import isnan, isfinite, percentile, abs, all, stack
    from os.path import dirname, join
    from colormap import Colormap
    from pathlib import Path


    # calc
    dir0 = cvnpath('anatomicals') / subjectid
    pp0 =  cvnpath('ppresults') /  subjectid

    # match files
    if all([isinstance(p, Path) for p in niifiles]):
      niifiles = [str(p) for p in niifiles]
    niifiles = matchfiles(niifiles) # after matchfiles niifiles become pathlib objects

    # load the first volume
    vol1 = nib.load(str(niifiles[0]))
    vol1data = vol1.get_data().astype('f4') # 32 bit floating point
    vol1data[isnan(vol1data)] = 0

    # ===============================================
    # use afni to align all volumnes
    # ===============================================
    # here is different from KK' cvnalignmultiple.m, we use afni linear align utility
    # to align multiple volumes

    # let's create a brainmask using afni utility
    datadir = niifiles.parent
    brainmaskfile = datadir / 'T1alignbrainmask.nii.gz'

    # skullstrip to create the mask
    result = unix_wrapper('3dSkullStrip -input {} -prefix {} -mask_vol'.format(str(niifiles[0]), str(brainmaskfile)))
    # on stone 3DSkullStrip cannot specify the output directory... afni bug??
    # we manually move the mask file
    result = unix_wrapper('mv T1alignbrainmask.nii.gz %s/'.format(str(datadir)))

    # read the mask vol file
    brainmask = nib.load(str(brainmaskfile)).get_data()

    # inspect first volume and brainmask
    makeimagestack3dfiles(vol1data, join(str(pp0),'{}figures'.format(outputprefix), 'vol{:03d}'.format(0)), skips,rots, wantnorm=1, addborder=1)
    makeimagestack3dfiles(brainmask, join(str(pp0), '%sfigures'.format(outputprefix), 'brainmask'), skips,rots, wantnorm=1, addborder=1)
    # ===============================================


    # # manually define ellipse on the first volume for use in the auto alignment
    # if isempty(mcmask)
    #   [f,mn,sd] = defineellipse3d(vol1data)
    #   mcmask = {mn sd}
    #   fprintf('mcmask = %s\n',cell2str(mcmask))
    # else
    #   mn = mcmask{1}
    #   sd = mcmask{2}

    # loop over volumes
    outputfiles = [p[:-7] + '_aligned.nii.gz' for p in niifiles]

    vols=[]  # note that this list does not contain the 1st volume
    for p in range(1, len(niifiles)):
      # issue the cmd as list. This is the input for unix_wrapper
      cmd = ['3dAllineate',\
      '-base', niifiles[0], '-source', niifiles[p], '-prefix', outputfiles[p],\
      '-weight', brainmaskfile, '-1Dparam_save', niifiles[p][:-7],\
      '-interp', 'cubic', '-cost', 'crM', '-final', 'wsinc5']
      # do it
      unix_wrapper(cmd)

      ## start the alignment
      #alignvolumedata(vol2data,vol2size,vol1data,vol1size)  # NOTICE THAT FIRST VOLUME IS THE TARGET!

      # auto-align (rigid-body, correlation)
      #alignvolumedata_auto(mn,sd,[1 1 1 1 1 1 0 0 0 0 0 0],[4 4 4])
      #alignvolumedata_auto(mn,sd,[1 1 1 1 1 1 0 0 0 0 0 0],[2 2 2])
      #alignvolumedata_auto(mn,sd,[1 1 1 1 1 1 0 0 0 0 0 0],[1 1 1])

      # get the transformation
      #tr = alignvolumedata_exporttransformation

      # get slices from vol2 to match vol1
      #matchvol = extractslices(vol2data,vol2size,vol1data,vol1size,tr)

      # read the aligned volume
      matchvol = nib.load(outputfiles[p]).get_data()
      assert all(matchvol.shape==vol1data.shape), 'This # %d volume have a different size!' % p
      # REALLY IMPORTANT: ENSURE FINITE (e.g. flirt blows up otherwise)
      matchvol[~isfinite(matchvol)] = 0
      # inspect it
      makeimagestack3dfiles(matchvol, join(pp0, '%sfigures' % outputprefix, 'vol%03d' % p), skips, rots, wantnorm=1, addborder=1)
      # record it into the list
      vols.append(matchvol)

    # average all vols
    meanvol = sum(vols) / len(vols)
    # inspect it
    makeimagestack3dfiles(meanvol, join(pp0, '%sfigures' % outputprefix, 'volavg'), skips, rots, wantnorm=1, addborder=1)

    # finally, write out residual images
    # prepare colormap
    if len(vols) != 1:
      mx = percentile(stack([abs(vol - meanvol) for vol in vols], axis=-1), 99)
      [makeimagestack3dfiles(vol-meanvol, join(pp0, '%sfigures' % outputprefix, 'resid%03d' % p),\
        skips,rots, cmap=Colormap().cmap_linear('blue','black','red'), wantnorm=(-mx, mx), \
        addborder=1) for p, vol in enumerate(vols)]

    # save the mean vol NIFTI file as output
    savenifti(meanvol, join(dir0,'%s.nii.gz' % outputprefix), niftiobj=vol1)

