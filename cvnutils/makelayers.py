def makelayers(subjectid,layerdepths,layerprefix,fstruncate='pt'):
    '''
    def makelayers(subjectid,layerdepths,layerprefix,fstruncate)

    <subjectid> is like 'C0041'
    <layerdepths> is a vector of fractional distances (each having at
      most two decimal places).  e.g. linspace(.1,.9,6).
      NOTE: layerdepth=0 is pial and layerdepth=1 is white!
    <layerprefix> is a string that will be added to filenames (e.g. 'A').
      this causes files like 'lh.layerA1' to be made.
    <fstruncate> is the name of the truncation surface in fsaverage (default. 'pt',
      which refers to 'lh.pt' and 'rh.pt')

    Create layer surfaces.
    Subdivide layer and other surfaces to form dense surfaces.
    Calculate transfer functions to go from/to fsaverage standard surfaces
     and the single-subject dense surfaces.
    Truncate the dense surfaces based on the fsaverage <fstruncate> surface,
     and write out new surfaces.
    Calculate thickness, curvature, and sulc values for the single-subject dense surfaces.
    Calculate SAPV and AEL for each surface (dense trunc only).

    Turn on matlabpool before calling for a big speed-up.

    Example files that are created:
    lh.layerA1
    lh.layerA1DENSE
    lh.layerA1DENSETRUNCpt
    tfunDENSE.pkl
    lh.DENSETRUNCpt.pkl
    lh.curvatureDENSE.mgz
    lh.curvatureDENSETRUNCpt.mgz
    lh.sapv_sphere_DENSETRUNCpt.mgz

    history:
    - 2017/08/02 - added support for smoothwm
    - 2016/11/04 - added transfer functions for the fsaverage dense surfaces
    - 2016/04/29 - add saving of sulc, sapv, and ael start using unix_wrapper


    #######======== by RZ ===============================================
    history:
      20180717 RZ started to use pathos.multiprocessing to perform parallel computing
      20180714 RZ edited based on cvnmakelayers.m
    '''
    from RZutilpy.cvnpy import cvnpath,transfertodense
    from RZutilpy.math import mod2
    from RZutilpy.rzio import savepkl,loadpkl
    from math import floor
    import nibabel.freesurfer.io as fsio
    import numpy as np
    from pathos.multiprocessing import Pool

    # calc
    dir0 = (Path(cvnpath('anatomicals')) / subjectid).str
    fsdir =  (Path(cvnpath('freesurfer')) / subjectid).str
    fsdirAVG = (Path(cvnpath('freesurfer')) / 'fsaverage').str

    # define
    hemis = ['lh', 'rh']

    ########## create layer surfaces
    def expand(ii):
        p = mod2(ii,len(layerdepths)) # depth indx
        q = floor(ii / len(layerdepths)) # hemi index
        #use 1-depth so that depth 0 = pial and depth 1 = white
        # This way if you use linspace(.1,.9,6), A1 will be equivalent to canonical
        # layer I (molecular layer) and layer A6 will be equivalent to canonical
        # layer VI (innermost...)
        d = 1 - layerdepths[p - 1]
        unix_wrapper('mris_expand -thickness {wm} {depth:.2f} {outputsurf}'.format(\
          wm=(Path(fsdir)/'surf'/f'{hemis[q]}.white').str, \
          depth=d,\
          outputsurf=(Path(fsdir)/'surf'/f'{hemis[q]}.layer{layerprefix}{p}').str))
    if __name__ == '__main__':
        with Pool() as p:
            p.imap_unordered(expand, range(1, 2*len(layerdepths) + 1))


    ######## subdivide layer and other surfaces (creating dense surfaces)

    # calc a list of surfaces
    surfs = ['inflated', 'sphere', 'sphere.reg', 'white', 'pial', 'smoothwm']
    for p in range(1, len(layerdepths)+1):
        surfs.append(f'layer{layerprefix}{p}') # e.g. 'layerA1'


    # subdivide the surfaces
    def subdivide(ii):
        p = mod2(ii,len(surfs)) # surf index
        q = floor(ii/len(surfs)) # hemi index
        unix_wrapper('mris_mesh_subdivide --surf {inputsurf} --out {outputsurf} --method linear --iter 1'.format(\
          inputsurf=(Path(fsdir)/hemis[q]/surfs{p}).str,\
          outputsurf=(Path(fsdir)/hemis[q]/(surfs{p}+'DENSE')).str))
    if __name__ == '__main__':
        with Pool() as p:
            p.imap_unordered(subdivide, range(1, 2*len(surfs) + 1))

    ########## calculate some transfer functions for the dense surfaces [VERSION 1 (to standard fsaverage)]

    # calculate transfer functions
    [tfunFSSSlh,tfunFSSSrh,tfunSSFSlh,tfunSSFSrh] = \
      calctransferfunctions((Path(fsdirAVG)/'surf'/'lh.sphere.reg').str, \
                            (Path(fsdirAVG)/'surf'/'rh.sphere.reg').str, \
                            (Path(fsdir)/'surf'/'lh.sphere.regDENSE').str, \
                            (Path(fsdir)/'surf'/'rh.sphere.regDENSE').str)

    # save
    savepkl((Path(dir0) / 'tfunDENSE.pkl').str,\
      {'tfunFSSSlh':tfunFSSSlh,'tfunFSSSrh':tfunFSSSrh,\
      'tfunSSFSlh':tfunSSFSlh,'tfunSSFSrh':tfunSSFSrh})

    ######## calculate some transfer functions for the dense surfaces [VERSION 2 (to dense fsaverage)]
    # calc
    [tfunFSSSlh,tfunFSSSrh,tfunSSFSlh,tfunSSFSrh] = \
      calctransferfunctions((Path(fsdirAVG)/'surf'/'lh.sphere.regDENSE').str, \
                            (Path(fsdirAVG)/'surf'/'rh.sphere.regDENSE').str, \
                            (Path(fsdir)/'surf'/'lh.sphere.regDENSE').str, \
                            (Path(fsdir)/'surf'/'rh.sphere.regDENSE').str)

    # save
    savepkl((Path(dir0)/'tfunDENSEDENSE.pkl').str,\
      {'tfunFSSSlh':tfunFSSSlh,'tfunFSSSrh':tfunFSSSrh,\
      'tfunSSFSlh':tfunSSFSlh,'tfunSSFSrh':tfunSSFSrh})

    ########## revive the first version!!
    transfunc = loadpkl((Path(dir0)/'tfunDENSE.pkl').str)

    ########## truncate the dense surfaces based on the lh.<fstruncate> and rh.<fstruncate> fsaverage surfaces

    # calc number of vertices
    fsnumlh = fsio.read_geometry((Path(fsdirAVG)/'surf/'/'lh.white').str)[0].shape[0]
    fsnumrh = fsio.read_geometry((Path(fsdirAVG)/'surf/'/'rh.white').str)[0].shape[0]

    # do it
    for hemi in hemis:

        # calculate a vector of vertex values indicating which is included [fsaverage]

        ##！！！ check here, should figure out read_patch_asc##
        surf = read_patch_asc((Path(fsdirAVG) / 'surf'/ f'{hemi}.{fstruncate}.patch.3d.asc').str)
        ##！！！ ##

        vals = np.zeros(fsnumlh + fsnumrh)

        ## !!! ##
        if hemi == 'lh':
          vals[surf.vertices+1] = 1
        elif hemi == 'rh':
          vals[fsnumlh+(surf.vertices+1)] = 1
        ## !!! ##

        # transfer these values to the dense individual-subject surface and do a find.
        # this tells us indices of vertices in the dense surface that are valid
        validix = np.where(transfunc['tfunFSSSlh'][vals]) if hemi == 'lh' \
        else np.where(transfunc['tfunFSSSrh'][vals])

        # write out reduced surfaces
        for sf in surfs:

            # read in the original dense surface
            [verticesA,facesA,volinfo] = fsio.read_geometry((Path(fsdir)/'surf'/f'{hemi}.{sf}DENSE').str, read_metadata=True)

            # logical indicating which faces survive
            okfaces = np.all(np.isin(facesA,validix), axis=1)  # FACES x 1

            # calculate the new faces
            temp = facesA[okfaces,:]

            ##!!!##
            facesA = calcposition(validix, temp.flatten()).reshape(*temp.shape).copy()
            ##!!!##

            # calculate the new vertices
            verticesA = verticesA[validix,:]

            # write out the truncated surface
            fsio.write_geometry((Path(fsdir) / 'surf'/ f'{hemi}.{sf}DENSETRUNC{fstruncate}').str, verticesA, facesA, volinfo)


      # save the DENSE->DENSETRUNC indices (truncsize x 1)
      savepkl((Path(fsdir)/'surf'/f'{hemi}.DENSETRUNC{fstruncate}.pkl').str, {'validix':validix})


      # save the orig->DENSE indices (densesize x 1)
      numverts_orig = fsio.read_geometry((Path(fsdir)/'surf'/f'{hemi}.inflated').str)[0].shape[0]

      # note the 0 inde problem here, here might not be correct
      validix = transfertodense(subjectid, np.arange(numverts_orig), hemi,'nearest','inflated')
      savepkl((fsdi/'surf'/f'{hemi}.DENSE.pkl').str,{'validix':validix})


    ######### transfer thickness, curvature, and sulc values from standard to dense

    for hemi in hemis:

        # load
        a1 = loadpkl((Path(dir0)/f'{hemi}midgray.pkl').str)
        a2 = loadpkl((Path(fsdir)/'surf'/f'{hemi}.DENSETRUNC{fstruncate}.pkl').str)
        # read sulc data
        a3 = fsio.read_morph_data((Path(fsdir)/'surf'/f'{hemi}.sulc').str)

        # transfer values
        thickness = transfertodense(subjectid, a1['thickness'], hemi,'nearest')
        curvature = transfertodense(subjectid, a1['curvature'],hemi,'nearest')
        sulc      = transfertodense(subjectid, a3,          hemi,'nearest')
      #  save(sprintf('%s/%smidgrayDENSE.pkl',dir0,hemi),'thickness','curvature')

        # write mgz
        writemgz(subjectid,'thicknessDENSE',thickness, hemi)
        writemgz(subjectid,'curvatureDENSE',curvature, hemi)
        writemgz(subjectid,'sulcDENSE',     sulc,      hemi)

        # write mgz for truncated
        writemgz(subjectid,f'thicknessDENSETRUNC{fstruncate}',thickness[a2['validix']],hemi)
        writemgz(subjectid,f'curvatureDENSETRUNC{fstruncate}',curvature[a2['validix']],hemi)
        writemgz(subjectid,f'sulcDENSETRUNC{fstruncate}',     sulc[a2['validix']],     hemi)

        # write curv
        _,facesA = fsio.read_geometry((Path(fsdir)/'surf'/f'{hemi}.inflatedDENSE').str)
        fsio.write_morph_data((Path(fsdir)/'surf'/f'{hemi}DENSE.curv').str,curvature,facesA.shape[0])

        # write curv for truncated
        _,facesA = fsio.read_geometry((Path(fsdir)/'surf'/f'{hemi}.inflatedDENSETRUNC{fstruncate}').str)
        fsio.write_morph_data((Path(fsdir)/'surf'/f'{hemi}DENSETRUNC{fstruncate}.curv').str, curvature[a2['validix']], facesA.shape[0])


    ######## compute and save some useful quantities for dense trunc surfaces

    # for each hemisphere
    for hemi in hemis:

        # for each of the surfaces
        for sf in surfs:

            # read in the surface
            verticesA,facesA = fsio.read_geometry((Path(fsdir)/'surf'/f'{hemi}.{sf}DENSETRUNC{fstruncate}'.str))

            ## !! ## change here
            # compute and save SAPV
            sapv = vertex_area(verticesA,facesA)  # column vector
            writemgz(subjectid,f'sapv_{sf}_DENSETRUNC{fstruncate}',sapv,hemi)

            # compute and save AEL
            ael = vertex_neighbor_distance(verticesA,facesA,'mean')  # column vector
            writemgz(subjectid,f'ael_{sf}_DENSETRUNC{fstruncate}',ael,hemi)
            ## !! ## change here


  #################################### SOME CHECKS

  # cd /software/freesurfer/subjects/C0041/
  # freeview -f surf/lh.layerA1:overlay=surf/lh.curv:edgethickness=0
  # freeview -f surf/lh.layerA1DENSE:overlay=surf/lh.curvatureDENSE.mgz:edgethickness=0
  # freeview -f surf/lh.inflated:overlay=surf/lh.curv:edgethickness=0
  # freeview -f surf/lh.inflatedDENSE:overlay=surf/lh.curvatureDENSE.mgz:edgethickness=0
  # freeview -f surf/lh.inflatedDENSETRUNCpt:overlay=surf/lh.curvatureDENSETRUNCpt.mgz:edgethickness=0
