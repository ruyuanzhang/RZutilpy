# other notes
* A good explanation of decorator in python
[decorator in python](https://www.zhihu.com/question/26930016)
* [explanation](https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386820023084e5263fe54fde4e4e8616597058cc4ba1000) for

```
from __future__ import
```
* generator explanation?

# configure python and ipython
* Once Anoconda is properly installed, go to user home directory 
```
cd ~/.ipython/profile_default
nano scientific_startup.py
```
* all relevant configration will be in ~/.ipython/profile_default/ipython_config.py
* in ipython_config.py, we set the scientific_startup.py as the startup running file for ipython
* to reload externally import module and function

```
# from module X import function Y, if you edit Y, ipython will not reload function Y
import sys
sys.path.append(r'X.py')
from X import Y

# can use magic cmd %aimport
import sys
sys.path.append(r'X.py')
%aimport X
from X import Y

```

* Run a script but keep varible in name space. You can do in ipython
```
run -i test.py
```


# path
* We know use rzpath object, which is a modified wrapper of path-lib object, you can do like
* 
```
from RZutilpy.system import Path
```

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

* the use of pathlib.path object

```
from pathlib import Path

print(Path.home())  # 用户目录
cwd = Path.cwd()    # 当前目录
print(cwd)

full_name = Path(__file__)   # 当前文件名
print(full_name)
print(full_name.suffix)     # 文件后缀
print(full_name.stem)   # 文件名不带后缀
print(full_name.name)   # 带后缀的完整文件名
print(full_name.parent)     # 路径的上级目录
print(full_name.is_dir())   # 判断是否是目录
print(full_name.resolve())  # 返回绝对路径
print(full_name.exists())       # 路径是否存在
print(full_name.root)       # 返回路径的根目录
print(full_name.parts)  # 分割路径 类似os.path.split(), 不过返回元组
print(full_name.stat())     # 返回路径信息, 同os.stat()

# note that for any input str, please first do expanduser() then do resolve() to covert it to an obsoluate path, otherwise will be problem

b = Path('pathtofile').expanduser().resolve()
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

* boolean and bitwise operateion

```
If you are not dealing with arrays and are not performing math manipulations of integers, you probably want and.

If you have vectors of truth values that you wish to combine, use numpy with  &
```

# Object-related proproraming

* 实例方法只能被实例对象调用，静态方法(由@staticmethod装饰的方法)、类方法(由@classmethod装饰的方法)，可以被类或类的实例对象调用。
	* 实例方法，第一个参数必须要默认传实例对象，一般习惯用self。
	* 静态方法，参数没有要求。
	* 类方法，第一个参数必须要默认传类，一般习惯用cls。
* given a object, get its parent class

```
import inspect
a = Path('~')
parent = inspect.getmro(type(a)) # will return a tuple
# you can directly use it 
b = parent[1]('~')
```

# conda skills
* save conda environment file

```
# on mac and linux
source activate envname
conda env export -n base --no-builds> rzutilpy.yml

```
But based on what I tried (i.e., try to immigrate the whole python enviroment setting from Macpro to linux), this functionality is not that useful. It only works from within-platform immigration of an conda environment....

* update the conda envrioment file

```
# on mac and linux
conda env update -f rzutilpy.yml
```

* python parallel computer is disappoting, now we have

```
# multipocessing
# this is good and I think efficient but this module use pickle and many functions cannot be pickled

# pathos
# which is a branch of pathos and follows the same logic, but I cannot make it work on my computer

# ipyparrallel
# which is new and avoids the pickle problem, but it requires the configuration profile. Not sure how to set it up

``` 

# Numpy specific 
* Some times use map/zip/list together
* Note the difference between np.stack and np.concatenate
	- concatenate cannot create a new axis, but faster than stack
	- stack always create a new axis
* repmat = np.tile
* permute = np.transpose
* squeeze = np.squeeze or a.squeeze() 
* matlab find = np.where
* np.sum can directly input boolean data type and count how many true
* sprintf = % but can also use format or f"" instead
* cell2mat = np.block
* sort = np.sort (return sorted arr), np.argsort (return index)


```
'xxxx%02dxxx' % a
'xxxx%02dxxx%s' % (a, b) 

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

* y in ys
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

* sort

* 返回view的情况

```
# 最主要是numpy
b = a.reshape
b = a.T
# list append一个view也不行
a = np.arange(10)
b = []
b.append(a)
a[1] = 1000
print(b)  # 这时候b也会改变，因为append的是一个view

# 不用担心view
b = a  # when a is a scalar
a = a.reshape  # 自己改变自己
a = a.T  #自己改变自己
b = a.max() # 计算一个值
```

* numpy 100题

```
# note here
print(sum(range(5),-1))
from numpy import *
print(sum(range(5),-1))

#
print(0.3 == 3 * 0.1)  # False

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

* modify properties of LineCollection, can use functions like
get_color, get_color, set_color, get_linestyle

* fix, ax = plt.subplots(3, 2, figsize=(12, 4))
* plt.colorbar(pad=0.05, shrink=0.8)
* get default colormap

```
plt.rcParams['axes.prop_cycle'].by_key()['color']
can get other cmap
plt.get_cmap('Set1', 20)
```

* switch current figures. Useful when using pure command line tool to perform computation on server

```
f1 = plt.figure()
f2 = plt.figure()
# switch to f1
plt.figure(f1.number)
```


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

* ''.replace(old,new)

* fstring format
```
f'{a:.2f}'
```

# Pandas
* read a file
```
pd.read
```

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

* dataframe to ndarray
df.values


#  regular expression

* for escape sequences(转义字符), like '\d+', we should use a r prefix

```
p = re.compile(r'\d+')
m = p.match('heihei123')
```

* use () to add token

```
text = 'FOV 140*320'
p = re.compile(r'^(\d{1,4})p\*(\d{1,4})s$')
matchgroup = p.match(text)
plines = int(matchgroup.group(1))  # step in phase encoding direction
flines = int(matchgroup.group(2))  # step in frequency encoding direction
= [plines, flines]
```


#  compatibility, debug
* (last updated 20180618) Mayavi2 is released on May 27, 2018. This new mayavi toolkit fully support python3. The current release includes mayavi 4.6, vtk 8.1

* (last updated 20180618) Psychpy 1.9.0 is now released and this is a major release aiming for supporting python 3. Be careful, current version requires pyglet 1.3.0. It will report error suin pyglet 1.3.2 ()


* Pysurfer. Pysurfer requires support from mayavi. Since the new version mayavi was just released, it might take some time for pysurfer people to catch up.

* afni, brainvoyager, current afni only support python 2, not python 3.

* Pycortex, not sure how it uses, crappy software...