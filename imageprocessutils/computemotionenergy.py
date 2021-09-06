# the functinon to calculate orientation energy
def computemotionenergy(img, spatempfilter, stride):
    '''
    calculate orientation energy of an image based on a set of gabor filters.

    <img>: Input image can be numpy array or tensor, 
        is a (batch_size, c, T, H, W), Note that input image is 'uint8' dtype and range (0, 256)
    <spatempfilter>: 
        the object returned by makemultiscalespatiotemporalfilters function
    <stride>: int, stride as number of pixels along the spatial domain


    Note:
        1. We typically set the stride as 1 in the temporal domain
    '''
    
    import torch
    from torch.nn.functional import conv3d
    from torch import Tensor, from_numpy # to use conv3d function, it must be converted to tensor
    from numpy import array, transpose, newaxis, round, sqrt
    
    # convert img to tensor
    is_tensor = False
    if isinstance(img, Tensor):
        is_tensor = True
    else: # convert it as tensor
        img = from_numpy(img).type(torch.float)

    img = img / 256 # convert to (0~1)
    imgSize, imgLen = img.shape[3], img.shape[2]  # assume square image

    if isinstance(stride, int):
        stride=[stride] 
    
    gbr, sd, tf = spatempfilter['gabor'], spatempfilter['sd'], spatempfilter['TF']
    
    filteredimg = []
    for igbr, vgbr in enumerate(gbr): # loop each spatial and temporal scale
        # reformat the filter
        gbrtmp = vgbr
        gbrtmp = transpose(gbrtmp, [3, 2, 0, 1]) # (out_channels, kT, kH, kW)
        gbrtmp = gbrtmp[:, newaxis, :, :, :]  # (out_channels, 1, kT, kH, kW)
        gbrtmp = from_numpy(gbrtmp).type(torch.float) # convert it to torch
        ksize = gbrtmp.shape[3] # assume square kernel
        tsize = gbrtmp.shape[2]
        nKernel = gbrtmp.shape[0]
        # now gbrtmp is a [outchannel, group, T, H, W], as standard input for conv3d

        # calculate stride and padding
        stride_tmp = int(round(stride[igbr]))
        spadding = int(ksize / 2 - imgSize % stride_tmp / 2)
        tpadding = int((tsize-1)/2)

        # convolve
        # output a is a [batch_size, Cout, Tout, Hout, Wout]
        a = conv3d(img, gbrtmp, stride=(
            1, stride_tmp, stride_tmp), padding=(tpadding, spadding, spadding))

        #a = torch.squeeze(a)
        # assume 0:Cout/2 and Cout/2+1: are different phase,
        
        # transform quadradic pair of simple cells to complex cells
        a = sqrt(a[:, :int(nKernel/2), :, :, :]**2 + a[:, int(nKernel/2):, :, :, :]**2)
        
        if is_tensor:
            filteredimg.append(a.view(a.shape[0], a.shape[1], a.shape[2] - 1))
        else:
            a = array(a)  # convert it back to numpy array
            filteredimg.append(a.reshape(a.shape[0], a.shape[1], a.shape[2], -1))
    # flatten it as a vector
    return filteredimg
