def videotoimagesequence(videofile, filenamepattern, fps=None):
    '''
    videotoimagesequence(videofile, filenamepattern, fps=None):

    Read a video file and write it as a image sequence.

    Input:
        <videofile>: a str, the videofilename
        <imagenamepattern>: A filename specifying the numerotation format and
            extension of the pictures. For instance “frame%03d.png” for filenames
            indexed with 3 digits and PNG format. Also possible: “some_folder/frame%04d.jpeg”,
            etc.
        <fps>: fps for images. Default is the video's fps

    Output:
        a moviepy clip object
    '''

    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(videofile)
    clip.write_images_sequence(filenamepattern, fps=fps)
    return clip

