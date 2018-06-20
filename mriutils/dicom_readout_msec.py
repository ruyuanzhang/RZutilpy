def dicom_readout_msec(ds, mode='CVN'):
    '''
    dicom_readout_msec(ds, mode='CVN'):

    output the <epireadouttime> in milliseconds. This function is based on Keith's
    matlab utility function dicom_readout_msec.m. The key variable is 'BandwidthPerPixelPhaseEncode'
    This variable is in csaheader. We use nibabel.nicom.csareader.get_csa_header()
    function to read this field.

    Input:
        <ds>: can be
            1. ds structure created by pydicom.dcmread()
            2. a file path or wildcard for a dicom file, e.g, 'MR008-0032.dcm'. When wildcard
                case, make sure only one matched file.
        <mode>: FSL and SPM expect different calculations of <epireadouttime>
            can be
            'FSL':
            'SPM','CVN' (default):
    Output:
        <epireadouttime> in millisecs, is an important variable in KK's func
            preprocessing pipeline to use fieldmap to correct
        <bpppe>: BandwidthPerPixelPhaseEncode in millisecs

    Note
        1. partial fourier does not effect distortion
        2. iPAT is "included" in echo spacing when computed directly from the
            dicom header bpppe, so don't separately account for that
        3. Chris said the regular expression approach might fail in some dataset.
            consider to use other one
    '''
    from pydicom import dcmread
    from pydicom.dataset import FileDataset
    from nibabel.nicom.csareader import get_csa_header
    from RZutilpy.rzio import matchfiles
    import re

    if isinstance(ds, FileDataset):
        pass
    elif isinstance(ds, str):
        try:
            ds = matchfiles(ds)
            ds = dcmread(ds)
        except:
            print('dicom read failed, double check this file')

    csa = get_csa_header(ds)
    bpppe = csa['tags']['BandwidthPerPixelPhaseEncode']['items'][0]

    # figure out inplane matrix, not that we assume

    # use regular expression might be wrong for some data structure.. be careful
    p = re.compile(r'^(\d{1,4})p\*(\d{1,4})s$')

    matchgroup = p.match(ds[int('0051', 16), int('100b', 16)].value)
    npe = int(matchgroup.group(1))  # step in phase encoding direction

    es = 1/(bpppe * npe)

    if mode.upper() in ['SPM', 'CVN']:
        epireadouttime=1000 * npe * es
    elif mode.upper() in ['FSL']:
        epireadouttime=1000 * (npe - 1) * es

    return epireadouttime, bpppe

