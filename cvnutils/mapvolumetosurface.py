def mapvolumetosurface(subjectid, numlayers, layerprefix, fstruncate,\
  volfiles, names, datafun=@(x) x,specialmm=None, interptype='cubic',alignfile=None, outputdir=None):
    '''
    function mapvolumetosurface(subjectid,numlayers,layerprefix,fstruncate, ...
     volfiles,names,datafun,specialmm,interptype,alignfile,outputdir)

    <subjectid> is like 'C0051'
    <numlayers> is like 6
    <layerprefix> is like 'A'
    <fstruncate' is like 'pt'
    <volfiles> is a wildcard or cell vector matching one or more NIFTI files. can also be raw matrices.
    <names> is a string (or cell vector of strings) to be used as prefixes in output filenames.
        There should be a 1-to-1 correspondence between <volfiles> and <names>.
    <datafun> (optional) is a function (or cell vector of functions) to apply to the data
        right after loading them in. If you pass only one function, we apply that function
        to each volume.
    <specialmm> (optional) is
         0 means do the usual thing
         N means interpret the matrices in <volfiles> as having a voxel size of N mm.
           can be a vector of different mm numbers. when the N (or vector) case is used,
           <volfiles> should be a matrix or cell vector of matrices.
         Default: 0.
    <interptype> (optional) is 'nearest' | 'linear' | 'cubic'.  default: 'cubic'.
    <alignfile> (optional) is an alignment.mat file that indicates the positioning
         of the volume. if this case is used, <specialmm> should be a single scalar N
         and should be consistent with the 'tr' variable in <alignfile>.
         Default is to do the usual thing.
    <outputdir> (optional) is the directory to write the .mgz files to.
     Default is cvnpath('freesurfer')/<subjectid>/surf/

    Use interpolation to transfer the volume data in <volfiles> onto the layer
    surfaces (e.g. layerA1-A6) as well as the white and pial surfaces.
    Save the results as .mgz files.

    There are three cases:
    (1) The usual case is that the volumes in <volfiles> are assumed to
       be in our standard FreeSurfer 320 x 320 x 320 0.8-mm space.
    (2) A different case is when the <specialmm> mechanism is used in this
       case, the user sets the voxel size and matrix size and we create
       volumes that share the same center location as the standard FreeSurfer space.
    (3) A third case is when the <specialmm> mechanism is used in conjunction
       with <alignfile>. This allows the volumes to be placed in arbitrary locations.

    history:
    - 2016/11/30 - add <alignfile> and <outputdir> inputs
    - 2016/11/29 - add <specialmm> and <interptype> inputs

    ##### RZ notes ###############
    <volfiles> can accept
        (1). a wildcard string
        (2). a list of filenames
        (3). a list of path-like objects
        we internally convert to (1),(3) to (2)
    <interptype> doesn't matter, since map_coordinates only use spline interpolation
    <outputdir> now

    history:
      20180717 RZ
      20180714 RZ edit it based on cvnmapvolumetosurface.m
    '''
    from RZutilpy.cvnpy import cvnpath,writemgz
    from RZutilpy.rzio import loadpkl, matchfiles
    from RZutilpy.mri import loadniftimulti
    from RZutilpy.system import rzpath
    import nibabel.freesurfer.io as fsio
    import nibabel as nib
    import numpy as np
    from scipy.ndimage import map_coordinates

    # internal constants [NOTE!!!]
    fsres = 256
    newres = 320

    # figure out datafile
    # convert it to list
    if isinstance(volfiles, str):  # wildcard
        volfiles = matchfiles(volfiles)
    if isinstance(volfiles, str):  # still str, only one volume matched
        volfiles = [volfiles]
    # if path-like objects, we convert to string, easier to load multiple nifti
    volfiles = [x.str if isinstance(x,rzpath) else x for x in volfiles]

    # calc
    fsdir = cvnpath('freesurfer')/subjectid
    hemis = ['lh', 'rh']

    # load
    a1 = loadpkl(alignfile) if alignfile else None

    # figure out surface names
    surfs = []
    surfsB = []
    for p in range(1, numlayers + 1):
        surfs.append(f'layer{layerprefix}{p}DENSETRUNC{fstruncate}')  # six layers, dense, truncated
        surfsB.append(f'layer{layerprefix}{p}_DENSETRUNC{fstruncate}')  # six layers, dense, truncated

    surfs.append(f'whiteDENSETRUNC{fstruncate}')  # white
    surfsB.append(f'white_DENSETRUNC{fstruncate}')  # white
    surfs.append(f'pialDENSETRUNC{fstruncate}')   # pial
    surfsB.append(f'pial_DENSETRUNC{fstruncate}')   # pial

    # load surfaces
    vertices = [[],[]]
    for p,hemi in enumerate(hemis):
        for q, sf in enumerate(surfs):
            vertices[p].append(fsio.read_geometry((fsdir/'surf'/f'{hemi}.{sf}').str)[0]) # get the vertices
            vertices[p][q] = vertices[p][q].T + np.array([128, 129, 128]).reshape(-1,1)  # NOTICE THIS!!!
            vertices[p][q] = np.vstack((vertices[p][q], np.ones(vertices[p][q].shape[1])))

    ## !! ## note here, read in multiple nifti
    # load volumes
    if specialmm is None:
        ## !! ## note here, read in multiple nifti
        data,_ = loadniftimulti(volfiles.str)  # load the data
        data = np.stack(data,axis=-1) # stack all volumes to the 4th dimension
        ## !! ##
        assert all(data.shape[:3]==(newres, newres, newres)) # sanity check
        nd = 1 if data.ndim<=3 else data.shape[3]
    else:
        data = volfiles
        data = [data] if ~isinstance(data, list) else data
        specialmm = np.tile(specialmm,(len(data))) if len(specialmm)==1 else specialmm
        nd = len(data)
    ## !! ## note here, read in multiple nifti

    # sanity check
    assert nd==len(names)

    # expand datafun
    datafun = [datafun] if ~isinstance(datafun, list) else datafun
    datafun = datafun * nd if len(datafun)==1 else datafun

    # interpolate volume onto surface and save .mgz file:
    for p in range(nd):
        # this is the usual standard case
        if specialmm is None:
            tempdata = datafun[p](data[:,:,:,p])
            for q, hemi in enumerate(hemis):
                for r, sf in enumerate(surfs):
                    coord = (vertices[q][r][0:3,:] - .5)/fsres * newres + .5  # DEAL WITH DIFFERENT RESOLUTION

                    ##!!!## make sure the replacement of ba_interp3_wrapper
                    temp = map_coordinates(tempdata,coord) # temp is the value
                    ##!!!##

                    writemgz(subjectid,f'{names[p]}_{surfsB[r]}', temp, hemi, outputdir)

      # this is the case where the user sets the voxel size
        else:
            tempdata = datafun[p](data[p])
            for q, hemi in enumerate(hemis):
                for r, sf in enumerate(surfs):
                    # in this case, the user specifies the alignment
                    if alignfile is not None:

                        ##!!!## double check here, can compare the matlab result
                        # note that this tr matrix is from EPI voxelspace to T1 fsspace
                        # transformation, thus we take the inverse
                        mat, vec = nib.affines.to_matvec(tempdata, a1['T'])
                        coord = np..linalg.inv(mat)@coord + vec
                        ##!!!## double check here

                    # in this case, we assume the center of the slab is matched
                    else:
                        coord = (vertices[q][r][0:3,:] - (1+fsres)/2) * (1/specialmm[p]) + ((1+np.array(data[p].shape))/2).flatten().T

                    # do the interpolation
                    ##!!!## make sure the replacement of ba_interp3_wrapper
                    # note that this coord is a 3 x nVert coord, output temp is 1 x nVert vector
                    # tempdata is a 3d volume
                    temp = map_coordinates(tempdata, coord)
                    ##!!!## make sure the replacement of ba_interp3_wrapper

                    # write out the file
                    writemgz(subjectid,f'{names[p]}_{surfsB[r]}',temp,hemi,outputdir)
