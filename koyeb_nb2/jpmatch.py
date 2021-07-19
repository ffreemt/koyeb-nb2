"""Emulate jsonpath_ext_rw (cant pack with cz_freeze or pyinstaller."""
from jsonpath_rw import parse


def jpmatch(x, y):
    """Emulate jsonpath_ext_rw."""
    return [elm.value for elm in parse(x).find(y)]
