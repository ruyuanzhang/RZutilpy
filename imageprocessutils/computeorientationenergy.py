# the functinon to calculate orientation energy
def computeorientationenergy(img, gaborfilter, stride):
    '''
    calculate orientation energy of an image based on a set of gabor filters.

    <img>: Input image can be numpy array or tensor, is a (batch_size, c, H, W), 
        Note that input image is 'uint8' dtype and range (0, 256)
    <gaborfilter>: 
        the object returned by makemultiscalegaborfilters function
    <stride>: int, stride as number of pixels
    '''
    import torch
    from torch.nn.functional import conv2d
    from torch import Tensor, from_numpy # to use cov2d function, it must be converted to tensor
    from numpy import array, transpose, newaxis, round, sqrt
    
    # convert img to tensor
    is_tensor = False
    if isinstance(img, Tensor):
        is_tensor = True
    else: # convert it as tensor
        img = from_numpy(img).type(torch.float)

    img = img / 256
    imgSize = img.shape[2] # assume square image 
    
    gbr, sd = gaborfilter['gabor'], gaborfilter['sd']
    
    filteredimg = []
    for iSd, vSd in enumerate(sd): # loop each scale
        # reformat the filter
        gbrtmp = gbr[iSd]
        gbrtmp = transpose(gbrtmp, [2, 0, 1]) # (out_channels, kH, kW)
        gbrtmp = gbrtmp[:, newaxis, :, :]  # (out_channels, 1, kH, kW)
        gbrtmp = from_numpy(gbrtmp).type(torch.float) # convert it to torch
        ksize = gbrtmp.shape[2] # assume square kernel
        nKernel = gbrtmp.shape[0]
        # now gbrtmp is a [outchannel, group, H, W], as standard input for conv2d

        # calculate stride and padding
        stride_tmp = int(round(stride[iSd]))
        padding = int(ksize / 2 - imgSize % stride_tmp / 2)

        # convolve
        # output a is a [batch_size, Cout, Hout, Wout]
        a = conv2d(img, gbrtmp, stride=stride_tmp, padding=padding)

        #a = torch.squeeze(a)
        # assume 0:Cout/2 and Cout/2+1: are different phase,
        
        # transform quadradic pair of simple cells to complex cells
        a = sqrt(a[:, :int(nKernel/2), :, :]**2 + a[:, int(nKernel/2):, :, :]**2)
        
        if is_tensor:
            filteredimg.append(a.view(a.shape[0], a.shape[1], -1))
        else:
            a = array(a)  # convert it back to numpy array
            filteredimg.append(a.reshape(a.shape[0], a.shape[1], -1))
    # flatten it as a vector
    return filteredimg
