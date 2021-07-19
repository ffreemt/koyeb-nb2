"""Emulate jsonpath_ext_rw (jsonpath_ext_rw cant pack with cz_freeze or pyinstaller."""
from jsonpath_rw import parse


class jp:
    """Emulate jp.match in jsonpath_rw_ext."""

    @staticmethod
    def match(x, y):
        """Locate y in x.

        jp.match('$', obj)
        jp.match('$..dst', resp_fd4.json()): search 'dst'
        """
        return [elm.value for elm in parse(x).find(y)]
