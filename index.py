'''
linspacepixels(x1, x2, n=50):
updatekeyvalue(x, y, mode=0):
'''


def linspacepixels(x1, x2, n=50):
    # return a vector of equally spaced points that can
    # be treated as centers of pixels whose total field-of-view
    # would be bounded by <x1> and <x2>.
    # linspacepixels(x1,x2,n)
    #
    # <x1>,<x2> are numbers
    # <n> is the number of desired points
    #
    # Example:
    # isequal(linspacepixels(0,1,2),[.25 .75])
    import numpy as np
    dif = (x2-x1)/n/2  # half the difference between successive points
    return np.linspace(x1+dif, x2-dif, num=n)


def updatedict2dict(x, y, mode=0):
    '''
    updatedict(x, y):

    update dict x using the value from y. First check any y element also exist in x. If yes, update the value of the key in x using the value in y. If x or y are an object, we update the attribute value

    <x>,<y> are dict
    <mode>: is
        (1) 0 means do not create new keys in x, if x does not have a element in y.
        (2) 1 means create a new keys and give the element value in y to x
        default 0
    '''
    assert isinstance(x, dict), 'Input should be a dict or a class'
    assert isinstance(y, dict), 'Input should be a dict or a class'

    for ele in y.keys():
        if ele in x.keys():
            x[ele] = y[ele]
        else:
            if mode == 0:
                continue
            elif mode == 1:
                x[ele] = y[ele]
    return x


def updatedict2class(x, y):
    '''
    updatedict2class(x, y, mode=0):

    We use the element in dict <y> to update attributes of class <x>.

    <x> is a class with some attributes.
    <y> is a dict. We use the value in y to update value in x.
    '''
    assert isinstance(y, dict), 'Input y should be a dict or a class'

    for ele in y.keys():
        if ele in x._dict_.keys():
            setattr(x, ele, y[ele])
    return x


def updateclass2dict(x, y, mode=0, wantaccessprivate=False):
    '''

    <x> is a dict. <y> is a class with some attributes.

    '''
    import re
    assert isinstance(x, dict), 'Input x, should be a dict or a class'

    regex = re.compile('_.')  # private attribute

    for ele in y.__dict__.keys():
        # use regular expression to match attribute start with '_'
        if re.match(regex, ele) & wantaccessprivate:  # this is a weakly private attribute and we want to update it
            if ele in x.keys():
                x[ele] = getattr(y, ele)
            else:
                if mode == 0:
                    continue
                elif mode == 1:
                    x[ele] = getattr(y, ele)
        elif re.match(regex, ele) & ~wantaccessprivate:  # this is a weakly private attribute but we do not want to update it
            continue
        else:  # not a private attribute
            if ele in x.keys():
                x[ele] = getattr(y, ele)
            else:
                if mode == 0:
                    continue
                elif mode == 1:
                    x[ele] = getattr(y, ele)
    return x

