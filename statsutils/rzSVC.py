def rzSVC(data, label, cv=10, kernel='linear', multiclass='one-other', **kwargs):
    '''
    wrapper of ski-learn surpport vector classifer
    
    <data>: an 2D array with [nSamples, nFeatures]
    <label>: 1D array with [nSamples,]
    <kernel>(optional): kernel for SVC, default:'linear'
    <cv>(optional): int, n-fold cross validation, for cross_val_score function
    <multiclass>(optional):
        'one-other' (default): classify one versus all the other
        'one-one': classify one versus the other one categories
    <kwargs>: kwargs for SVC and linearSVC function

    Note:
        1. we output the average score (one value) of different cross validations
        2. we perform feature scaling using StandardScaler() function
        3. For two classification problem, we use SVC function. For multi-class problem, if, <multiclass> is 'one-one', we use SVC function to perform one verus one function, if <multiclass> is 'one-other', we use linearSVC function to perform one versus the other classification. In the later case, we can only use linear SVM.

    20200317 RZ switched to default function from SVC to linearSVC
    '''

    from sklearn.model_selection import cross_val_score
    from sklearn.pipeline import make_pipeline 
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC, LinearSVC

    from numpy import unique
    if unique(label).size == 2: # two-class
        # return cross_val_score(make_pipeline(StandardScaler(), LinearSVC(**kwargs)), data, label, cv=cv).mean() if kernel == 'linear' else cross_val_score(make_pipeline(StandardScaler(), SVC(kernel=kernel, **kwargs)), data, label, cv=cv).mean()

        return cross_val_score(make_pipeline(StandardScaler(), SVC(kernel=kernel, **kwargs)), data, label, cv=cv, verbose=1).mean()
        

    elif unique(label).size > 2: # multi-class
        if multiclass == 'one-one':
            return cross_val_score(make_pipeline(StandardScaler(), SVC(kernel=kernel, **kwargs)), data, label, cv=cv).mean()
        elif multiclass == 'one-other':
            return cross_val_score(make_pipeline(StandardScaler(), LinearSVC(**kwargs)), data, label, cv=cv, verbose=1).mean()
       




