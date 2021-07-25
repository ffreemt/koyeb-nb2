"""Send stderr to a string.

Does not work yet.

Use contexlib redirect_stderr/redirect_stdout instead.
"""
import sys
from io import StringIO
from contextlib import contextmanager


@contextmanager
def capture_stderr(astring: str):
    """Send stderr to a string.

    >>> astring = ""
    >>> with capture_stderr(astring):
    >>>     print("aaa", file=sys.stderr)
    >>> astring
    'aaa'
    """
    old = sys.stderr
    buff = StringIO()
    sys.stderr = buff
    try:
        astring = buff.getvalue()
        yield astring
    finally:
        sys.stderr = old
