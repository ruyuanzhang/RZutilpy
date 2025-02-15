import pathlib2 as pathlib
# we use the subclass to redefine the Path, and provide several useful utilities

class Path(type(pathlib.Path())):
    def __new__(cls, *args, **kwargs):
        tmp = type(pathlib.Path()).__new__(cls, *args, **kwargs)
        tmp = tmp.expanduser()
        tmp = tmp.resolve()
        return tmp

    def __init__(self, path):
        pass

    # ========= add some properties ===============
    # some useful properties

    # name: '~/test.py' 'test.py'

    @property
    def pstem(self): # property only-read
        # pure name without suffixes, useful when having multiple suffixes
        return self.name.replace(''.join(self.suffixes), '')

    @property
    def str(self): # 
        # full path string
        return self.__str__()

    @property
    def strnosuffix(self): # property only-read
        # full path string without all suffexs
        return self.str.replace(''.join(self.suffixes), '')

    @property
    def suffixesstr(self): # property only-read
        # a string of the combination of all suffixes
        return ''.join(self.suffixes)
    # ========= add some function done ===============
    def home(self):
        # original home function seems not work, now I rewrite it here.
        from os.path import expanduser
        return type(self)(expanduser('~'))

