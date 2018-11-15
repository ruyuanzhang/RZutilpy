def calcsapvael(vertices, faces, wantsapv=True, wantael=True):
    '''
    def calcsapvael(vertices,faces,sapv=True,ael=True):

    calculate surface area per vertex <sapv> and average edge length <ael> for all
    input vertices

    Input:
        <vertices>: vertices array (nVerts, 3)
        <faces>: faces array (nFaces, 3)
        <wantsapv>: bool, want to calculate sapv, default:True
        <wantael>: bool, want to calculate ael, default:True
    Output:
        <sapv>: 1d (nVerts,) array
        <ael>: 1d (nVerts,) array

    at least <wantsapv> or <wantael> should be true.

    if both <wantsapv> and <wantael> are true, we return (sapv, ael). Otherwise only
    return <sapv> or <ael>

    # can test this speed
    from time import time
    t = time()
    sapv = rz.mri.calcsapvael(verts,faces,wantael=False)
    print(time()-t)

    History:
        20180717 RZ test the speed, for a surface with 160000 vertices, it take
            ~250s(so slow..). RZ also confirm the this function output correct values
            by comparing results to vertex_area.m and vertex_neighbour_distance.m
        20180714 RZ created it

    To do:
        1. maybe test the speed??
        2. use parallel computing??
    '''
    from pathos.multiprocessing import Pool
    from numpy import where, any, sqrt, abs, array, unique
    from time import time

    # check input
    assert wantsapv is True or wantael is True, 'at least you want to compute sapv or ael'

    def sapvael(i_vert):
        '''
        <i_vert> is the vertex index, start from 0
        '''
        thisvert = vertices[i_vert, :]
        # find the faces that contain this vertices

        faces_surnd_idx = where(any(faces == i_vert, axis=1))[0] # here can use reduce??
        faces_surnd = faces[faces_surnd_idx, :]
        vertices_surnd_idx = unique(faces_surnd.flatten()[(faces_surnd != i_vert).flatten()])
        vertices_surnd = vertices[vertices_surnd_idx, :]

        # calculate the ael
        if wantael:
            ael_thisvert = (sqrt(\
                (vertices_surnd[:,0] - thisvert[0]) ** 2 + \
                (vertices_surnd[:,1] - thisvert[1]) ** 2 + \
                (vertices_surnd[:,2] - thisvert[2]) ** 2)).mean()

        # calculate the face area, for each face, assume vertex A,B,C
        # the face area is the vecto
        if wantsapv:
            # compute three edges
            el1 = sqrt(((vertices[faces_surnd[:,0],:] - vertices[faces_surnd[:,1],:]) ** 2).sum(axis=1))
            el2 = sqrt(((vertices[faces_surnd[:,1],:] - vertices[faces_surnd[:,2],:]) ** 2).sum(axis=1))
            el3 = sqrt(((vertices[faces_surnd[:,2],:] - vertices[faces_surnd[:,0],:]) ** 2).sum(axis=1))
            s = (el1 + el2 + el3) / 2
            sapv_thisvert = sqrt(s*(s-el1)*(s-el2)*(s-el3)).mean()

        if wantsapv and wantael:
            return sapv_thisvert, ael_thisvert
        elif not wantsapv and wantael:
            return ael_thisvert
        elif wantsapv and not wantael:
            return sapv_thisvert

    # will switch to parallel computer if needed
    # currently we use map
    print('Compute sapv and/or ael...might take a while....\n')
    p = Pool()
    #b = p.map(sapvael, range(200), chunksize=100) # debug, testing purpose
    b = p.map(sapvael, range(vertices.shape[0]), chunksize=(vertices.shape[0]//10)) # this is for speed testing
    p.close()
    if wantsapv and wantael:
        # this solution seems slower...
        #for i,el in enumerator(b):
        #    sapv[i]=el[0]
        #    ael[i]=el[1]

        # this is memory intensive, but faster
        sapv = array([i[0] for i in b])
        ael = array([i[1] for i in b])
        return sapv, ael
    else:
        return array(b)




