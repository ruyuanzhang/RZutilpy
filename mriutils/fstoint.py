def fstoint(x):
    # function x = fstoint(x)
    #
    # <x> is a 3D volume, numpy array
    #
    # Perform various flips and permutations to go from
    # FreeSurfer space to our internal MATLAB space.

    from numpy import flip
    return flip(flip(x.transponse([0, 2, 1]), axis=2), axis=0)
