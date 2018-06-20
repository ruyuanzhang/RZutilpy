def gettimestr(structtime=None):
    '''
    Return a time string. This function is useful to obtain time-dependent file names

    <structtime> can be a struct_time object returned by gmtime. If None, then we use
    the gmtime to get current time.

    We use strftime function to convert time str.

    Return a str like '20180423150203'


    '''
    from time import localtime, strftime, struct_time

    if isinstance(structtime, struct_time):
        return strftime('%Y%m%d%H%M%S', structtime)
    elif structtime is None:
        return strftime('%Y%m%d%H%M%S', localtime())
    else:
        raise ValueError(' Input is wrong !')


