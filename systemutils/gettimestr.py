def gettimestr(fmt='short', structtime=None):
    '''
    Return a time string. This function is useful to obtain time-dependent file names

    <fmt> can be
        'short': Return a str like '20180423150203', to add as file name
        'full': return a full str like, '2018-09-25, 16:07:16', to print out timing info
    <structtime> can be a struct_time object returned by gmtime. If None, then we use
    the gmtime to get current time.


    We use strftime function to convert time str.

    Return a str like '20180423150203'


    '''
    from time import localtime, strftime, struct_time

    if isinstance(structtime, struct_time):
        if fmt=='short':
            return strftime('%Y%m%d%H%M%S', structtime)
        elif fmt=='full':
            return strftime('%Y-%m-%d, %H:%M:%S', structtime)
    elif structtime is None:
        if fmt == 'short':
            return strftime('%Y%m%d%H%M%S', localtime())
        elif fmt == 'full':
            return strftime('%Y-%m-%d, %H:%M:%S', localtime())
    else:
        raise ValueError(' Input is wrong !')


