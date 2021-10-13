"""Parse command according to a given argparse.ArgumentParser."""
from typing import Tuple

from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
import shlex
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from logzero import logger


def parse_cmd(
    command: str, parser: ArgumentParser = None
) -> Tuple[Namespace, str, str]:
    """Parse command a given argparse.ArgumentParser.

    Args
        command: str to parse
        parser: predefined template
    Returns
        args, stdout, stderr
    """
    if parser is None:
        parser = ArgumentParser(
            prog="dummy",
            description='dummy parser for cases when no parser is provided',
            # exit_on_error=False,  # exit_on_error avail in 3.9
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument("params", nargs="*", help="list of parameters of type str")

    # capture stderr
    stderr = StringIO()
    stdout = StringIO()
    args = parser.parse_args([])
    with redirect_stderr(stderr), redirect_stdout(stdout):
        # catch SystemExit
        try:
            args = parser.parse_args(shlex.split(command))
        except SystemExit:
            logger.error("SystemExit caught.")
            # args = parser.parse_args([])
        except BaseException as e:
            logger.error(e)
            # args = parser.parse_args([])
    if stderr.getvalue():
        logger.error(stderr.getvalue())

    return args, stdout.getvalue(), stderr.getvalue()
