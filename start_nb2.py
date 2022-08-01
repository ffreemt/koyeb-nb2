"""Start gocq and nb2 in one go."""
from multiprocessing import Process
import subprocess as sp
from shlex import split
from time import sleep

from logzero import logger

from koyeb_nb2.start_gocq import start_gocq


def main():
    """Bundle start_gocq with nb run -f bot.py."""
    gocq = Process(target=start_gocq)
    gocq.start()

    cmd = "nb run -f bot_minimal.py"
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
                out = proc.stdout.read()
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
