from .mridata import mridata

class T2data(mridata):
    '''
    T2data is a subclass of mridata. It inherits the mridata attributes and
    methods. In addition,

    History
        20180424 RZ created it.
    '''

    def alignT2toT1(self, T1file, outputfolder):
        '''
        alignT2toT1(self, T1file, outputfolder):

        <T1file>: can be
            (1), a T1data instance, in this case, we look for T1file.meanvol
            (2), a nibabel nifity object
            (3), a 3d array
            (4), a path for T1 nifti file
        <outputfolder>, under which folder we save the data. Under <outputfolder>,
            we create a new subfolder 'T1T2alignment' and save all related
            info/figures under this figure
        '''
        pass
