def findminoutlier(funcfiles, outputDir=None):
    '''
    def findminoutlier(func, outputDir=None):

    Find the minimal outlier from a set of runs of functional data. This function is
    derived direct from the script generate from afni_proc. We want to isolate this part
    so we can use the minimal outlier to perform epi2anat alignment separately

    Input:
        <funcfiles>: can be
            (1): a string, a wildercard to matchfile multiple functional files
            (2): a list of strings of fullfile paths
        <outputDir>: output directory, can be a string or a path object
    Output:

    '''
    from RZutilpy.rzio import matchfiles
    from RZutilpy.system import unix_wrapper, Path, makedirs
    from os import getcwd
    from numpy import loadtxt

    funcfiles = matchfiles(funcfiles) if isinstance(funcfiles, str) else funcfiles
    assert len(funcfiles) >= 0, 'can not find data files!'

    nRuns = len(funcfiles)
    nVols_list = [ int(unix_wrapper(f'3dinfo -nt {i}')) for i in funcfiles]

    # deal with Path
    outputDir = Path(getcwd()) if outputDir is None else outputDir
    outputDir = Path(outputDir) if ~isinstance(outputDir, Path) else outputDir
    makedirs(outputDir) # create outputDir if not exist

    # remove existing files
    unix_wrapper(f'rm {outputDir}/out.pre_ss_warn.txt', verbose=False)
    unix_wrapper(f'rm {outputDir}/outcount.r**.1D', verbose=False)
    unix_wrapper(f'rm {outputDir}/out.min_outlier.txt', verbose=False)
    unix_wrapper(f'rm {outputDir}/vr_base_min_outlier*', verbose=False)


    # make outcount files
    pressfile = open(f'{outputDir}/out.pre_ss_warn.txt', 'w')
    for i in range(nRuns):
        unix_wrapper(f'3dToutcount -automask -fraction -polort 2 -legendre                     \
                {funcfiles[i]} > {outputDir}/outcount.r{i+1:02d}.1D', verbose=False)

        outcount = loadtxt(f'{outputDir}/outcount.r{i+1:02d}.1D')
        if outcount[0] >= 0.4:
            print(f"** TR #0 outliers: possible pre-steady state TRs in run {i+1:02d}", file=pressfile)
    pressfile.close()
    # combine all files
    unix_wrapper(f'cat {outputDir}/outcount.r*.1D > {outputDir}/outcount_rall.1D', verbose=False)

    import matplotlib.pyplot as plt;import ipdb;ipdb.set_trace();

    # find the which run and which volume
    outcountfile = loadtxt(f'{outputDir}/outcount_rall.1D')
    miniindex = outcountfile.argmin()
    i=0
    while i <= nRuns:
        if miniindex < sum(nVols_list[:i+1]):
            minoutrun = i+1
            minouttr = miniindex - sum(nVols_list[:i])
            break
        i=i+1

    min_outlier_vol_file = open(f'{outputDir}/out.min_outlier.txt', 'w')
    print(f'min outlier: run {minoutrun}, TR {minouttr}', file=min_outlier_vol_file)
    min_outlier_vol_file.close()

    # extract this vr_min_outlier
    unix_wrapper(f'3dbucket -prefix {outputDir}/vr_base_min_outlier "{funcfiles[minoutrun-1]}[{minouttr}]" ', verbose=False)
    print(f'min outlier: run {minoutrun}, TR {minouttr}')



