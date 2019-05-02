class funcpreprocess():
    '''
    an object to perform preprocessing of functional MRI data
    '''

    # some constants
    tsnrmx = 5          # max temporal SNR percentage (used in determining the color range)
    numinchunk = 30     # max images in chunk for movie
    fmapdiffrng = (-50, 50)  # range for fieldmap difference volumes

    # some input
    def __init__(self,epis,episize,epiinplanematrixsize,epitr,episliceorder,epiphasedir,epireadouttime,
        figuredir=None,inplanes=None,inplanesizes=None, fieldmaps=None,\
        fieldmapbrains=None,fieldmapsizes=None,fieldmapdeltate=None,\
        fieldmapunwrap=1,fieldmapsmoothing=(5,5,5),epifieldmapasst=None,\
        numepiignore=0, motionreference=(1,1),motioncutoff=1/90,extratrans=None,targetres=None,sliceshiftband=None,\
        fmriqualityparams=(None,None,None),fieldmaptimeinterp='cubic',mcmask=None,\
        maskoutnans=True,epiignoremcvol=None,dformat='f8',epismoothfwhm=None,wantpushalt=False):

        # ====== assign values=============
        self.figuredir = figuredir
        #inplanes
        self.inplanes = inplanes
        self.inplanesizes = inplanesizes
        # fieldmap
        self.fieldmaps = fieldmaps
        self.fieldmapbrains = fieldmapbrains
        self.fieldmapsizes = fieldmapsizes
        self.fieldmapdeltate = fieldmapdeltate
        self.fieldmapunwrap = fieldmapunwrap
        self.fieldmapsmoothing = fieldmapsmoothing
        self.fieldmaptimeinterp = fieldmaptimeinterp
        # epi
        self.epis = epis
        self.episize = episize
        self.epiinplanematrixsize = epiinplanematrixsize
        self.epitr = epitr
        self.episliceorder = episliceorder
        self.epiphasedir = epiphasedir
        self.epireadouttime = epireadouttime
        self.epifieldmapasst = epifieldmapasst
        self.numepiignore = numepiignore
        self.epismoothfwhm = epismoothfwhm
        # motion correction
        self.motionreference = motionreference
        self.motioncutoff = motioncutoff
        self.mcmask = mcmask
        # others
        self.extratrans = extratrans
        self.targetres = targetres
        self.sliceshiftband = sliceshiftband
        self.fmriqualityparams = fmriqualityparams
        self.maskoutnans = maskoutnans
        self.epiignoremcvol = epiignoremcvol
        self.dformat = dformat
        self.wantpushalt = wantpushalt

        #=========== some additional processing ====================
        self._wantfigs = (figuredir is not None)
        self._wantmotioncorrect = (motionreference is not None)
        self._epidim = epis[0].shape
        self._epifov = self._epidim * episize

    # ==================================================================
    # ========== posthoc properties ====================================
    # ==================================================================
    @property
    def nrmx(self):
        return self._nrmx

    # ==================================================================
    # =============== all methods ======================================
    # ==================================================================
    def writeoutinplanevols():
        pass

    def writeoutinplanevols():
        pass

    def slicetimecorrection(self):
        pass


    def fieldmapcorrection(self):
        pass


    def motioncorrection(self):
        pass


    def smoothfieldmap(self):
        pass

    def run(self):
        '''
        the main program that run the functional preprocessing. we detailed in step by step
        '''



        '''
        step 1.if you supply in-plane volumes, we write them out as figures for inspection.
        the in-plane volumes are individually contrast-normalized.  we also write out
        versions of the in-plane volumes that are matched to the field-of-view and
        resolution of the EPI data.  these versions are also individually
        contrast-normalized.
        '''
        writeoutinplanevols()

        '''
        step 2.for each EPI run, we drop volumes according to <numepiignore>
        '''
        dropfirstepis()

        '''
        step 3.for each EPI run, we perform slice time correction according to <episliceorder>,
        interpolating each slice to the time of the first slice.  to obtain new values,
        we use sinc interpolation, replicating the first and last time points to handle
        edge issues.  (in the case where <episliceorder> is a cell vector of length 2,
        we use pchip interpolation and change the TR of the data.)
        '''
        slicetimecorrection()

        '''
        step 4. for each EPI run, we compute the temporal SNR.  this is performed by regressing
        out a line from each voxel's time-series, computing the absolute value of the
        difference between successive time points, computing the median of these absolute
        differences, dividing the result by the mean of the original time-series, and then
        multiplying by 100.  negative values (which result when the mean is negative) are
        explicitly set to NaN.  we write out the temporal SNR as figures for inspection,
        using MATLAB's jet colormap.  high values (red) are good and correspond to a
        temporal SNR of 0%.  low values (blue) are bad, and correspond to a temporal SNR
        of 5.  (note that it would make some sense to take the reciprocal of the computed
        metric such that the mean signal level is in the numerator, but we leave it as-is
        since we believe having the median absolute difference in the numerator is simpler.)
        '''
        computewritetemporalsnr(self)

        '''
        step 5. we write out the first and last volumes of each EPI run to the directory "EPIoriginal".
        (the aggregate set of first volumes are contrast-normalized as a whole; the aggregate
        set of last volumes are contrast-normalized as a whole.)  we also write out the first
        30 volumes of the first EPI run to the directory "MOVIEoriginal".  (the set of volumes
        are contrast-normalized as a whole.)
        '''
        writeepioriginal()

        '''
        step 6. if fieldmaps are provided, we write out the fieldmaps, fieldmap brains, and a histogram
        of fieldmap values as figures for inspection.  we also write out versions of fieldmap
        brains that are matched to the field-of-view and resolution of the EPI data.  we also
        write out successive differences of the fieldmaps (e.g. 2-1, 3-2, 4-3, etc.), accounting
        for phase wraparound.  the range of the fieldmap figures is -N Hz to N Hz, where N is
        1/(<fieldmapdeltate>/1000)/2.  the range of the fieldmap difference figures is -50 Hz
        to 50 Hz.  the fieldmap brain figures are individually contrast-normalized.
        '''



