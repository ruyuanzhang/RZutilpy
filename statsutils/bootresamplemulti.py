def bootresamplemulti(x, nBoot=1000):
    '''
    bootresamplemulti(x, nBoot=1000):

    resample an vector for bootstrap. We assume input is a long vertical
    vector,then we generate nboot columes as the result. remember. this
    is sampling with replacement.

    Args:
        <x>: we flatten the x, x can be an array or a list
        <nBoot>: how many samples we want,default is 1000
    Return:
      sample:a x.size X <nBoot> matrix, each column is a sample
      ind: x.size X <nBoot> matrix, each column is a sample. value is the
          index in original input, ind must be int
    Note:
      it assumes sample with replacement

    Examples:
        sample,ind = rz.bootresamplemulti(rand(10,1),500);

    '''
    import numpy as np

    assert isinstance(x,np.ndarray), 'Input should be a ndarray'

    ind = np.random.randint(0, x.size, (x.size, nBoot))

    sample = x.flatten()[ind]

    return sample, ind