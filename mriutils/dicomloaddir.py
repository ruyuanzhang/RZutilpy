def dicomloaddir(files, filenamepattern='*.dcm', maxtoread=None, phasemode=None,\
    desiredinplansize=None, dformat='float'):
    '''
    dicomloaddir(files, filenamepattern='*.dcm', maxtoread=None, phasemode=None,\
        desiredinplansize=None, dformat='float'):

    load multiple dicom files in one or multi directories

    Input:
        <files>: can be:
            (1) a string of a directory
            (2) a list of (2)
            (3) a rzpath object
            (4) a list of (3) object
        <filenamepattern>: str, the wildcard for the dicom file in a directory
        <maxtoread>: int, maximum number of dicom files to read
        <phasemodel>: ...implement later, ignore for now...
        <desiredinplansize>: ...implement later, ignore for now...,
            a 1x2 array, desired inplace size, if dicom files
            do not follow this size, we resize it.
        <dformat>: ...implement later, ignore for now
            read in data format
    Output:
        <vollist>: a list of volume arrays for multiple runs, if just one run,
            we return the array
        <dicominfolist>: a list of dicom info dict for multiple runs, if just one run,
            we return the dicom info dict

    Note:
        1. This function currently works with Siemens Prisma 3T and Magnetom 7T, not sure
        other scanners like GE. For Siemens, we focus on these attributes (can update this):
            (0018, 0050) Slice Thickness
            (0028, 0030) Pixel Spacing
            (0051, 100b) AcquisitionMatrixText
            (0019, 100a) NumberOfImagesInMosaic, 1 if anatomical data
            (0018, 0080) Time (TR)
            (0018, 0081) Echo Time (TE)
            (0018, 1312) Inplane Phase Encoding Direction
            (0019, 1029) MosaicRefAcqTimes (slicetimeorder), None if anatomical data
            (0051, 1016) a str, check mosaic, read from the dicom file
            (0051, 100c) FOV
            We also add keys:
            'ismosaic': boolean, whether this is a mosaic image
            'voxelsize': 1x3 list, based on Slice Thickness and Pixel Spacing
            'AcquisitionMatrix': [phase, frequency] matrix, derived from AcquisitionMatrixText. Phase step
                has no meaning if data is structure?

            'FovSize':[phase_len, frequency_len] mm, derived from FOV
            'epireadouttime': calculated from rz.mri.dicom_readout_msec, only valid for epi, None if other files

        2. Note that all these keys are scanner specific. Most of these should work for
            Siemens scanner but might not work for GE or Phillipe scanner.


    Example:


    Todo:
        1. figure out how to add read phase data
        2. check if some of the fields do no exist
        3. resize image to accommodate desired inplane size
        4. save all metafile using pickel

    History:
        20180720 <files> now can accept path-like objects
        20180626 RZ fixed the bug for reading the anatomical files
        20180605 RZ use nibabel.nicom.csareader.get_csa_header() function to read
            csa file and get the [BandWidthPerPixelPhaseEncode]
        20180422 RZ change the stack images in the last step so user can see
            report while waiting for image stack
        20180420 RZ created this function

    '''

    from pydicom import dcmread
    from RZutilpy.rzio import matchfiles
    from RZutilpy.array import split2d
    from RZutilpy.mri import dicom_readout_msec
    from RZutilpy.system import rzpath
    from numpy import stack
    from progressbar import progressbar as pbar
    import re
    import time


    # deal with input
    files = [files] if not isinstance(files, list) else files
    # convert it to path-like object
    files = [rzpath(p) if not isinstance(p, rzpath) else p for p in files]


    # start to load
    dicominfolist = []
    vollist = []
    for iDir, filedir in enumerate(files):   # loop directory
        filepattern = filedir / filenamepattern
        dcmnames = matchfiles(filepattern.str)
        if len(dcmnames) == 0:
            print('This {} does not appear to be a directory containing {} files, so skipping.\n'.format(filedir,filenamepattern))
            break
        else:
            print('This {} appear to be a directory containing {} files, so loading.\n'.format(filedir, filenamepattern))

        dcmnames = dcmnames[:maxtoread]  # remove last couple of dcm files

        # ====== deal with dicom info, save a customized dicominfo dict =======
        import matplotlib.pyplot as plt;import ipdb;ipdb.set_trace();
        ds = dcmread(dcmnames[0].str)  # read 1st vol for info purpose
        # note current we assume this dicom have all fields below!! And we save
        # the very raw dicom info here
        dcminfothisrun= dict()
        dcminfothisrun['SliceThickness'] = ds[int('0018', 16), int('0050', 16)].value
        dcminfothisrun['PixelSpacing'] = ds[int('0028', 16), int('0030', 16)].value
        dcminfothisrun['AcquisitionMatrixText'] = ds[int('0051', 16), int('100b', 16)].value
        dcminfothisrun['RepetitionTime'] = ds[int('0018', 16), int('0080', 16)].value
        dcminfothisrun['EchoTime'] = ds[int('0018', 16), int('0081', 16)].value
        dcminfothisrun['InplanePhaseEncodingDirection'] = ds[int('0018', 16), int('1312', 16)].value
        dcminfothisrun['FOV'] = ds[int('0051', 16), int('100c', 16)].value
        dcminfothisrun['checkmosaic'] = ds[int('0051', 16), int('1016', 16)].value

        # figure out whether it is mosaic image
        if dcminfothisrun['checkmosaic'].find('MOSAIC') >=0:
            dcminfothisrun['ismosaic'] = True  # indicate this is a epi file
            print('We are loading some mosaic images, need to convert a mosaic image to 3d,\
                this directory might contain epi data ...\n')
        else:
            dcminfothisrun['ismosaic'] = False  # indicate this is not a epi file
        if [int('0019', 16), int('100a', 16)] in ds:  # simense
            dcminfothisrun['NumberOfImagesInMosaic'] = ds[int('0019', 16), int('100a', 16)].value if dcminfothisrun['ismosaic'] else 1
        elif [int('0021', 16), int('104f', 16)] in ds:  # GE
            dcminfothisrun['NumberOfImagesInMosaic'] = ds[int('0021', 16), int('104f', 16)].value if dcminfothisrun['ismosaic'] else 1

        dcminfothisrun['MosaicRefAcqTimes'] = ds[int('0019', 16), int('1029', 16)].value if dcminfothisrun['ismosaic'] else None
        dcminfothisrun['epireadouttime'] = dicom_readout_msec(ds)[0] if dcminfothisrun['ismosaic'] else None

        # save voxel size
        dcminfothisrun['voxelsize'] = list(dcminfothisrun['PixelSpacing']) + [dcminfothisrun['SliceThickness']]

        # figure out inplane matrix, not that we assume
        # note this regular expression might fail in normal resolution imaging

        p = re.compile(r'^(\d{1,4}).?\*(\d{1,4}).?$')
        matchgroup = p.match(dcminfothisrun['AcquisitionMatrixText'])
        if matchgroup:
            plines = int(matchgroup.group(1))  # step in phase encoding direction
            flines = int(matchgroup.group(2))  # step in frequency encoding direction
            dcminfothisrun['AcquisitionMatrix'] = [plines, flines]
        else:
            ValueError('can not find the phase encoding direction!')

        # figure out inplane matrix, not that we assume
        p = re.compile(r'^FoV (\d{1,6})\*(\d{1,6})$')
        matchgroup = p.match(dcminfothisrun['FOV'])
        p_len = int(matchgroup.group(1))  # step in phase encoding direction
        f_len = int(matchgroup.group(2))  # step in frequency encoding direction
        dcminfothisrun['FovSize'] = [p_len / 10, f_len / 10] if dcminfothisrun['ismosaic'] else [p_len, f_len]
        # have to divide this number by 10 for epidata, not sure why....

        # save dicom info in this run
        dicominfolist.append(dcminfothisrun)
        # show some information
        print(dcminfothisrun)

        # ================  deal with the volumes ====================
        print('\nReading in dicoms ......')
        vol = [dcmread(i.str).pixel_array for i in pbar(dcmnames)]   # read pixel data
        # split mosaic images
        if dcminfothisrun['ismosaic']:
            # Note that we assume plines and flines will be exact divided by the image
            # this is typically true
            vol = [split2d(i, plines, flines) for i in vol]  # split each 2d mosaic image to 3d image
            # only keep acquired slices, the last several images are sometimes black
            vol = [i[:, :, :dcminfothisrun['NumberOfImagesInMosaic']] for i in vol]

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
        if dcminfothisrun['ismosaic']:
            print('These are mosaic images, might be epi data.\n')
        else:
            print('These are not mosaic images, might not be epi data.\n')
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




