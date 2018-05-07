from .mridata import mridata

class T1data(mridata):
    '''
    T1data is a subclass of mridata. It inherits the mridata attributes and
    methods.


    Methods:
        runfreesurfer

    History
        20180424 RZ created it.
    '''

    def runfreesurfer(self, dataloc=None, extraflags=[]):
        '''
        push T1 data to freesurfer. Similar to cvnrunfreesurfer.m in cvncode

        We use subprocess

        <dataloc>: a NIFTI T1 .nii.gz file like '/home/stone-ext1/fmridata/AurelieData/Austin_3D.nii.gz'
        <extraflags>: a list of extra flags for recon-all. e.g.,[]

        To do:
            1. add T2 flag?? not sure if it is useful
        '''
        import os

        assert self.meanvol is not None, 'You might need to first calculate meanvol'
        assert os.path.exist(dataloc), 'The T1 nifti file does not exist! Consider save\
             the meanvol to nifti first'

        #
        comand = ['recon-all', '-s', self.subjectname, '-i', dataloc] + extraflags\
        + ['>', dataloc+'reconlog.txt']

        completeprocess = subprocess.run(comand, stdout=subprocess.PIPE)
        assert (completeprocess.returncode == 0), 'recon-all failed, check'


if __name__ == "__main__":
    pass



