def rzboxplot(data:list, x:list=None, boxWidth:float=0.5, colors:list=None, **boxkwargs):
    '''
    A simple wrapper function that combines seaborn boxplot and stripscatter plot

    <data>: a list of numpy array data, sometimes we can use split function to parse an array into a list
    <x>: a list, positions of each bar
    <boxWidht>: default(0.5). Note that dot jitter range also correspond to <boxWidth>
    <color>: a list of colors for each category
    <boxkwargs>: TBD

    return:
    <box>: handle of boxes
    <scatter>: handles of scatter points
    '''

    import matplotlib.pyplot as plt
    from numpy import arange, random

    nBox = len(data) # how many boxes we draw

    if x is None:
        x = arange(nBox)
    if colors is None: # use default colors 
       colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    
    jitWidth = boxWidth
    
    box=[]
    scatter=[]
    for idx, value in enumerate(data): # loop data list
        
        # plot scatter first
        xx = random.uniform(x[idx]-jitWidth/2, x[idx]+jitWidth/2, size=value.shape)
        t = plt.scatter(xx, value, color=colors[idx])
        scatter.append(t)
        
        print(idx)

        # box plot
        c = t.get_facecolor() # get the color
        
        t = plt.boxplot(value, positions=(x[idx],), widths=boxWidth, showmeans=True, meanline=True, patch_artist=True, boxprops={'facecolor':'none', 'edgecolor':c, 'linewidth':2}, meanprops={'color':c, 'linestyle':'-', 'linewidth':2}, whiskerprops={'color':c, 'linewidth':2}, capprops={'color':c, 'linewidth':2},medianprops={'linestyle': ''}, zorder=-1)

        box.append(t.copy())

    return box, scatter
    