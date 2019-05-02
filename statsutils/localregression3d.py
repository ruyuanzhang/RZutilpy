def localregression3d(x, y, z, w, x0, y0, z0, degree=1, kernal='epan', h=None, wts=None, mode=0):
    '''
    localregression3d(x, y, z, w, x0, y0, z0, degree, kernal, h, wts, mode):

    Input:
        <x>,<y>,<z>,<w> are matrices of the same size with the data
        <x0>,<y0>,<z0> are matrices of the same size with the points to evaluate at
        <degree> (optional) is degree of polymonial fit, default=1
        <kernel> (optional) is 'epan'.  default: 'epan'.
        <h> (optional) is the bandwidth [xb yb zb].  values can be Inf.
            can be a scalar in which case we use that for all three dimensions.
            default: [std(x(:)) std(y(:)) std(z(:))]/10.
        <wts> (optional) is a matrix the same size as <w> with non-negative numbers.
            these are weights that are applied to the local regression in order to
            allow certain points to have more influence than others.  note that
            the weights enter the regression in exactly the same way as the kernel
            weights.  default: ones(size(<w>)).
        <mode> (optional) is
            0 means normal
            1 means that <x>,<y>,<z> are generated from ndgrid(1:nx,1:ny,1:nz)
            and that <w> and <wts> are matrices of the same size as <x>,<y>,<z>.
            we require that there be no NaNs in <w> and <wts>.
            the point of this mode is to speed up execution.
            default: 0.
    Output:
        return a matrix with the value of the function at <x0>,<y0>,<z0>.

    singular warnings are suppressed.  can return NaNs.
    note that entries with NaN in <x>, <y>, <z>, or <w> are ignored.

    note that we use pathos.multiprocessing.Pool as a way to potentially speed up execution.
    if parallelization is used, note that status dots are outputted only at the end.

    If <mode>==0, we use sklearn.neighbors NearestNeighbors

    Example:
        x = np.random.randn(1,1000)
        y = np.random.randn(1,1000)
        z = np.random.randn(1,1000)
        w = np.sin(x) + np.cos(y) + np.tan(z) + .2*np.random.randn(x.size)
        [x0,y0,z0] = np.mgrid(-1:.1:1)
        w0 = localregression3d(x,y,z,w,x0.flatten(),y0.flatten(),z0.flatten())
        w0actual = (sin(x0) + cos(y0) + tan(z0)).flatten()
        plt.figure()
        plt.scatter(w0,w0actual,'r.')
        plt.xlabel('local regression fit');
        plt.ylabel('true values')

    History:
        20180720
        20180628 RZ created it

    To do:
        -implement asymmetric kernel in mode==0
    '''

    from numpy import ndarray, array, ones, isscalar, isnan, ceil, floor, arange,\
    zeros, stack, nan

    from pathos.multiprocessing import Pool
    from RZutilpy.stats import polyfit3d

    # we assume x,y,z,w,x0,y0,z0 are all ndarray
    assert isinstance(x, ndarray) and isinstance(y, ndarray) and isinstance(z, ndarray) \
    and isinstance(w, ndarray) and isinstance(x0, ndarray) and isinstance(y0, ndarray) \
    and isinstance(z0, ndarray), 'x,y,z,w,x0,y0,z0 must be ndarray!'

    # set default value
    if h is None:
        h = array([x.std(), y.std(), z.std()]) / 10
    if wts is None:
        wts = ones(x.size)
        wtsopt = True
    else:
        wtsopt = False

    if isscalar(h):
        h = array([h, h, h])

    # prep
    if mode == 0: # normal case
        x = x.flatten()
        y = y.flatten()
        z = z.flatten()
        wts = wts.flatten()
        # remove nan
        bad = isnan(x) | isnan(y) | isnan(z) | isnan(w) | isnan(wts)
        x = x[~bad]
        y = y[~bad]
        z = z[~bad]
        wts = wts[~bad]
    elif mode == 1:
        nx = x.size
        ny = y.size
        nz = z.size

    # find nearest neighbor of each dot in [x0,y0,z0] in [x,y,z]
    if mode == 0: # more general case
        # we use sklearn utility to find nearest neighbors, note that this might be slow...
        from sklearn.neighbors import NearestNeighbors
        neigh = NearestNeighbors()  # default distance 1
        neigh.fit(stack((x,y,z), axis=-1)) # in this case we first fit to the x, y, z

    def localregression3d_helper(_x, _y, _z):
        # here _x, _y, _z represents a single dot in x0,y0,z0 array

        if mode == 0: # more general case
            # find the nearest neighbor
            # note that currently we only find the nearest neighbor in a symmetric sphere,
            # namely same bandwidth in three direction.
            dist, nbrs = neigh.radius_neighbors(array([_x, _y, _z]).reshape(1,-1), radius=h[0])
            # note that this dist is eucelidean distance
            dist = dist[0]  #strip array since we only have one reference point
            nbrs = nbrs[0]
            k = 0.75 * (1 - dist**2 / h[0]**2)  # weight based on dist, this is similar to KK's localregression3d.m

            # get out early
            if nbrs.size==0:
                return

            # filter out
            xA = x[nbrs]
            yA = y[nbrs]
            zA = z[nbrs]
            wA = w[nbrs]
            wtsA = ones(xA.size) if wtsopt else wts[ix]
            n = xA.size

        elif mode == 1:  # ngrid case
            # for ngrid case, no need to use nearest neighbour
            indices = [arange(max(1, ceil(_x-h[0])), min(nx, floor(_x+h[0]))), \
            arange(max(1, ceil(_y-h[1])), min(ny, floor(_y+h[1]))),\
            arange(max(1, ceil(_z-h[2])), min(nz, floor(_z+h[2])))]
            ix = np.zeros((nx, ny, nz)).astype('boolean')
            ix[indices[0], indices[1], indices[2]] = True
            ix = ix.flatten()

            # calculate the L2 distance, note that we do not take the square root
            dist = ((indices[0]-_x)/h[0]) ** 2 + ((indices[1]-_y)/h[1]) ** 2 + ((indices[2]-_z)/h[2]) ** 2
            k = 0.75 * (1-dist)
            k[k < 0] = 0

            # get out early
            if not ix:
                return

            # filter out
            xA, yA, zA = meshgrid(indices[0], indices[1], indices[2])
            xA = xA.flatten()
            yA = yA.flatten()
            zA = zA.flatten()
            wA = w[ix]
            wtsA = ones(xA.size) if wtsopt else wts[ix]
            n = xA.size

        # after get the neighbor and calcuate the weight, we do the regression

        # polyfit
        k = k * wtsA  # distance-dependent weight multiple the input weight
        coef, _, _, _ = polyfit3d(xA, yA, zA, wA, deg=degree, grid=False, weight=k)
        return  array([1, _x, _y, _z]) @ coef # be careful here

    # for debugging purpose
    f = nan * zeros(x0.shape).flatten()
    cnt = 0
    for i, _x, _y, _z in zip(x0,y0,z0):
        print('{}{}{}'.format(_x,_y,_z))
        f[cnt] = localregression3d_helper(_x, _y, _z)
        cnt += 1


    # print('localregression3d')
    # if __name__ == '__main__':
    #     with Pool() as p:
    #         f = p.imap(localregression3d_helper, zip(x0, y0, z0))
    # print('done.\n')

    return array(f)


