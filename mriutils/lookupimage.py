

class lookupimage():
    '''
    visualization and brain background and a overlay

    '''

    def __init__(self, surffile):
        self.surf(surffile)


    updatefigure(self, surf):
        pass

    # get and set
    @property
    def overlayscalars(self):
        return self._overlayscalars
    @overlayscalars.setter
    def overlayscalars(self, x):
        self._overlayscalars = x  #set

    # get and set the surface
    @property
    def surf(self):
        return self._overlayscalars
    @surf.setter
    def surf(self, x):
        self.surf = x
        return self._overlayscalars




