class rzmodelfit(object):
    def __init__(self, func, data, **kwargs):
        self.objectFun = func # a voxels
        self.data = data
        self.nDataPts = 

        # set some default parameters
        #from numpy import inf
        default_args = {
            'nFit': 20, # number of optimizations to run
            
            # necessary for argumentatation
            'args': None,
            'method':'L-BFGS-B',
            'options': {},

            'otherArgs': {}, # optional arguments for specifically for optimizations, include, 'bounds','jac','hessian', 'hessainp', 'constraitns' etc
        }
        # update keywards to default settings
        default_args.update(kwargs)

        # update otherArgs for optimizations
        default_args.update(default_args['otherArgs'])

        # prepare self.opt for ''
        match default_args['methods']:
            case 'L-BFGS-B':
                default_options={'disp': 99, 'maxcor': 10, 'ftol': 2.220446049250313e-09, 'gtol': 1e-05, 'eps': 1e-08, 'maxfun': 15000, 'maxiter': 15000, 'iprint': - 1, 'maxls': 20, 'finite_diff_rel_step': None}        
                
                default_args['options'] = default_options
                default_args.update(kwargs)
                
                self.opt = {
                    'args': default_args['args'],
                    'methods': default_args['methods'],
                    'bounds': default_args['bounds'],
                    'options': default_args['options'],
                }
                self.opt.update(default_args['otherArgs'])
        
        default_args.update(kwargs)
    

    def runfit(self, **kwargs):
        
        # prepare fitting
        self.prepareFit()
        
        # Run fitting procedures
        self.runOptimization()

        
        # after optimization, do some calculation
        self.fvals = 
        self.AIC = self.computeaic()
        self.BIC = self.computebic()
        self.LME = self.computelme()

        # display results


        pass

    def prepareFit(self):
        # prepare model fitting, we mainly do 
        # (1): calculate and setting initial values
        # (2): setting optimizations initial values

        from numpy import empty, linspace
        # prepare initialize seed
        print('Prepare initial values...\n')
        self.opt.initVals = empty(self.nFit, **self.nVars)
        for iVar in range(self.nVars):
             self.opt.initVals[:, iVar]= linspace(self.opt.bounds[iVar][0], self.opt.bounds[iVar][1], self.nFit, endpoint=True)
        
        # prepare optimizations options 
        print('Prepare optimization options...\n')
        self.opt.options = self.
    
    def runoptimization(self):
        # run optimization
        print('Running optimizations...')
        from scipy.optimize import minimize
        for iFit in range(self.nFit):
            print(f'\n{iFit} times Fit... ')
            result = minimize(self.objectFunc, self.opt)
        

    def computeaic(self):
        # compute AIC value
        return 2*self.negloglikeli + 2*self.nVars

    def computebic(self):
        # compute BIC value
        from numpy import log
        return 2*self.negloglikeli + self.nVars * log(self.nDataPts)

    def computeLME(self):
        # computer log model evidence
        pass