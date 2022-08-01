"""Execute a command.

https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running/4417735#4417735
"""
import subprocess
import sys
from shlex import split

from logzero import logger


def execute(command):
    # process =
    try:
        with subprocess.Popen(
            split(command),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ) as process:

            # Poll process for new output until finished
            # while True:
            while process.poll() is None:
                if process.stdout is not None:
                    nextline = process.stdout.readline()
                else:
                    continue
                if nextline == '' and process.poll() is not None:
                    break

                # sys.stdout.write(nextline)
                logger.debug(nextline)
                # sys.stdout.flush()

        output = process.communicate()[0]
        exitCode = process.returncode

        if exitCode == 0:
            return output
        else:
            # raise sys.ProcessException(command, exitCode, output)
            raise subprocess.CalledProcessError(exitCode, process.args)
    except Exception as exc:
        logger.error(exc)


def main():
    cmd = "nb run -f bot_minimal.py"
    # cmd = "ping -n 100 google.com"

    try:
        execute(cmd)
    except Exception as exc:
        logger.error(exc)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        logger.error(exc)
    finally:
        # execute("taskkill /f /im nb.exe")
        ...
