def split(a, axis=-1, indices_or_sections=None):
    '''
    split(a, axis=0, indices_or_sections):
    wrapper of the np.split. see the definition of a, axis and indices_or _sections

    We make the following changes:
    1. indices_or_sections: default is a.shape[axis]. This means just split every
        single element along axis
    2. we squeeze the resulted array in element
    3. the default axis is -1, which means the largest dimension of an array.

    '''
    import numpy as np
    if indices_or_sections is None:
        indices_or_sections = a.shape[axis]
    b = np.split(a, indices_or_sections, axis=axis)
    # squeeze the b
    return [ele.squeeze() for ele in b]
    # b is a list