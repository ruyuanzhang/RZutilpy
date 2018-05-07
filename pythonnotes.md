# Some notes for python programming on neuroimaging 
* sklearn.neighbors.NearestNeighbors is a good class that can calculate nearestNeighbors in a ndimage. This might be useful to implement surface mapping to volume
* tkinter can be used for implementing the
* Many cost functions metrics have been provided by sklearn.metrics



# configure python and ipython
* Once Anoconda is properly installed, go to user home directory 
```
cd ~/.ipython/profile_default
nano scientific_startup.py
```
* all relevant configration will be in ~/.ipython/profile_default/ipython_config.py
* in ipython_config.py, we set the scientific_startup.py as the startup running file for ipython

# python command summary
* sys.path to show all path
* subprocess.run(['ls', '-al'])
* some useful path function

```
# get absolute path
os.path.abspath
# get foldername
os.path.dirname
# split the path
header, base = os.path.split(path)
# split the file and extension
file, extension = os.path.splitext(path)
# replace '~' with home directory, replace environment variable
os.path.expanduser(path)
os.path.expandvars

# check time
os.path.getatime
os.path.getctime
os.path.getmtime
```

* operate system 

```
# check environment variable
os.environ['PATH']
```

* convert hexadecimal numbers to decimal

```
s = '0061'
d = int(s, 16)
% this is useful when extracting dicom information
```

* merge two dicts

```
z = {**x, **y}
```

# Numpy specific 
* Some times use map/zip/list together
* np.split, np.reshape, np.vstack, np.hstack, np.dstack, np.concatenate, np.stack
* Note the difference between np.stack and np.concatenate
	- concatenate cannot create a new axis,
	- stack always create a new axis
	
concatenate array into the new axis, use np.stack, not np.concatenate

* repmat = np.tile
* permute = np.transpose
* squeeze = np.squeeze or a.squeeze() 
* matlab find = np.where
* np.sum can directly input boolean data type and count how many true
* sprintf = %
* cell2mat = np.block

```
'xxxx%02dxxx' % a
'xxxx%02dxxx%s' % (a, b) 

```
* get the index of the max value
```
a.argmax()
a.argmin()
```
* some useful path tool

```
# get current path
a = os.path.getcwd()
# get obsolute path of a file
a = os.path.get
# split path to base and the file
'xx/xx/name.mat' to ('xx/xx', 'name.mat')
a = os.path.split(filename)
# split path file and extension
'xx/xx/name.mat' to ('xx/xx/name', 'mat')
a = os.path.splitext(filename)
```

* (A==B).all()

```
    np.array_equal(A,B)  # test if same shape, same elements values
    np.array_equiv(A,B)  # test if broadcastable shape, same elements values
    np.allclose(A,B,...) # test if same shape, elements have close enough values
```

* intergers in numpy can not use elementwise negative power, should switch to float

```
    e.g., (np.arange(5)+1) ** (-3) report error
    e.g., (np.arange(5.0) + 1) ** (-3) is OK
```

y in ys
```

* change data type, a.astype('uint8')

* add a new axis
    ys = x[:50, np.newaxis]
    ys = x[:50, None, None]

* np.stack can pack multiple arrays in a list along the new axis
```
a = list( np.random.randn(3,3) for _ in range(3))
b = np.stack(a)
b.shape
c = np.stack(a)
c.shape
```
* note below
```
None == None
True
np.nan == np.nan
false
```


# Figure related (matplotlib)
* remove extra axes,
     fig.delaxes(ax[-1])

* get default colormap

```Python
plt.rcParams['axes.prop_cycle'].by_key()['color']
# can get other cmap
clist = rz.figure.colormap('gray', 20)
# if you want to use the color
plt.plot(x,y,c=clist(0))
# see all internal colormaps in matplotlib
https://matplotlib.org/examples/color/colormaps_reference.html
```

* build a colormap from a color list
```
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list(
                    'rzcolormap', cmap)
```

* use rz.figure.regplot can set scatter=False to remove all marker and only plot the line

* when setting the none color, please use like mfc='none', not mfc=None

* to get all children in an axes
```
child = axes.get_children()
```
* create a data-color look up table.
	1. use several normalize function in color module to normalize data to [0 1]. Actually normalize is a mapping function, input is the data value, output is the color. You can provide this norm object when use some ploting function, such as imshow, hist
	2. Then use axes.pcolormesh to create a pcm object.
	3. Use pcm object to plot colorbar 
	4. see example below
https://matplotlib.org/gallery/statistics/hist.html#sphx-glr-gallery-statistics-hist-py

* use plt.setp to set propertie to multiple axes

* axes.set_visible(False) can hide an axes. This is useful n x n subplots grid cannot be fully filled.

# String manipulation 
1. strcmp can use ==

matplotlib font

* family: A list of font names in decreasing order of priority. The items may include a generic font family name, either ‘serif’, ‘sans-serif’, ‘cursive’, ‘fantasy’, or ‘monospace’. In that case, the actual font to be used will be looked up from the associated rcParam in matplotlibrc.
* style: Either ‘normal’, ‘italic’ or ‘oblique’.
* variant: Either ‘normal’ or ‘small-caps’.
* stretch: A numeric value in the range 0-1000 or one of ‘ultra-condensed’, ‘extra-condensed’, ‘condensed’, ‘semi-condensed’, ‘normal’, ‘semi-expanded’, ‘expanded’, ‘extra-expanded’ or ‘ultra-expanded’
* weight: A numeric value in the range 0-1000 or one of ‘ultralight’, ‘light’, ‘normal’, ‘regular’, ‘book’, ‘medium’, ‘roman’, ‘semibold’, ‘demibold’, ‘demi’, ‘bold’, ‘heavy’, ‘extra bold’, ‘black’
* size: Either an relative value of ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’ or an absolute font size, e.g., 12

* byte variable to string, use .decode() method

```
b'abcde'.decode("utf-8")
'abcde'
```

# Matlibplot notes 
* fix, ax = plt.subplots(3, 2, figsize=(12, 4))
* plt.colorbar(pad=0.05, shrink=0.8)
* remove extra axes,
     ``` fig.delaxes(ax[-1])```

* get default colormap
```
plt.rcParams['axes.prop_cycle'].by_key()['color']
can get other cmap
plt.get_cmap('Set1', 20)
```

# Pandas

* delete a column or a
```
del data['aa']
data.drop([16 17])
data.drop([16 17], inplace=True)
```
* find index based on a condition
```
a = df[(df.BoolCol == 3) & (df.attr == 22)].index.tolist()
```

* find data based a condition
```
a = df[(df.BoolCol == 3) & (df.attr == 22)]
```

* return a row or column if know index
```
a = df.xs(2)  # return the row index 2
help(df.xs)

can also use

a = df.loc[2]  # return the second row
```

* use == just make a inference to original dataframe. to make a new copy, use 
```
df2 = df.copy()
```

* datafrom to ndarray

```
```