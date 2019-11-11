def show_images(images, cols=0):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 0): Number of columns in figure (number of rows is
                        set to np.ceil(n_images/float(cols))). Default 0 indicate
                        to arrange image in a square grid
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # define rows and col
    n_images = len(images)
    if cols == 0:
        cols = int(np.ceil(np.sqrt(n_images)))
    rows = int(np.ceil(n_images / float(cols)))

    fig, ax = plt.subplots(rows, cols)
    ax = ax.flatten()
    np.delete(ax, np.arange(n_images, cols * rows + 1))

    for n, image in enumerate(images):
        if image.ndim == 2:
            plt.sca(ax[n])
            plt.gray()
            ax[n].imshow(image)
            ax[n].axis('off')

    plt.show()
    # fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)

    # remove all white space
    return fig, ax