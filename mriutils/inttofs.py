def inttofs(x):
    # def x = inttofs(x):
    #
    # <x> is a 3D volume, numpy ary
    #
    # Perform various flips and permutations to go from
    # our internal MATLAB space to FreeSurfer space.
    from numpy import flip
    return (flip(flip(x, axis=0), axis=2)).tranpose([0, 2, 1])
