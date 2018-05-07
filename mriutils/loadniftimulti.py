def loadniftimulti(files):
    '''
    load multiple nifti file and return a list of the nifti object and a list
    of vols.

    <files> a list of string specifying the filenames,we return a list of vols
    <vols> and a list of nifti object <niftiobj>

    To do:
        1. what type of information we want to extract from nifti files?


    History:
        20180424 RZ created it.

    '''
    from nibabel import load
    vols= []
    niftiobj = []
    for i in files:
        tmp = load(i)
        niftiobj.append(tmp)
        vols.append(tmp.get_data())

    return vols, niftiobj