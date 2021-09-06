#  RZ' stats

from .statsutils import localregression3d
localregression3d = localregression3d.localregression3d

from .statsutils import booterrorbar
booterrorbar = booterrorbar.booterrorbar

from .statsutils import bootresamplemulti
bootresamplemulti = bootresamplemulti.bootresamplemulti

from .statsutils import sem
sem = sem.sem

from .statsutils import cohend
cohend = cohend.cohend

from .statsutils import hedgeg
hedgeg = hedgeg.hedgeg

from .statsutils import ttest
ttest = ttest.ttest


# == fit polymial ==
from .statsutils import polyfit1d
polyfit1d = polyfit1d.polyfit1d

from .statsutils import polyfit2d
polyfit2d = polyfit2d.polyfit2d

from .statsutils import polyfit3d
polyfit3d = polyfit3d.polyfit3d

# == local regression ===
from .statsutils import localregression3d
localregression3d = localregression3d.localregression3d

from .statsutils import rzSVC
rzSVC = rzSVC.rzSVC

# unique model fitting module
from .statsutils import fitnonlinearmodel
fitnonlinearmodel = fitnonlinearmodel.fitnonlinearmodel
