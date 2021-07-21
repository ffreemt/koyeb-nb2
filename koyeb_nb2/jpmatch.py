'''
to emulate jsonpath_ext_rw (cant pack with cz_freeze or pyinstaller
 '''
from jsonpath_rw import parse

def jpmatch(x, y):
    return [elm.value for elm in parse(x).find(y)]
