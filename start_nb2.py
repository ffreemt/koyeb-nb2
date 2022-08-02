"""Start gocq and nb2 in one go."""
import os
import subprocess as sp
import time
from multiprocessing import Process
from shlex import split
from time import sleep

from logzero import logger

from koyeb_nb2.start_gocq import start_gocq

os.environ["TZ"] = "Asia/Shanghai"
try:
    time.tzset()
except Exception:
    ...  # only works in Linux


def main():
    """Bundle start_gocq with nb run -f bot.py."""
    gocq = Process(target=start_gocq)
    gocq.start()

    cmd = "poetry run nb run -f bot_minimal.py"
    logger.debug("cmd: %s", cmd)
    try:
        with sp.Popen(
            split(cmd),
            # shell=True,
            stdout=-1,
            # stderr=-1,
            stderr=sp.STDOUT,
            text=True,
        ) as proc:
            while proc.poll() is None:
                _ = """
                out = proc.stdout.readl()
                logger.debug(out.decode("utf8"))
                # """
                # err = proc.stderr.read()
                if proc.stdout is not None:
                    out = proc.stdout.read()
                else:
                    continue

                # logger.error(err.decode("utf8"))
                # logger.error(err)
                logger.error(out)
                sleep(1)
        if proc.returncode != 0:
            raise sp.CalledProcessError(proc.returncode, proc.args)
    except Exception as exc:
        logger.error(exc)
    finally:
       gocq.kill()  # not really necessary

    # will not come to this
    logger.info("end")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.error(exc)
