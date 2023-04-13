def list2dataframe(data: list, datalabels:list, columns=None):
    '''
    A utility function to convert list data to dataframe. This is mainly for ploting purpose
    
    <data>: a list of 1d numpy array to plot
    <datalabels>: a list of string or list with labels corresponding to each data group
        with two formats 
        1. ['cat1', 'cat2',...] only one grouping factor
        2. (['cat1', 'group1'], ['cat2', 'group1'],...,['cat1', 'group2'], ['cat2', 'group2'], ...) multiple grouping factor
    '''
    assert len(data) == len(datalabels), 'inconsistent length of data and datalabels'

    # clean the data
    if type(datalabels[0])!=list:
        datalabels = [[i] for i in datalabels]

    assert len(columns) == len(datalabels[0]), 'inconsistent dimensions between columns and datalabels'

    df = []
    from pandas import DataFrame
    for i in range(len(data)):
        df = df + [[j] + datalabels[i] for j in data[i]]
    
    columns.insert(0, 'data')
    return DataFrame(df, columns=columns)