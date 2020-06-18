# -*- coding: utf-8 -*-
"""
RZutilpy figure module

@author: ruyuan
"""

'''
default_img_set()
plot()
regplot()
colormap()
colorinterp()
cmapang()
drawcolorbarcircular()

'''

# default_img_set()
from .figureutils import default_img_set
default_img_set = default_img_set.default_img_set

# plot
from .figureutils import plot
plot = plot.plot
#import matplotlib.pyplot as plt
#plt.plot = plot.plot

from .figureutils import bar
bar = bar.bar

from .figureutils import bar2
bar2 = bar2.bar2

# regplot
from .figureutils import regplot
regplot = regplot.regplot

# colormap
from .figureutils import colormap
colormap = colormap.colormap

# getdefaultcolorlist
from .figureutils import getdefaultcolorlist
getdefaultcolorlist = getdefaultcolorlist.getdefaultcolorlist

# colorinterp
from .figureutils import colorinterp
colorinterp = colorinterp.colorinterp

# cmapang
from .figureutils import cmapang
cmapang = cmapang.cmapang

# cmapang2
from .figureutils import cmapang2
cmapang2 = cmapang2.cmapang2

# cmapang3
from .figureutils import cmapret
cmapret = cmapret.cmapret

# drawcolorbarcircular
from .figureutils import drawcolorbarcircular
drawcolorbarcircular = drawcolorbarcircular.drawcolorbarcircular

from .figureutils import drawcolorbarhalfcircular
drawcolorbarhalfcircular = drawcolorbarhalfcircular.drawcolorbarhalfcircular

# show_images
from .figureutils import show_images
show_images = show_images.show_images

# add more color palettable  
from .figureutils import colorpalettable
colorpalettable = colorpalettable.colorpalettable




