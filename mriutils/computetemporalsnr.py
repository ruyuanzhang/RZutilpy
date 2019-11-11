def computetemporalsnr(vols=None,dim=-1):
    '''
    def [tsnr,mn,mad] = computetemporalsnr(vols,dim)

    <vols> is X x Y x ... x T with time-series along the last dimension (must be 2 or higher).
    <dim> (optional) is the dimension with time-series data. Default: -1 (the last dimension).

    return <tsnr> as a matrix of size X x Y x ... with the temporal SNR.
    also, return <mn> with the mean (of the original time-series).
    also, return <mad> with the median absolute difference (see below).

    The temporal SNR is defined as follows:
    1. first regress out a constant and a line from the time-series
    of each voxel.
    2. then compute the absolute value of the difference between each
    pair of successive time points (if there are N time points,
    there will be N-1 differences).
    3. compute the median absolute difference (mad).
    4. divide by the mean of the original time-series and multiply by 100.
    5. if any voxel had a negative mean, just return the temporal SNR as NaN.

    the purpose of the differencing of successive time points is to be relatively
    insensitive to actual activations (which tend to be slow), if they exist.

    if <vols> is None, we return None for all outputs.

    example:
    vols = getsamplebrain(4);
    [tsnr,mn,mad] = computetemporalsnr(vols);
    figure; imagesc(makeimagestack(mn));   caxis([0 2500]); axis image; colormap(gray); colorbar;
    figure; imagesc(makeimagestack(mad));  caxis([0 100]);  axis image; colormap(gray); colorbar;
    figure; imagesc(makeimagestack(tsnr)); caxis([0 5]);    axis image; colormap(jet);  colorbar;

    ======================== RZ notes =========================================

    History
        20180723 RZ created it based on computetemporalsnr.m

    '''
    from numpy import nan,diff,abs
    from RZutilpy.mri import detrendtimeseries

    # internal constants
    maxtsnrpolydeg = 1

    # do it
    if vols is None:
      tsnr = None
      mn = None
      mad = None
    else:
      mn = vols.mean(axis=dim)

      tmp = vols.reshape(prod(vol.shape[:-1]),vol.shape[-1])
      tmp_detrend, _, _ = detrendtimeseries(tmp.T).T
      mad = abs(diff(tmp_detrend, axis=-1)).median(axis=-1).reshape(*vol.shape[:-1])

      tsnr = mad / mn * 100
      tsnr[tsnr<=0] = np.nan

    return tsnr,mn,mad
