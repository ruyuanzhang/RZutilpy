def runfreesurfer2(subjectid,extraflags=''):
    '''
    def runfreesurfer2(subjectid,extraflags):

    <subjectid> is like 'C0001'
    <extraflags> (optional) is a string with extra flags to pass to recon-all.
     Default: ''

    This is part 2/2 for pushing anatomical data through FreeSurfer.
    see code for assumptions.
    '''
    from RZutilpy.cvnpy import cvnpath, writemgz, fstoint
    from RZutilpy.system import makedirs,Path
    from RZutilpy.rzio import savepkl, loadpkl
    import nibabel.freesurfer.io as fsio
    import nibabel as nib
    import re
    from numpy import stack
    from sklearn.neighbors import NearestNeighbors


    # calc
    dir0 = (Path(cvnpath('anatomicals')) / subjectid).str
    fsdir = (Path(cvnpath('freesurfer')) / subjectid).str

    # make subject anatomical directory
    makedirs(dir0)

    # convert some miscellaneous files

    # convert .thickness files to ASCII
    # no need for python since nibabel can directly read the file
    # unix_wrapper('mris_convert -c {0}/surf/lh.thickness {0}/surf/lh.white {0}/surf/lh.thickness.asc'.format(str(fsdir)))
    # unix_wrapper('mris_convert -c {0}/surf/rh.thickness {0}/surf/rh.white {0}/surf/rh.thickness.asc'.format(str(fsdir)))

    # # convert .curv files to ASCII
    # unix_wrapper('mris_convert -c {0}/surf/lh.curv {0}/surf/lh.white {0}/surf/lh.curv.asc'.format(str(fsdir)))
    # unix_wrapper('mris_convert -c {0}/surf/rh.curv {0}/surf/rh.white {0}/surf/rh.curv.asc'.format(str(fsdir)))

    #### make mid-gray surface

    unix_wrapper('mris_expand -thickness {0}/surf/lh.white 0.5 {0}/surf/lh.graymid'.format(fsdir))
    unix_wrapper('mris_expand -thickness {0}/surf/rh.white 0.5 {0}/surf/rh.graymid'.format(fsdir))

    #### consolidate mid-gray surface stuff into a .mat file
    for hemi in ['lh' 'rh']:
        # read .graymid surface
        vertices,faces = fsio.read_geometry((Path(fsdir) / 'surf'/ f'{hemi}.graymid').str)

        # construct vertices (4 x V), becareful here, numpy and matlab index might be different!!!
        vertices = vertices.T + np.array([128, 129, 128]).reshape(-1,1)
        vertices = np.vstack((vertices, np.ones(vertices.shape[1]).reshape(1,-1)))

        # construct faces (F x 3)
        faces = faces[:,[0, 2, 1]]  # necessary to convert freesurfer to matlab

        # load auxiliary info (V x 1)
        thickness = fsio.read_morph_data((Path(fsdir) / 'surf' / f'{hemi}.thickness').str)
        curvature = fsio.read_morph_data((Path(fsdir) / 'surf' / f'{hemi}.curv').str)

        # get freesurfer labels (fslabels is V x 1)
        fslabels, _, _ = fsio.read_annot((Path(fsdir) / 'label' / f'{hemi}.aparc.annot').str)

        # save
        savepkl((Path(cvnpath('anatomicals')) / subjectid / f'{hemi}midgray.pkl'.format(hemi)).str,
          {'vertices':vertices, 'faces':faces, 'thickness':thickness, \
          'curvature':curvature, 'fslabels': fslabels})

    #### calculate gray-matter information

    if isempty(regexp(extraflags,'hires')):
        # load ribbon
        ribmgz = nib.load((Path(fsdir)/ 'mri' / 'ribbon.mgz').str)
        rib = fstoint(ribmgz.get_data())

        # load coordinates of surface vertices
        coord0 = stack(\
          (loadpkl(Path((cvnpath('anatomicals')) / subjectid / 'lhmidgray.mat').str)['vertices'],\
            loadpkl((Path(cvnpath('anatomicals')) / subjectid / 'rhmidgray.mat').str)['vertices']),\
          axis=1)

        #### use nearestNeighour, need to double check this
        nbrs = NearestNeighbors(1, metric='l2')
        nbrs.fit(coord0.T)
        dist, mnix = nbrs.kneighbors(rib, 1) # do I need to reshape dist and mnix?


        # compute distances to vertices [i.e. create a volume where gray matter voxels have certain informative values]
        #[dist,mnix] = surfaceslice2(ismember(rib,[3 42]),coord0, 3, 4)  # NOTICE HARD-CODED VALUES HERE
        ####

        # save
          # 1-mm volume with, for each gray matter voxel, distance to closest vertex (of mid-gray surface)
        nib.save(inttofs(dist), (Path(fsdir) / 'mri'/ 'ribbonsurfdist.mgz').str, ribmgz)
          # 1-mm volume with, for each gray matter voxel, index of closest vertex (of mid-gray surface)
        nib.save(inttofs(mnix),(Path(fsdir) / 'mri'/ 'ribbonsurfindex.mgz').str, ribmgz)


    #### calculate transfer functions

    # calc
    [tfunFSSSlh,tfunFSSSrh,tfunSSFSlh,tfunSSFSrh] = \
      calctransferfunctions((Path(cvnpath('freesurfer')).joinpath('fsaverage', 'surf','lh.sphere.reg')).str, \
                            (Path(cvnpath('freesurfer')).joinpath('fsaverage', 'surf','rh.sphere.reg')).str, \
                               (Path(cvnpath('freesurfer')).joinpath(subjectid, 'surf','lh.sphere.reg')).str, \
                               (Path(cvnpath('freesurfer')).joinpath(subjectid, 'surf','rh.sphere.reg')).str)

    # save
    savepkl((Path(cvnpath('anatomicals')) / subjectid /'tfun.mat').str,\
      {'tfunFSSSlh': tfunFSSSlh,\
      'tfunFSSSrh': tfunFSSSrh,\
      'tfunSSFSlh': tfunSSFSlh\
      'tfunSSFSrh': tfunSSFSrh})

    # write out some useful mgz files (inherited from cvnmakelayers.m)

    # do it
    for hemi in ['lh', 'rh']:
        # load
        a1 = loadpkl((Path(dir0) / f'{hemi}midgray.mat').str)

        a3 = fsio.read_geometry((Path(fsdir) / 'surf' / f'{hemi}.sulc').str)

        # write mgz
        writemgz(subjectid,'thickness',a1.thickness, hemi)
        writemgz(subjectid,'curvature',a1.curvature, hemi)
        writemgz(subjectid,'sulc', a3, hemi)

