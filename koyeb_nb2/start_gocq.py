"""Start gocqhttp with subprocess.

Intended to be wrapped in multiprocess.Process.
"""
# pylint: disable=invalid-name
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

    # pass if both (config.yml device.json) exist
    logger.debug(" config.yml: %s", Path("config.yml").exists())
    logger.debug(" device.json: %s", Path("device.json").exists())

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

    # koyeb: unzip config-device.zip using
    # os.environ.get("PW4UNZIP") as password
    if not (Path("config.yml").exists() and Path("device.json").exists()):
        logger.info("Unzipping (unizp -o -P... ) config-device.zip if exist (for koyeb) ")
        if Path("config-device.zip").exists():
            pw4unzip = os.environ.get("PW4UNZIP")
            # assert pw4unzip, " env var PW4UNZIP not set"
            if not pw4unzip:
                logger.warning("copy or generate config.yml and device.json in %s", Path().resolve())
                logger.warning("or make config-device.zip available and set env var PW4UNZIP.")
                logger.info("Goodbye!")
                raise SystemExit(1)

            try:
                cmd = split(f"unzip -o -P {pw4unzip} config-device.zip")
                sp.check_call(cmd)
            except Exception as exc:
                logger.error(exc)

    if platform().lower().startswith("windows"):
        cmd = "go-cqhttp_windows_amd64.exe"
    else:
        cmd = "./go-cqhttp"
    logger.debug("cmd: %s", cmd)

    assert Path(cmd).exists(), f"File {cmd} does not exist."

    # make sure it's executable for linux
    if platform().lower().startswith("linux"):
        # os.chmod(cmd, os.stat(cmd) | stat.S_IEXEC)
        sp.check_call(["chmod", "+x", cmd])

    if not Path("config.yml").exists():
        logger.warning(" config.yml does not exist.")
        logger.info(" go-cqhttp wont run properly...")

    if not Path("device.json").exists():
        logger.warning(" device.json does not exist.")
        logger.info(" go-cqhttp wont run properly...")

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
