def defineellipse3d(arr, wantnorm=True, wantfit=False, mn=(0.5, 0.5, 0.5), sd=(0.2, 0.2, 0.2)):
    '''
    defineellipse3d(arr, wantnorm=True, wantfit=False, mn=(0.5, 0.5, 0.5), sd=(0.2, 0.2, 0.2)):

    define an ellipse in 3d space

    Input:
        <m> is a 3D volume
        <wantnorm> (optional) is whether to contrast-normalize
            <m> for display purposes.  default: True.
        <wantfit> (optional) is whether to obtain an initial position
            and size by fitting a 3D Gaussian to <m>.  default: False.
        <mn>,<sd> (optional) are the initial position and size to use.
            if supplied, then we ignore <wantfit>.  if not supplied
            and not <wantfit>, then we use a default position and size.

    To do:
        1. complete the wantfit function

    History:
        20180424 RZ created it, did not implement wantfit function

    '''
    from numpy import percentile, min, linspace, round
    from RZutilpy.math import normalizerange
    from RZutilpy.imageprocess import makegaussian3d, makeimagestack
    import matplotlib.pyplot as plt
    import tkinter as tk

    # check input



    # set some internal constraints
    mul = 5     # what factor does the shift key apply?
    step = .02  # what is the initial step size?
    pct = 1     # percentile for normalization
    state = 2   # see below
    mix = .5    # amount of ball to mix
    ss = 20     # low-resolution for fitting
    mndefault = [.5, .5, .5]
    sddefault = [.2, .2, .2]
    maxslices = 25  # maximum number of slices to show

    # normalize volume range
    if wantnorm:
        rng = percentile(arr.flatten(), [pct, 100-pct])
        arr = normalizerange(arr,0, 1, rng[0], rng[1])

    # define initial seed, Now we pass...
    if mn is None:
        pass
    elif wantfit:
        pass
    else:
        mn = mndefault
        sd = sdadefault

    # prep
    doupdate = True
    mmx = arr.max()
    mmn = arr.min()
    mrng = arr.ptp()
    mmx = mmx + mrng / 2
    mmn = mmn - mrng / 2
    slice_toshow = round(linspace(0, arr.shape[2] - 1, min((arr.shape[2], maxslices)))).astype('int')

    # do it
    figobj = plt.figure()
    axesimg = None
    while True:
        if doupdate:
            print(mn)
            print(sd)
            # make the ball volume
            ball, xx, yy, zz = makegaussian3d(arr.shape, mn, sd)
            ball = ball > 0.5  # binarize the ball

            # make the weighted volume..
            if state == 0:
                wvol = (1 - ball) * arr
            elif state == 1:
                wvol = arr
                wvol[ball] = mmn * mix + wvol[ball] * (1 - mix)
            elif state == 2:
                wvol = arr
                wvol[ball] = mmx * mix + wvol[ball] * (1 - mix)
            elif state == 3:
                wvol = ball * arr

            # show it
            if axesimg is None:
                axesimg = plt.imshow(makeimagestack(wvol[:, :, slice_toshow]), cmap='gray')
            else:
                axesimg.set_data(makeimagestack(wvol[:, :, slice_toshow]))
                plt.draw()



            # wait for response
            key = input()
            doupdate = 1

            if key:
                # control without multiplication
                if key[0] == 'w':
                    mn[0] = mn[0] - step
                elif key[0] == 's':
                    mn[0] = mn[0] + step
                elif key[0] == 'a':
                    mn[1] = mn[1] - step
                elif key[0] == 'd':
                    mn[1] = mn[1] + step
                elif key[0] == 'q':
                    mn[2] = mn[2] - step
                elif key[0] == 'e':
                    mn[2] = mn[2] + step
                elif key[0] == 'i':
                    sd[0] = sd[0] - step
                elif key[0] == 'k':
                    sd[0] = sd[0] + step
                elif key[0] == 'j':
                    sd[1] = sd[1] - step
                elif key[0] == 'l':
                    sd[1] = sd[1] + step
                elif key[0] == 'u':
                    sd[2] = sd[2] - step
                elif key[0] == 'o':
                    sd[2] = sd[2] + step

                # uppercase, use multiplication
                elif key[0] == 'W':
                    mn[0] = mn[0] - mul * step
                elif key[0] == 'S':
                    mn[0] = mn[0] + mul * step
                elif key[0] == 'A':
                    mn[1] = mn[1] - mul * step
                elif key[0] == 'D':
                    mn[1] = mn[1] + mul * step
                elif key[0] == 'Q':
                    mn[2] = mn[2] - mul * step
                elif key[0] == 'E':
                    mn[2] = mn[2] + mul * step
                elif key[0] == 'I':
                    sd[0] = sd[0] - mul * step
                elif key[0] == 'K':
                    sd[0] = sd[0] + mul * step
                elif key[0] == 'J':
                    sd[1] = sd[1] - mul * step
                elif key[0] == 'L':
                    sd[1] = sd[1] + mul * step
                elif key[0] == 'U':
                    sd[2] = sd[2] - mul * step
                elif key[0] == 'O':
                    sd[2] = sd[2] + mul * step

                elif key[0] == ',':
                    state = mod(state + 1,4)
                elif key[0] == '-':
                    step = step / 2
                    doupdate = 0
                elif key[0] == '+':
                    step = step * 2
                    doupdate = 0
                elif key[0] == '0':
                    mn = mndefault
                    sd = sddefault
                elif key[0] == '0':
                    break

    print('mn = {}\n'.format(mn))
    print('sd = {}\n'.format(sd))

    return ball, mn, sd









