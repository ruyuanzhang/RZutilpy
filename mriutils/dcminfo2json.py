def dcminfo2json(dcm, filename):
    '''
    Save the scanning info from a dicom file into json format. THis is useful to keep
    all scanning parameters when converting dcm files to nifti. Also useful to prepare
    BIDS format

    Input:
        <dcm>: dicom file, can be
            (1), a string or a path-lib object towards ONE '*.dcm' file
            (2), a string or a path-lib object towards the directory contain '*.dcm' file
                In this case, we only read the head info from the 1st dcm
            (3), a pydicom object
        <filename>: a string or a path-lib object, with or without '.json' suffix are all OK

    Note:
        1. Currently this program only support Siemens dicom files
        2. Echo time, repetition time, slice timing are all in ms
        3. we do some modification on raw dcm header
             (1) we remove '[Unknown]' parameters
             (2) we remove 'Patient*' parameters
             (3) we remove 'CSA' parameters
             (4) we rename '[MosaicRefAcqTimes]' to 'SliceTiming'
             (5) we remove 'Referenced Image Sequence'
             (6) we add 'FOV' and 'ismosaic'
        4. If you want to access individual DataElement, you must call
            dcm[tag], otherwise you can only get a RawDataElment object,
            which is weird. To obtain a list of DataElement. You can do like
            ele = [dcm[i.tag] for i in dcm.values()]

    History:
        20190413 RZ created
    '''
    from RZutilpy.rzio import savejson, matchfiles
    from RZutilpy.system import Path

    from pydicom import dcmread
    from pydicom.dataset import FileDataset
    import pydicom

    if not isinstance(dcm, FileDataset):
        dcm = Path(dcm)
        # judge it is a directory or a dcm file
        dcm = Path(matchfiles((dcm/'*.dcm').str)[0]) if dcm.suffix=='' else dcm
        #
        assert dcm.suffix=='.dcm', 'dcm input seems incorrect!'
        dcm = dcmread(dcm.str)

    assert isinstance(dcm, FileDataset), 'dcm here should be an pydicom FileDataset object!'

    # read the tag, keywords and values
    tmp = [dcm[i.tag] for i in dcm.values()]
    values = [i.value for i in tmp]
    descriptions = [i.description() for i in tmp]

    # first remove some unknown parameters
    data = [(i,j) for (i,j) in zip(descriptions, values) if i != '[Unknown]']
    # remove Patient information
    data = [(i,j) for (i,j) in data if 'Patient' not in i]
    # remove CSA header info
    data = [(i,j) for (i,j) in data if 'CSA' not in i]

    # remove pixel data
    data = dict(data)
    data.pop('Pixel Data', None)

    # manually add and adjust some information
    data['FOV'] = dcm[int('0051', 16), int('100c', 16)].value
    data['ismosaic'] = dcm[int('0051', 16), int('1016', 16)].value
    data.pop('Referenced Image Sequence', None)
    data['SliceTiming'] = data.pop('[MosaicRefAcqTimes]', None)

    try:
        data.pop('Icon Image Sequence')
        data.pop('Source Image Sequence')
    except:
        pass

    # deal with pydicom data type issue... This is stupid
    for i,j in data.items():
        if isinstance(j, pydicom.multival.MultiValue):
            data[i] = list(j)
        elif isinstance(j, pydicom.valuerep.DSfloat) or isinstance(j, pydicom.valuerep.IS):
            data[i] = float(j)
        elif isinstance(j, pydicom.uid.UID) or isinstance(j, pydicom.valuerep.PersonName3):
            data[i] = str(j)

    #import ipdb;ipdb.set_trace();import matplotlib.pyplot as plt;
    # save json and return the dict
    savejson(filename, data)
    return data





