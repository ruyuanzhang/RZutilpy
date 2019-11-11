def cmapret(name='lh', ref=None):
    '''
    angular colormap from HCP retinotopic data set
    default output left namesphere

    <lh>,<rh>: angular cmap for left and right hemisphere
    <ecc>: eccentricity cmap
    <size>: pRF size cmap

    For <lh>,<rh>, we create 360 colors, for <ecc>,<size>, we create 256 colors
    '''

    from RZutilpy.figure import colormap
    from scipy.interpolate import interp1d
    import numpy as np

    ref_angs = np.array([-3.14159, -2.35619, -1.5708, -0.785398, 0, 0.785398, \
        1.5708, 2.35619, 3.14159])

    if name.lower()=='lh':
        cmap = np.array([0.666667, 0., 0.666667, \
                1., 0.333333, 0.666667, \
                0.666667, 0., 0., \
                1., 1., 0.333333, \
                0., 0.666667, 0., \
                0.333333, 1., 1., \
                0., 0., 0.666667, \
                0.666667, 0.333333, 1.,
                0.666667, 0., 0.666667]).reshape(9,3)
        fill_value = [0.666667, 0., 0.666667]
        angs = np.arange(360)
        temp = angs / 180 * np.pi
        temp[temp > np.pi] = temp[temp > np.pi] - 2 * np.pi

        finalcmap = np.empty((360, 3))
        finalcmap[:, 0] = interp1d(ref_angs, cmap[:, 0], bounds_error=False, fill_value=fill_value[0])(temp)
        finalcmap[:, 1] = interp1d(ref_angs, cmap[:, 1], bounds_error=False, fill_value=fill_value[1])(temp)
        finalcmap[:, 2] = interp1d(ref_angs, cmap[:, 2], bounds_error=False, fill_value=fill_value[2])(temp)

        return colormap(finalcmap, 360, keeplast=True)

    elif name.lower()=='rh':
        cmap = np.array([0., 0.666667, 0.,
                1., 1., 0.333333,
                0.666667, 0., 0.,
                1., 0.333333, 0.666667,
                0.666667, 0., 0.666667,
                0.666667, 0.333333, 1.,
                0., 0., 0.666667,
                0.333333, 1., 1.,
                0., 0.666667, 0.]).reshape(9,3)

        fill_value = [0, 0.666667, 0.]
        angs = np.arange(360)
        temp = angs / 180 * np.pi
        temp[temp > np.pi] = temp[temp > np.pi] - 2 * np.pi

        finalcmap = np.empty((360, 3))
        finalcmap[:, 0] = interp1d(ref_angs, cmap[:, 0], bounds_error=False, fill_value=fill_value[0])(temp)
        finalcmap[:, 1] = interp1d(ref_angs, cmap[:, 1], bounds_error=False, fill_value=fill_value[1])(temp)
        finalcmap[:, 2] = interp1d(ref_angs, cmap[:, 2], bounds_error=False, fill_value=fill_value[2])(temp)

        return colormap(finalcmap, 360, keeplast=True)

    elif name.lower()=='ecc':
        ref = np.array([0, 1.5, 3, 6, 12, 24, 48, 90]) if ref is None else ref
        cmap = np.array([0.,  0.,  0.666667,
                1.,  0.333333,    1.,
                0.666667,    0.,  0.,
                1.,  1.,  0.333333,
                0.,  0.666667,    0.,
                0.333333, 1., 1.,
                0.333333, 0.333333, 0.333333,
                1.,  1.,  1.])

        finalcmap = np.empty((256, 3))
        finalcmap[:, 0] = interp1d(ref, cmap[:, 0])(temp)
        finalcmap[:, 1] = interp1d(ref, cmap[:, 1])(temp)
        finalcmap[:, 2] = interp1d(ref, cmap[:, 2])(temp)

        return colormap(finalcmap, 256, keeplast=True)

    elif name.lower()=='size':
        ref = np.array([0, 0.375, 0.75, 1.5, 3, 6, 12, 22.5]) if ref is None else ref
        cmap = np.array([0.,  0.,  0.666667,
                1.,  0.333333,   1.,
                0.666667,    0.,  0.,
                1.,  1.,  0.333333,
                0.,  0.666667,    0.,
                0.333333,    1.,  1.,
                0.333333,    0.333333, 0.333333,
                1.,  1.,  1.])

        finalcmap = np.empty((256, 3))
        finalcmap[:, 0] = interp1d(ref, cmap[:, 0])(temp)
        finalcmap[:, 1] = interp1d(ref, cmap[:, 1])(temp)
        finalcmap[:, 2] = interp1d(ref, cmap[:, 2])(temp)

        return colormap(finalcmap, 256, keeplast=True)
