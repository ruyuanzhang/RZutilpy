def scatterboxplot(data, xjiter=0.02, boxargs={}, scatterargs={}):
    '''
    customized scatter plot with individual data point
    '''
    
    # how many data groups
    l = len(data)
    color = ['C'+str(i) for i in range(l)]
     

    # default boxargs
    default_boxargs = \
    {
        'positions': range(l),
        'showfliers': False,
        'medianprops':{'color':color, 'lw': 5},
    }
    default_boxargs = default_boxargs | boxargs
    
    plt.box(data, **default_boxargs)

    # default scatter args
    default_scatterargs = \
    {
        'alpha': 0.5,
    }
    default_scatterargs = default_scatterargs | scatterargs


    for i in range(l): # loop data group
        x = np.random.rand(data[i].size)*xjiter
        plt.scatter(x, data[i], **default_scatterargs)



    