def mod2(x, y):
    # return y if mod(x,y)==0
    f = x % y
    f[f==0] = y
    return
    f