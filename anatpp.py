'''
This module
'''


class Anatpreprocess:
    def __init__(self, subjectid=None, datadir=None):
        self.subjectid = None
        self.datadir = None


    # collect all T1s
    def collectT1s(self, gradfile=None, str0='T1w', wantskip=True):
        import glob
        import os
        import subprocess

        datadir = self.datadir
        subjectid = self.subjectid

        # derive the data folder dir for this subject
        dir0 = self.datadir + '/' + subjectid
        # make a folder for this subject
        assert (os.mkdir(dir0))

        # massage, make it as a list
        if not isinstance(datadir, list):
            datadir = [datadir]

        t1files = []
        for iDir in len(datadir):
            t1fiels0 = glob.glob(datadir[iDir] + '/dicom/*{}*'.format(str0))
            if wantskip:
                assert (mod(len(t1fiels0), 2) == 0)
                t1fiels0 = t1fiels0[1::2]
            t1files = t1files.append(t1fiels0)

        # covert dicoms to NIFTIS and get the filenames
        files = []
        for iFile in len(t1files):
            result = subprocess.run('')



