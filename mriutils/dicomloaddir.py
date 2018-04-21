def dicomloaddir(files, filenamepattern='*.dcm', maxtoread=None, phasemode=None,\
    desiredinplansize=None, dformat='float'):
    '''
    load multiple dicom files in one of multi directories
    Input:
        <files>: directory of a list of directories to read dicom
        <filenamepattern>: str, the wildcard for the dicom file in a directory
        <maxtoread>: int, maximum number of dicom files to read
        <phasemodel>: ..implement later, ignore for now..
        <desiredinplansize>: a 1x2 array, desired inplace size, if dicom files
            do not follow this size, we resize it.
        <dformat>: data format to save, sometimes to reduce memory burden
    Output:
        <vol>:
        <volizes>:
        <inplanmatrixsize>:
        <trs>:

    Note:
    1. This function currently works with Siemens prisma and magnetom 7T, not sure
    GE scanner. For Siemens, we focus on these attributes (can update this):
        (0018, 0050) Slice Thickness
        (0028, 0030) Pixel Spacing
        (0051, 100b) AcquisitionMatrixText
        (0019, 100a) NUmberOfImagesInMosaic
        (0018, 0080) Time (TR)
        (0018, 0081) Echo Time (TE)
        (0018, 1312) Inplane Phase Encoding Direction
        (0019, 1029) MosaicRefAcqTimes (slicetimeorder)
        (0051, 1016) check ismosaic, if yes, multiple slices written in a big mosaic
            image
        We also add keys:
        'ismosaic': boolean, whether this is a mosaic image
        'voxelsize': 1x3 list, based on Slice Thickness and Pixel Spacing
        'AcquisitionMatrix': [phase, frequency] matrix, derived from AcquisitionMatrixText

    Example:


    Todo:
    1. figure out how to add read phase data
    2. check if some of the fields do no exist


    History:
        20180420 RZ created this function

    '''
    from os.path import join
    from pydicom import dcmread
    from RZutilpy.rzio import matchfiles
    from RZutilpy.array import split2d
    from numpy import stack
    import re


    # deal with input
    if isinstance(files, str):
        files = [files]  # single dicom, convert it to list
    elif isinstance(files, list):
        pass
    else:
        raise ValueError('Wrong file directories !')

    dicominfolist = []
    vollist =
    for iDir, filedir in enumerate(files):   # loop directory
        filepattern = join(filedir, filenamepattern)
        dcmnames = matchfiles(filepattern)
        if len(dcmnames) == 0:
            print('this {} does not appear to be a directory with DICOM files, so skipping.\n'.format(filedir))
            break
        else:
            print('this {} appear to be a directory with DICOM files, so loading.\n'.format(filedir))

        dcmnames = dcmnames[:maxtoread]  # remove last couple of dcm


        # ====== deal with dicom info, save a customized dicominfo dict =======
        ds = dcmread(dcmnames[0])  # read 1st vol for info purpose
        # note current we assume this dicom have all fields below!! And we save
        # the very raw dicom info here
        dcminfothisrun['SliceThickness'] = ds[int('0018', 16), int('0050', 16)].value
        dcminfothisrun['PixelSpacing'] = ds[int('0028', 16), int('0030', 16)].value
        dcminfothisrun['AcquisitionMatrixText'] = ds[int('0051', 16), int('100b', 16)].value
        dcminfothisrun['NUmberOfImagesInMosaic'] = ds[int('0019', 16), int('100a', 16)].value
        dcminfothisrun['RepetitionTime'] = ds[int('0018', 16), int('0080', 16)].value
        dcminfothisrun['EchoTime'] = ds[int('0018', 16), int('0081', 16)].value
        dcminfothisrun['InplanePhaseEncodingDirection'] = ds[int('0018', 16), int('1312', 16)].value
        dcminfothisrun['MosaicRefAcqTimes'] = ds[int('0019', 16), int('1029', 16)].value
        dcminfothisrun['checkmosaic'] = ds[int('0051', 16), int('1016', 16)].value

        # figure out whether it is mosaic image
        if dcminfothisrun['checkmosaic'].find('MOSAIC'):
            dcminfothisrun['ismosaic'] = True
            print('We are loading some mosaic images, need to convert them to 3d')


        # save voxel size
        dcminfothisrun['voxelsize'] = dcminfothisrun['PixelSpacing'].append(dcminfothisrun['voxelsize'])
        print('voxel size is {}\n'.format(dcminfothisrun['voxelsize']))

        # figure out inplan matrix, not that we assume
        p = re.compile(r'^(\d{1,4})p\*(\d{1, 4})s$')
        matchgroup = p.match(dcminfothisrun['AcquisitionMatrixText'])
        plines = int(matchgroup(1))  # step in phase encoding direction
        flines = int(matchgroup(2))  # step in frequency encoding direction
        dcminfothisrun['AcquisitionMatrix'] = [plines, flines]
        print('Inplane matrix is {}\n'.format(dcminfothisrun['AcquisitionMatrix']))

        # save dicom info in this run
        dicominfolist.append(dcminfothisrun)
        print(dcminfothisrun)

        # ================  deal with the volumes ===============
        vol = [dcmread(i).pixel_array for i in dcmnames]   # read pixel data
        # split mosaic images
        if dcminfothisrun['ismosaic']:
            # how many images a mosaic include, we use the 1st element to figure out
            N = vol[0].shape[0]//plines
            nrows = vol[0].shape[0]//N
            ncols = vol[0].shape[1]//N
            vol = [split2d(i, nrows, ncols) for i in vol]  # split each 2d mosaic image to 3d image
        vol = stack(vol, axis=-1)  # stack to a 3d/4d file
        vollist.append(vol)

    return vollist, dicominfolist




