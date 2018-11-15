def cvnrunfreesurfer(subjectid, dataloc, extraflags='', scanstouse=None,t2nifti=None):
    '''
    function cvnrunfreesurfer(subjectid,dataloc,extraflags,scanstouse,t2nifti)

    <subjectid> is like 'C0001'
    <dataloc> is:
        (1) the scan directory like '/home/stone-ext1/fmridata/20151014-ST001-wynn,subject1'
        (2) a NIFTI T1 .nii.gz file like '/home/stone-ext1/fmridata/AurelieData/Austin_3D.nii.gz'
        (3) or a pathlib object of (1) or (2)
    <extraflags> (optional) is a string with extra flags to pass to recon-all.
        Default: ''
    <scanstouse> (optional) is a vector of indices of T1 scans to use.
        For example, if there are 5 scans, [1 3 5] means to use the 1st, 3rd, and 5th.
        Default is to use all available.
    <t2nifti> (optional) is a NIFTI T2 .nii.gz file (str or path obj). If you specify this case,
      <dataloc> must be case (2).

    push anatomical data through FreeSurfer.
    see code for assumptions.

    history:
    - 2016/11/28 - major update for the new scheme with manual FS edits.
    '''
    from RZutilpy.cvnpy import cvnpath
    from RZutilpy.system import makedirs, unix_wrapper, Path
    from RZutilpy.rzio import matchfiles


    # calc
    dir0 = (Path(cvnpath('anatomicals')) / subjectid).str
    fsdir = (Path(cvnpath('freesurfer')) / subjectid).str

    # make subject anatomical directory
    makedirs(dir0)

    # case 1
    if Path(dataloc).is_dir():

      # figure out T1 files [ASSUME THAT THERE ARE AN EVEN NUMBER OF DIRECTORIES]
      t1file = matchfiles((Path(dataloc) / 'dicom' / '*T1w*').str)
      assert len(t1file) % 2==0
      t1file = t1file[1::2]   # [hint: 2nd of each pair is the one that is homogenity-corrected]

            #           # figure out T2 file [ASSUME THAT WE WILL MATCH TWO DIRECTORIES]
            #           t2file = matchfiles(sprintf('%s/*T2w*',dataloc))
            #           assert(mod(length(t2file),2)==0)
            #           t2file = t2file(2:2:end)   # [hint: 2nd of the two is the one to use, as it is homogenity-corrected]

      # convert dicoms to NIFTIs
      for p in t1file:
        unix_wrapper('dcm2nii -o {} -r N -x N {}'.format(dir0, p))

            #   assert(0==unix(sprintf('dcm2nii -o %s -r N -x N %s',dir0,t2file)))

      # find the NIFTIs
      t1nifti = matchfiles('{}/dicom/*T1w*nii.gz'.format(dir0))
            #   t2nifti = matchfiles(sprintf('%s/*T2w*nii.gz',dir0))
            #assert(length(t1nifti)==1)
            #   assert(length(t2nifti)==1)
            #t1nifti = t1nifti{1}
            #   t2nifti = t2nifti{1}
      assert t2nifti is None

    # case 2, dataloc is a nifti file
    else:
      assert Path(dataloc).is_file() and Path(dataloc).exists()

      # find the NIFTI
      t1nifti = matchfiles(dataloc)
          #assert(length(t1nifti)==1)
          #t1nifti = t1nifti{1}
      if not t2nifti:
        t2nifti = matchfiles(t2nifti)
        assert len(t2nifti)==1
        t2nifti = t2nifti[0]


    # deal with scanstouse
    if not scanstouse:
      scanstouse = range(len(t1nifti))

    # call recon-all
    str0 = ['-i %s '.format(str(x)) for x in t1nifti[scanstouse]]

    if not t2nifti:
      extrat2stuff = ''
    else:
      extrat2stuff = '-T2 %s -T2pial'.format(t2nifti)

    unix_wrapper('recon-all -s {} {} {} -all {} > {}/reconlog.txt'.format(subjectid,str0,extrat2stuff,extraflags,str(dir0)))

    # convert T1 to NIFTI for external use
    unix_wrapper('mri_convert {}/mri/T1.mgz {}/mri/T1.nii.gz'.format(str(fsdir),str(fsdir)))
