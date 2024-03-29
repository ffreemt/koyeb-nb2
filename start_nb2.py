"""Start gocq and nb2 in one go."""
import os
import subprocess as sp
import time
from multiprocessing import Process
from shlex import split

# from time import sleep

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

    # cmd = "poetry run nb run -f bot_minimal.py"
    cmd = "nb run -f bot_minimal.py"
    logger.debug("cmd: %s", cmd)
    try:
        with sp.Popen(
            split(cmd),
            # shell=True,
            # stdout=sp.PIPE,
            # stderr=sp.STDOUT,
            stderr=sp.PIPE,
            text=True,
        ) as proc:
            while proc.poll() is None:
                _ = """
                out = proc.stdout.readl()
                logger.debug(out.decode("utf8"))
                # """
                # err = proc.stderr.read()
                # if proc.stdout is not None:
                if proc.stderr is not None:
                    # out = proc.stdout.read()
                    out = proc.stderr.read()
                    # logger.error(err.decode("utf8"))
                    # logger.error(err)
                    # sleep(.1)
                    
                    # only print nonempty
                    try:
                        out_ = out.strip()
                    except Exception as exc:
                        out_ = str(exc)
                    if out_:
                        logger.error(out_)   
                else:
                    continue

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
