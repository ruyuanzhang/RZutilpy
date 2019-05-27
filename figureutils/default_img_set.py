def default_img_set():
    import matplotlib as mpl

    mpl.rcParams['interactive'] = True

    # figure
    mpl.rcParams['figure.frameon'] = False
    mpl.rcParams['figure.titleweight'] = 'regular'
    mpl.rcParams['figure.titlesize'] = 'xx-large'
    mpl.rcParams['figure.autolayout'] = True
    mpl.rcParams['figure.facecolor'] = 'w'
    mpl.rcParams['figure.edgecolor'] = 'None'
    mpl.rcParams['savefig.dpi'] = 300
    mpl.rcParams['savefig.frameon'] = False
    mpl.rcParams['savefig.format'] = 'pdf'
    mpl.rcParams['savefig.facecolor'] = 'None'
    mpl.rcParams['savefig.edgecolor'] = 'None'
    mpl.rcParams['savefig.bbox'] = 'tight'
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    # axes
    mpl.rcParams['axes.facecolor'] = 'None'
    mpl.rcParams['axes.labelweight'] = 'bold'
    mpl.rcParams['axes.labelsize'] = 'x-large'
    mpl.rcParams['axes.titleweight'] = 'regular'
    mpl.rcParams['axes.titlesize'] = 'xx-large'
    mpl.rcParams['axes.linewidth'] = 1
    mpl.rcParams['xtick.major.width'] = 1
    mpl.rcParams['xtick.major.size'] = 5
    mpl.rcParams['xtick.labelsize'] = 'large'
    mpl.rcParams['ytick.major.width'] = 1
    mpl.rcParams['ytick.major.size'] = 5
    mpl.rcParams['ytick.labelsize'] = 'large'
    mpl.rcParams['lines.linewidth'] = 2
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.top'] = False
    # Character
    mpl.rcParams['font.family'] = 'Arial'
    mpl.rcParams['font.weight'] = 'bold'
    # legend
    mpl.rcParams['legend.frameon'] = False

    # line
