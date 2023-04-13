class rzmodelfit(object):
    '''
    probablistic model fitting object by Ru-Yuan Zhang



    last updated by
    2022

    Examples:
        # define a function and data
        import numpy as np
        data = np.array([1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        def negloglikeli(params, data):
            from numpy import log, finfo
            import numpy as np
            eps = finfo(np.float64).eps
            head = data.sum()
            char = data.size-data.sum()
            params = params * 0.99 + eps
            nll = -log(params)*head-log(1-params)*char
            return nll

        # run the fitting
        from RZutilpy.stats import rzmodelfit
        model = rzmodelfit(func=negloglikeli, data=data, nFit=1) # Create an object
        model.setoptim(bounds=[(0,1)]) # set optimize options
        model.runfit() # do it 
    
    '''
    def __init__(self, func, data, **kwargs):
        self.objectFun = func # a voxels
        self.data = data
        self.nVars = 1

        # deal with kwargs for model fitting
        # set some default values
        default_args = {
            'nFit': 20, # number of optimizations to run
        }
        # update keywards to default settings
        default_args.update(kwargs)

        self.nFit=default_args['nFit']

    def runfit(self, **kwargs):
        # the main function to run fitting
        
        # prepare initial values
        self.prepareinitvals()
        
        # Run fitting procedures
        self.runoptim()

        # display results
        pass

    def setoptim(self, **kwargs):
        # set optimizations
        default_opt = {
            'method': 'L-BFGS-B', # default methods
            'args': self.data, # arguments
            'options':{}
        }
        default_opt.update(kwargs)
        
        match default_opt['method']:
            case 'L-BFGS-B':
                pass
            case 'BFGS':
                pass

        # change some defaul options
        default_opt['options'].update({'disp': 3})

        self.opt = default_opt

    def prepareinitvals(self):        
        # prepare model fitting, we mainly do 
        # (1): calculate and setting initial values
        # (2): setting optimizations initial values
        from numpy import empty, linspace
        # prepare initialize seed
        print('Prepare initial values...')
        self.initVals = empty((self.nFit, self.nVars))
        for iVar in range(self.nVars):
             self.initVals[:, iVar]= linspace(self.opt['bounds'][iVar][0], self.opt['bounds'][iVar][1], self.nFit, endpoint=True)
    
    def runoptim(self):
        # run optimization
        from numpy import empty, argmin, hstack
        print('Running optimizations...')
        from scipy.optimize import minimize
        fvals, aic, bic, lme = empty((self.nFit)),empty((self.nFit)),empty((self.nFit)),empty((self.nFit))
        fitvals = empty((self.nFit, self.nVars))
        
        for iFit in range(self.nFit):
            print(f'{iFit} times Fit... ')
            result = minimize(self.objectFun, self.initVals[iFit, :], **self.opt)
            
            fvals[iFit] = result.fvals # negative loglikelihood
            aic[iFit] = self.computeaic(fvals[iFit])
            bic[iFit] = self.computebic(fvals[iFit])
            lme[iFit] = self.computelme(result)
            
            fitvals[iFit, :]=result.x
        
        # find the best fitting values
        idx = argmin(fvals)
        self.fitResults['bestfitvals'] = fitvals[idx, :]
        self.fitResults['bestfitmetrics'] = hstack((fvals[idx], aic[idx], bic[idx], lme[idx]))
        self.fitResults['metricnames'] = ['negloglikeli', 'AIC', 'BIC', 'LME']
        
    def computeaic(self, fvals):
        # compute AIC value
        return 2*fvals + 2*self.nVars

    def computebic(self, fvals):
        # compute BIC value
        from numpy import log
        return 2*fvals + self.nVars * log(self.nDataPts)

    def computeLME(self, result):
        # compute log model evidence
        from numpy import identity, log, pi
        from scipy.linalg import det
        # get hessian
        hessMat = result.hess_inv
        hessMat = hessMat * identity(hessMat.shape[1])
        
        lme = result.fval + 0 + self.nVars/2 * log(2*pi) - 1/2*log(det(hessMat))
        return lme