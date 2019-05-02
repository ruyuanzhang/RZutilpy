# This is a cheatsheet for tranlating utility function of knktuil and RZutil to python RZtuilpy


## colormap

## figure

## graphic

## imageprocessing

## indexing

## io
matchfiles - rz.io.matchfiles
## math
## matrix
in RZutilpy, we call this module array not matrix

* splitmatrix - np.split
* repmat - np.tile
## mri

* Some 3d volume manipulation

```
% performa a affline_transform and resample using spineline interpolation 
scipy.ndimage.affline_transform

% interpolation to get surface value from a volume value
scipy.ndimage.interpolate.map_coordinates

% smooth a volume
scipy.ndimage.gaussianfilter

% center of mass
scipy.ndimage.center_of_mass

% rotate and shift a volume
scipy.ndimage.interpolate.rotate
scipy.ndimage.interpolate.shift

```

## programming

## pt

## stats

## string
## timeseries 