# this is the basic class of MRI data.
# anatomical and functional data are subclasses
class mridata:
    '''
    This is the basic class of MRI data. Anatomical and functional data
    are supposed to be subclasses

    Attributes
        <filenames>: a list of strings of filenames
        <fileformat>: a string, can be 'folder', 'nifti', 'dicom'
        <fileobjlist>: if <fileformat> is
            (1), 'folder', <fileobjlist> is a list of dicom info
            (2), 'nifti', <fileobjlist> is a list of nibabel nifti object
            (3), 'dicom', <fileobjlist> is a list of pydicom image object
        <sameshape>: Boolean, whether all arrays in vols have same shape
        <vols>: a list of ndarray volumes
        <shapes>: a list of shapes of <vols>
        <meanvol>
    Methods
        loaddata:
        alignvolumes:


    History:
        20180426 RZ fix the import bug (not fix the meanvols bug)
        20180423 RZ created it

    Todo:
        1. fix the mean volume bug
        2. multi volume alignment

    '''

    def __init__(self, filenames):
        '''
        <filenames> is a list of string of the dataset names. Each element
        can be one of the three cases:
            (1): a folder which contains multiple dcm files
            (2): a nifti file with ext '.nii' or '.nii.gz'
            (3): a dicom file with ext '.dcm'

        Note that all elements should be the same format of three cases !

        To do:
            1. different format for different element?

        '''

        # initialize attributes
        self.subjectname = None
        self.filenames = filenames
        self.fileformat = None
        self.sameshape = None
        self.vols = []
        self.shapes = []
        self.fileobjlist = []  # see loaddata function
        self.meanvol = []
        self.transform_matrix_tofirstvol = []
        self.vols_aligned = []

        from os.path import splitext
        # get the self.fileformat, get ext
        ext = [splitext(i)[1] for i in filenames]
        if all([i == '' for i in ext]):
            self.fileformat = 'folder'
        elif all([i == 'dcm' for i in ext]):
            self.fileformat = 'dicom'
        elif all([i[-7:] == '.nii.gz' or i[-4] == '.nii' for i in filenames]):
            self.fileformat = 'nifti'
        else:
            raise ValueError('Input file name is wrong, check filenames!')


    def loaddata(self, **kwargs):
        '''
        load data based on filenames and fileformat. Return a list of vols and a
        list of auxiliary information

        **kwargs are for loading functions, currently it support
            1. rz.mri.dicomloaddir
            2. rz.mri.loadniftimulti

        History:
            20180424 RZ created
        '''
        from RZutilpy.mri import dicomloaddir, loadniftimulti
        from pydicom import dcmread

        from numpy import all

        print('Loading the data, might take a while ...')
        if self.fileformat == 'folder':   # load a folder of dicom file
            self.vols, self.fileobjlist = dicomloaddir(self.filenames, **kwargs)
        elif self.fileformat == 'dicom':
            self.fileobjlist = [dcmread(i) for i in self.filenames]
            self.vols = [i.pixel_array for i in self.fileobjlist]
        elif self.fileformat == 'nifti':
            self.vols, self.fileobjlist = loadniftimulti(self.filenames)
        print('Done !')

        # Some sanity check
        if all([all(i.shape == self.vols[0].shape) for i in self.vols]):
            self.sameshape = True
        else:
            self.sameshape = False

        # save array
        self.shapes = [i.shape for i in self.vols]


    def alignvolumes(self):
        '''
        Align multiple volumes to the 1st one, this is useful to align multiple T1 or
        T2 volumes and created an averaged volume.

        Note that DONOT use this for aligning EPI and fieldmap data.

        This function will save a list of aligned volumes and a list save the transformation matrix


        '''

        # make the average volume
        self.meanvol = makeavgvolume(self)

        pass


    def writealignimg(self, outputprefix=None, **kwargs):
        '''

        This function is useful after you align multiple volumes to the first one
        and write out some images to check the goodness of the alignment. This
        usually happens in anatomical proprocessing.

        We use rz.mri.makeimagestack3d function to write image

        <outputprefix>: is a output prefix,if it is NONE, then no write. Can be ''
        <**kwargs>: is the keyword arguments for makeimagestack function.

        '''
        from RZutil.mri import makeimagestackmri

        if self.meanvol is not None:   # volumes have already been aligned
            # calculate residual images
            T1_mean_residual = [i - self.meanvol for i in self.vols]
            # write residual images and aligned vols
            for i, vol in enumerate(T1_mean_residual):
                # residual volume
                prefix = outputprefix + ('residual%02d_' % i)
                makeimagestackmri(vol, prefix, skips=[5,5,5])
                # aligned volume
                makeimagestackmri(self.vol_aligned[i], outputprefix + 'vol%02d' % i, skips=[5,5,5])
            # write the mean volume
            makeimagestackmri(self.meanvol, outputprefix + 'mean', skips=[5,5,5])


    def makemeanvolume(self, mode='separate'):
        '''
        average vols and make a mean volume. This is useful for 4D epi data, we
        average across time dimension to make a mean volume.

        <mode> can be 'separate' or 'all'
            'separate': We create a mean volume for each volumes self.vols. In
                this case we take the mean along the last dimension. This is useful
                for 4D epi data. (default)
            'all': We create a mean volume for all self.vols. This is useful for
                T1,T2 and epi runs.

        History:
            20180517 RZ added <mode input> and fix bugs
        '''
        from numpy import concatenate

        if mode == 'separate':
            self.meanvols = [self.vols[i].mean(axis=-1) for i in range(len(self.vols))]
        if mode == 'all':
            assert self.sameshape is False,\
             ValueError("Can not average volumes with different shapes, please set the mode='separate'!")
            self.meanvols = concatenate(self.vols, axis=-1).mean(axis=-1)




    def writevideomrimulti(self, volsidx=None, **kwargs):
        '''
        writevolumemrimulti, we use rz.mri.writevideomri.py function

        <volsidx>: an integer or a list, the we write self.vols[<volidx>], default is all

        <kwargs> are input variables for rz.mri.writevideomri.py
            among which, note that we use the folder name as the video filename

        We return the MovieClip object or a cell of it

        History:
            20180517 RZ fixed the bug of input name, and use writevideomri.py as the
                default function
        To do:
            1. input different names??
        '''
        from RZutilpy.mri import writevideomri

        if volsidx is None:
            volsidx = list(range(len(self.vols)))

        if ininstance(volsidx, list):
            return [writevideomri(self.vols[i], self.files[i]+'.mp4', **kwargs) for i in volsidx]
        elif ininstance(volsidx, int):
            return writevideomri(self.vols[volsidx], self.files[volsidx]+'.mp4', **kwargs)

    def collectT1T2s(self):
        pass
