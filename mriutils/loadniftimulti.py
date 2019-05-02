def loadniftimulti(files):
    '''
    load multiple nifti file and return a list of the nifti object and a list
    of vols.

    <files> can be:
        1. a wildcard string
        2. a list of string specifying the filenames
        3. a list of path-like objects

    we return a list of vols <vols> and a list of nifti object <niftiobj>

    To do:
        1. what type of information we want to extract from nifti files?


    History:
        20180720 <files> can accept wildcard and a list of path-like objects
        20180424 RZ created it.

    '''
    from nibabel import load
    from RZutilpy.rzio import matchfiles

    if isinstance(files,str): # note that we treat it as wildcard not a single file name
        files = matchfiles(files)
    if ~isinstance(files,list): # which means only one volume matched
        files = [files]

    vols= []
    niftiobj = []
    for i in files:
        tmp = load(i)
        niftiobj.append(tmp)
        vols.append(tmp.get_data())

    return vols, niftiobj