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
        <vollist>: a list of volume arrays for multiple runs, if just one run,
            we return the array
        <dicominfolist>: a list of dicom info dict for multiple runs, if just one run,
            we return the dicom info dict

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
        (0051, 1016) check ismosaic, if yes, multiple slices written in a big mosaic image
        (0051, 100c) FOV
        We also add keys:
        'ismosaic': boolean, whether this is a mosaic image
        'voxelsize': 1x3 list, based on Slice Thickness and Pixel Spacing
        'AcquisitionMatrix': [phase, frequency] matrix, derived from AcquisitionMatrixText
        'FovSize':[phase_len, frequency_len] mm, derived from FOV

    Example:


    Todo:
        1. figure out how to add read phase data
        2. check if some of the fields do no exist
        3. resize image to accommodate desired inplane size


    History:
        20180422 RZ change the stack images in the last step so user can see
            report while waiting for image stack
        20180420 RZ created this function

    '''
    from os.path import join
    from pydicom import dcmread
    from RZutilpy.rzio import matchfiles
    from RZutilpy.array import split2d
    from numpy import stack
    import progressbar
    import re
    import time


    # deal with input
    if isinstance(files, str):
        files = [files]  # single dicom, convert it to list
    elif isinstance(files, list):
        pass
    else:
        raise ValueError('Wrong file directories !')

    # progress bar
    pbar =  progressbar.progressbar

    # start to load
    dicominfolist = []
    vollist = []
    for iDir, filedir in enumerate(files):   # loop directory
        filepattern = join(filedir, filenamepattern)
        dcmnames = matchfiles(filepattern)
        if len(dcmnames) == 0:
            print('This {} does not appear to be a directory with DICOM files, so skipping.\n'.format(filedir))
            break
        else:
            print('This {} appear to be a directory with DICOM files, so loading.\n'.format(filedir))

        dcmnames = dcmnames[:maxtoread]  # remove last couple of dcm


        # ====== deal with dicom info, save a customized dicominfo dict =======
        ds = dcmread(dcmnames[0])  # read 1st vol for info purpose
        # note current we assume this dicom have all fields below!! And we save
        # the very raw dicom info here
        dcminfothisrun= dict()
        dcminfothisrun['SliceThickness'] = ds[int('0018', 16), int('0050', 16)].value
        dcminfothisrun['PixelSpacing'] = ds[int('0028', 16), int('0030', 16)].value
        dcminfothisrun['AcquisitionMatrixText'] = ds[int('0051', 16), int('100b', 16)].value
        dcminfothisrun['NUmberOfImagesInMosaic'] = ds[int('0019', 16), int('100a', 16)].value
        dcminfothisrun['RepetitionTime'] = ds[int('0018', 16), int('0080', 16)].value
        dcminfothisrun['EchoTime'] = ds[int('0018', 16), int('0081', 16)].value
        dcminfothisrun['InplanePhaseEncodingDirection'] = ds[int('0018', 16), int('1312', 16)].value
        dcminfothisrun['MosaicRefAcqTimes'] = ds[int('0019', 16), int('1029', 16)].value
        dcminfothisrun['checkmosaic'] = ds[int('0051', 16), int('1016', 16)].value
        dcminfothisrun['FOV'] = ds[int('0051', 16), int('100c', 16)].value

        # figure out whether it is mosaic image
        if dcminfothisrun['checkmosaic'].find('MOSAIC'):
            dcminfothisrun['ismosaic'] = True
            print('We are loading some mosaic images, need to convert them to 3d ...\n')

        # save voxel size
        dcminfothisrun['voxelsize'] = list(dcminfothisrun['PixelSpacing']) + [dcminfothisrun['SliceThickness']]

        # figure out inplane matrix, not that we assume
        p = re.compile(r'^(\d{1,4})p\*(\d{1,4})s$')
        matchgroup = p.match(dcminfothisrun['AcquisitionMatrixText'])
        plines = int(matchgroup.group(1))  # step in phase encoding direction
        flines = int(matchgroup.group(2))  # step in frequency encoding direction
        dcminfothisrun['AcquisitionMatrix'] = [plines, flines]

        # figure out inplane matrix, not that we assume
        p = re.compile(r'^FoV (\d{1,6})\*(\d{1,6})$')
        matchgroup = p.match(dcminfothisrun['FOV'])
        p_len = int(matchgroup.group(1))  # step in phase encoding direction
        f_len = int(matchgroup.group(2))  # step in frequency encoding direction
        dcminfothisrun['FovSize'] = [p_len / 10, f_len / 10]

        # save dicom info in this run
        dicominfolist.append(dcminfothisrun)
        # show some information
        print(dcminfothisrun)

        # ================  deal with the volumes ====================
        print('\nReading in dicoms ......')
        vol = [dcmread(i).pixel_array for i in pbar(dcmnames)]   # read pixel data
        # split mosaic images
        if dcminfothisrun['ismosaic']:
            # Note that we assume plines and flines will be exact divided by the image
            # this is typically true
            vol = [split2d(i, plines, flines) for i in vol]  # split each 2d mosaic image to 3d image
            vol = [i[:, :, :dcminfothisrun['NUmberOfImagesInMosaic']] for i in vol]  # only keep acquired slices

        # stack images, take a while
        print('\n\nStack images ......\n')
        vol = stack(vol, axis=-1)  # stack to a 3d/4d file
        if vol.ndim == 3:  # expand to 4d if only 3d
            vol = vol[..., None]
        vollist.append(vol)

        # report info
        print('The 3D dimensions of the final returned volume are {}.\n'.format
            (vol.shape[:3]))
        print('There are {} volumes in the fourth dimension.\n'.format(vol.shape[-1]))
        print('The voxel size (mm) of the final returned volume is {}.\n'.format\
            (dcminfothisrun['voxelsize']))
        print('The in-plane matrix size (PE x FE) appears to be {}.\n'.format\
            (dcminfothisrun['AcquisitionMatrix']))
        print('The field-of-view (mm) of the final returned volume is {}.\n'.format\
            (dcminfothisrun['FovSize']))
        print('The TR is {} ms.\n\n\n\n'.format(dcminfothisrun['RepetitionTime']))



    if len(vollist) == 1:
        vollist = vollist[0]
    if len(dicominfolist) == 1:
        dicominfolist = dicominfolist[0]
    return vollist, dicominfolist




