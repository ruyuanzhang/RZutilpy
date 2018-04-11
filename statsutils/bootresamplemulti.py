def bootresamplemulti(x, nBoot=1000, rtrnum=1):
    '''
    %
    % resample an vector for bootstrap. We assume input is a long vertical
    % vector,then we generate nboot columes as the result. remember. this
    % is sample with replacement.
    %
    % Args:
    %   x: we flatten the x, x can be an array or a list
    %   nboot: how many samples we want,default is 1000
    %   rtrnum: number of returned variable, default is 1,
    %        (only return 1 variable)
    % Return:
    %   sample:a x.size X nboot matrix, each column is a sample
    %   ind: x.size X nboot matrix, each columen is a sample. value is the
    %       index in original input, ind must be int
    % Note:
    %   1. it assumes sample with replacement
    %   2. cell case is OK
    %
    % Example:
    % [sample,ind] = rz.bootresamplemulti(rand(10,1),500);
    % isequal(size(sample),[10,500])
    '''
    import numpy as np
    x = np.array(x).flatten()  # convert to array and flatten
    ind = np.floor(
        np.random.rand(x.size, nBoot) * x.size
    ).astype(int)  # as index shoule be int

    sample = x[ind]

    if rtrnum == 1:
        return sample
    elif rtrnum == 2:
        return sample, ind