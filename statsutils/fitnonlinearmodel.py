class fitnonlinearmodel():
    '''
    This is a general model fitting class for fitting nonlinear/and linear models.
    This is highly adapted to the individual vxs fitting

    The optimization procedure is a wrapper of scipy.optimize.least_squaes


    Properties:


    Methods:


    History:


    '''

    def __init__(self):
        import os
        #
        self._data = None
        self._input = None
        self._metric = correlation # default metric is correlation

        # default optimization, this is default for least_squares
        self._optimset = dict(jac='2-point', bounds=(-inf, inf), method='trf', ftol=1e-08, xtol=1e-08, gtol=1e-08, x_scale=1.0, loss='linear', f_scale=1.0, diff_step=None, tr_solver=None, tr_options={}, jac_sparsity=None, max_nfev=None, verbose=0, args=(), kwargs={})

        self.time_points = None # also number of data point
        self.nVoxels = None
        self.components = None
        self._isvxscase = False
        self.vxs = None

        #
        self.outputDir=os.getcwd() # default to the current directory

    def fit(self):
        '''
        do it, fit the model
        '''
        print('')

    # do some preprocessing
    def preprocess(self):

        # deal with vxs, currently we use simple cases

        # deal with the data
        self.loaddata() # load data if it is function case

        # assert input and data
        assert len(self._input)==len(self._data), 'Input and data have different runs'
        assert all([i.shape[0] == j.shape[0]for i in self._input and j in self._data])
        self.timePoints = [i.shape[0] for i in self._input]
        self.components = [i.shape[1] for i in self._input]
        self.totalnVxs = [i.shape[1] for i in self._data]
        self.nRuns = len(self._input)
        self.nModels = len(self._model)


    def loaddata(self):
        print('*** fitnonlinearmodel: loading data. ***\n')
        if callable(self.data):
            self._datafun = copy(self.data)
            if self._isvxscase:
                self.data = self.data(self.vxs)
            else:
                self.data = self.data()



    # set input stimulus
    @property
    def input(self):
        return self._input
    @input.setter
    def input(self, x):
        '''
        <stimulus> is:
          (1) a matrix with time points x components
          (2) a cell vector of (1) indicating different runs
          (3) a function that returns (1) or (2)
        '''
        from numpy import ndarray
        if isinstance(x, ndarray):
            # a matrix with time points x components
            self._input = [x]
            #assert(self.time_points = x.shape[0]) if self.time_points is None else self.time_points = x.shape[0]
        elif isinstance(x, list): # multiple runs
            self._input = x
        elif callable(x):  # it is a function
            # a function return (1) or (2)
            self.input = x()  # note the recursive here
        else:
            raise ValueError('Input can only be numpy array, list, a function')

    # set output data
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, x):
        '''
        <data> is:
            (1) a matrix with time points x voxels
            (2) a cell vector of (1) indicating different runs
            (3) a function that returns (1) or (2)
            (4) a function that accepts a vector of voxel indices and returns (1) or (2)
                  corresponding to those voxels.  in this case, <vxs> must be supplied.
        '''
        from numpy import ndarray
        from inspect import signature
        if isinstance(x, ndarray):
            self._data = [x]
        elif isinstance(x, list): # multiple runs
            self._data = x
        elif callable(x):  # it is a function
            # a function return (1) or (2)
            # currently we directly load data here, might be bad
            self._data = x
            x_sig = signature(x)
            if not x_sig.parameters: # x is a function, no vxs input
                self._isvxscase = False
                #self._data = x()
            else:
                assert self._vxs is not None, 'Check self._data and input vxs info'
                self._isvxscase = True  # only fit some vxs
                #self._data = x(self._vxs)
        else:
            raise ValueError('Input can only be numpy array, list, a function')

    # set model
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self, mdl):
        '''
        ** MODEL ***
        model> is a dict with keys
         {seed bounds func transform} where
           'seed' is the initial seed (1 x P).
           'bounds' are the bounds (2 x P).  NaNs in the first row indicate parameters to fix.
           'func' is a function that accepts two arguments, parameters (1 x P) and
             stimuli (N x C), and outputs predicted responses (N x 1).
           'transform' (optional) is a function that transforms stimuli into a new form prior
             to model evaluation.

        # to do...
        OR
         {M1 M2 M3 ...} where M1 is of the form {X Y Z W} described above,
           and the remaining Mi are of the form {F G H I} where
           F is a function that takes fitted parameters (1 x P) from the previous model
             and outputs an initial seed (1 x Pnew) for the current model
           G are the bounds (2 x Pnew).  NaNs in the first row indicate parameters to fix.
           H is a function that takes fitted parameters (1 x P) from the previous model
             and outputs a function that accepts two arguments, parameters (1 x Pnew) and
             stimuli (N x C), and outputs predicted responses (N x 1).
           I (optional) is a function that takes fitted parameters (1 x P) from the
             previous model and outputs a function that transforms stimuli into a
             new form prior to model evaluation.
        '''
        if isinstance(mdl, dict): # only one fit
            self._model = [mdl]
        #elif: isinstance(mdl, list): # sequential fit several models

    # set seed
    @property
    def seed(self):
        return self._seed
    @seed.setter
    def seed(self, x):
        pass

    # set optimization options
    @property
    def optimset(self):
        return self._optimset
    @optimset.setter
    def optimset(self, x):
        # the optimization settings must be a dict for optimization function
        from RZutilpy.program import updatedict
        try:
            updatedict(x, self._optimset, mode='check')
        except (ValueError, KeyError):
            print('Wrong keys in optimization dict')
            raise

    # metric
    @property
    def metric(self):
        return self._metric
    @metric.setter
    def metric(self, x):
        assert(callable(x))
        self._metric = x











