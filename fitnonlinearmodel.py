class fitnonlinearmodel:
    '''

    <x> is :
        (1) a matrix with input x variables. this input should in theory give  rise to one set of data (a column)
        (a) a list of (1) indicating different runs
    <data> is :
        (1) an array with time points x voxels. Here we might need to use parallel computing to fit each individual voxels
        (2) a list of (1) indicating different runs
    '''

    def __init__(self, fitopt):
        self.fitopt = fitopt
        self.model = fitopt['model']
        self.x = fitopt['x']
        self.data = fitopt['y']
        #self.optresult = optimize(self)

        # prepare input and data
        if ~isinstance(self.x, list):
            list(self.x)
        if ~isinstance(self.data, list):
            list(self.data)
        assert len(self.x) == len(self.data), 'x and data have different run number'

        # prepare argument for optimization

    def set_default_optimizeparam(self)：
        default_optimizeparam = {

        }




    def helper_optimize(self):   # optimize the model
        import scipy.optimize as opt

        opt.least_squares(self.model, x0, bounds=(-inf, inf))

        return