def replacehomepath(pattern):
    '''
    replacehomepath(pattern):

    replace home path like '~/test' to full path name, like 'Users/ruyuan/test'. We assume the pattern input is correct
    '''
    import re
    from pathlib import Path  # this is new since python 3.5
    home = str(Path.home())
    reg = re.compile('~.')

    if re.match(reg, pattern):
        pattern = pattern.replace('~', home)
    return pattern