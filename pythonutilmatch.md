# general matlab tranlation

* repmat = np.tile
* permute = np.transpose
* squeeze = np.squeeze or a.squeeze() 
* matlab find = np.where
* sprintf = %
* np.sum can directly input boolean data type and count how many true
* cell2mat = np.block
* get the index of the max value
```
a.argmax()
a.argmin()
```
* cellfun = map
# translating knkutil and RZtuil from matlab to python


## colormap and figure
* myplot = rz.figure.plot
* rz.figure.colormap

## graphic
## imageprocessing
## indexing
## io (rzio)
matchfiles = rz.rzio.matchfiles
## math
## matrix (array)
splitmatrix = rz.array.split
rotatematrix = np.rot90
## mri
## programming
unix_wrapper.m = rz.system.unix_wrapper
mkdirquite = os.makedirs
mkdirtemp = os.makedirs
## pt
## stats

## string
## timeseries