"""Start gocqhttp with subprocess.

Intended to be wrapped in multiprocess.Process.
"""
import os
import subprocess as sp
from pathlib import Path
from platform import platform
from shlex import split

from logzero import logger


def start_gocq(wd: str = "go-cqhttp"):
    """Start gocqhttp with subprocess.

    Intended to be wrapped in multiprocess.Process.
    Args:
        gocq executable and config device files in wd.
    """
    os.chdir(wd)
    logger.info("Starting gocq in %s", os.getcwd())

    if platform().lower().startswith("windows"):
        cmd = "go-cqhttp_windows_amd64.exe"
    else:
        cmd = "go-cqhttp"
    logger.debug("cmd: %s", cmd)

    assert Path(cmd).exists(), f"File {cmd} does not exist."

    # make sure it's executable for linux
    if platform().lower().startswith("linux"):
        # os.chmod(cmd, os.stat(cmd) | stat.S_IEXEC)
        sp.check_call(["chmod", "+x", cmd])

    # render.com uploads secret files in project root
    # copy config.yml and device.json from parent dir
    if not Path("config.yml").exists():
        try:
            sp.check_call(["cp", "../config.yml", "."])
        except Exception as exc:
            logger.error(exc)
    if not Path("device.json").exists():
        try:
            sp.check_call(["cp", "../device.json", "."])
        except Exception as exc:
            logger.error(exc)

    with sp.Popen(
        split(cmd),
        shell=True,
        # stdout=-1,
        stderr=-1,
        # bufsize=1,
        text=True,
    ) as proc:
        while proc.poll() is None:
            if proc.stderr is not None:
                err = proc.stderr.read()
            else:
                continue
            # logger.error(err.decode("utf8"))
            logger.error(err)

    if proc.returncode != 0:
        raise sp.CalledProcessError(proc.returncode, proc.args)

    logger.debug("end")


if __name__ == "__main__":
    start_gocq()
