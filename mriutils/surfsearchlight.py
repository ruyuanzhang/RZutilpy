def surfsearchlight(surf, datafile, func, radius=3, openmp=True, mp=4,\
    outprefix=None, intent=2005, verbose=False, method='3dsphere'):

    '''
    def surfsearchlight(surf, datafile, func, radius=3, openmp=True, mp=4,\
        outprefix=None, intent=2005):

    Perform surface-based search light analysis.

    Input:
        <surf>: a string, or path object indicate a surface file either in freesurfer format
            or .gii format. We read in this surface file to obtain geometry of surface vertices
        <datafile>: can be
                (1), .gii, .gii.gz surface data file, it should be in .gii format and the data should
                    be in nVert x M matrix, nVert is the number of vertex, M columns are data
                (2), nVert x M matric that internally can be directly used
        <func>: The function object to calculate, it takes in data file and generate output. Note
            that func either output a single value or output a tuple for multiple results
        <radius>: in mm (default: 3), radius to include vertex
        <openmp>: boolean, whether to use parallal computing, (default=True)
        <mp>: how many cores to open, default:20
        <outPrefix>: a string, we save to a .gii file, if you want to save to .gii file ,you must supply
            a .gii file for <datafile>
        <intent>: an int or a list of ints, intent number for each column of result array. This is necessary
            when saving results into a .gii file. check savegifti.py for more info
        <method>:
            (1) '3dsphere' (default), including vertex within a 3dsphere, typically run on a sphere or inflated surface
            (2) 'geodensic', using geodensic distance, which is more accurate but take a long time
                currently, this method seems problematic, I would not recommand this

    Output:
        We save a .gii file with the output


    20190413 RZ add <method>
    20190412 RZ created the file
    '''
    from numpy import ndarray, vstack, hstack, array, arange, where
    from RZutilpy.system import unix_wrapper, Path, gettimestr
    from RZutilpy.mri import savegifti

    from numpy import ndarray, vstack, array, arange
    from nibabel import load
    from nibabel.freesurfer.io import read_geometry

    from time import time
    from sklearn.neighbors import NearestNeighbors
    from pathos.multiprocessing import Pool

    from surfdist import surfdist

    # first read the surf file
    surf = Path(surf) if ~isinstance(surf, Path) else surf
    if surf.suffix == '.gii': # .gii format
        vtrx, faces = load(surf.str).darrays[0].data, load(surf.str).darrays[1].data
    else: # freesurfer format
        vtrx, faces = read_geometry(surf.str)

    # and read the data file
    if not isinstance(datafile, ndarray) and isinstance(datafile, str):
        datafile = Path(datafile)
        assert datafile.suffix == '.gii', 'data file should be .gii format!'
        giftiobj = load(datafile.str)
        data = [i.data for i in giftiobj.darrays]
        data = vstack(data).T # now data is nVert x M columns data file
    else:
        data = datafile

    del datafile

    # assert same number of vertices in surface and data
    assert data.shape[0]==vtrx.shape[0], 'surface file and data have different number of vertices!'
    nVtrx = data.shape[0]
    index = range(nVtrx)

    # calculate neighbour
    if method=='3dsphere':
        neigh = NearestNeighbors(radius=radius, metric='euclidean',n_jobs=mp)
        neigh.fit(vtrx) # in this case we first fit to the x, y, z
        nbrs = neigh.radius_neighbors(vtrx, return_distance=False)
    elif method=='geodesic': # slow... do not recommand
        # using surfdist
        def calcneighbors(i):
            print(i)
            dist = surfdist.dist_calc((vtrx, faces), index, i)
            return where(dist<=radius)[0]
        with Pool(mp) as p:
            # use imap, the returned results are in order
            #b = p.imap(calcneighbors, index, chunksize=2000)
            b = p.imap(calcneighbors, range(2000), chunksize=2000)
            nbrs = list(b)
    # note that nbrs is a ndarray, each element is an array since each element might have different

    # Define the wrapper function
    def runsearchlight(i):
        # get the index of neighbors
        idx = nbrs[i]
        # get the data of neighbors
        data_i = data[idx, :]
        if verbose:
            print(i)
        return func(data_i)

    # do it
    tstr = gettimestr('full')
    with Pool(mp) as p:
        # use imap, the returned results are in order
        b = p.imap(runsearchlight, arange(vtrx.shape[0]), chunksize=2000)
        #b = p.imap(runsearchlight, arange(2000), chunksize=2000)
        data2save = list(b)
    print(f'searchlight starts from {tstr}')
    print(f'searchlight ends     at {gettimestr("full")}')


    # let's take about 1d or 2d
    nCol = len(data2save[0]) if isinstance(data2save[0], tuple) else 1
    data2save = array(data2save) if nCol == 1 else vstack(data2save)

    # save the file
    if outprefix:
        assert 'giftiobj' in locals(), 'You must input a .gii file for data if you want to save result to .gii'
        savegifti(data2save, outprefix, giftiobj, intent)

    return data2save













