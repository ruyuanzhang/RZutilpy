def rzSVC(data, label, C=1, cv=10, kernel='linear', multiclass=''):
    '''
    wrapper of ski-learn surpport vector classifer
    
    <data>: an 2D array with [nSamples, nFeatures]
    <label>: 1D array with [nSamples,]
    <C>(optinal): hyperparameter, default:1
    <kernel>(optional): kernel for SVC, default:'linear'
    <cv>(optional): int, n-fold cross validation
    <multiclass>(optional):
        'one-one'(default): 
        'one-other': 

    Note:
        1. we output the average score (one value) of different cross validation
        2. Note that we perform feature scaling using StandardScaler(), function
        3. For two classification problem, we use SVC function. For multi-class problem, if, <multiclass> is 'one-one', we use SVC function to perform one verus one function, if <multiclass> is 'one-other', we use linearSVC function to perform one versus the other classification. In the later case, we can only use linear SVM.

    '''

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC

from numpy import unique
if unique(label).size = 2: # two-class
    return cross_val_score(make_pipeline(StandardScaler(), SVC(C=C, kernel=kernel)), data, label, cv=cv).mean()

elif unique(label).size > 2: # multi-class
    if multiclass == 'one-one':
        return cross_val_score(make_pipeline(StandardScaler(), SVC(C=C, kernel=kernel)), data, label, cv=cv).mean() 
    elif multiclass == 'one-other':
        return cross_val_score(make_pipeline(StandardScaler(), LinearSVC(C=C)), data, label, cv=cv).mean()
       




