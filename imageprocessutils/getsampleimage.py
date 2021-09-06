def getsampleimage(imgnum):
    '''
    Get a sample image for image processing
    <imgnum>: int
    '''
    from cv2 import imread
    from RZutilpy.system import Path
    from RZutilpy import imageprocess

    # get the image path
    pic = Path(imageprocess.__file__)
    pic = pic.parent / 'imageprocessutils' / f'getsampleimage{imgnum}.png'
    return imread(pic.str)
