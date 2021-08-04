"""Run AIML germanbot.

based on frenchbot
"""
# pylint: disable=invalid-name
from pathlib import Path
import re
import string
import logzero
from logzero import logger
from aiml import Kernel

logzero.loglevel(10)
kernel = Kernel()

aimldir = Path(__file__).parent / "aiml-std-de"
if Path(aimldir).exists():
    _ = Path(aimldir) / r"*.aiml"
    kernel.learn(_.as_posix())
    logger.info("kernel.learn( ): Loading aiml from %s", Path(aimldir))
else:
    logger.error("Cant load *.aiml")


# kernel.respond("load aiml b")

kernel.setBotPredicate("master", "Internet")
kernel.setBotPredicate("botmaster", "ishmael")
kernel.setBotPredicate("location", "France")
kernel.setBotPredicate("birthday", "a Friday")
kernel.setBotPredicate("birthplace", "net")
kernel.setBotPredicate("it", "a French project")
kernel.setBotPredicate("gender", "female")
kernel.setBotPredicate("favoritecolor", "bleu")

kernel.setBotPredicate("name", "Alison")

logger.debug(" done loading kernel ")

# for removing irregular punctuation
patt = re.compile(rf"[{string.punctuation}]\s+([{string.punctuation}])")


def germanbot(sent: str) -> str:
    """Run germanbot.

    >>> germanbot('Guten Abend')
    'Guten Abend. Wie war Dein Tag?'

    """
    try:
        sent = str(sent)
    except Exception as e:
        logger.error("str(sent) exc: %s", e)
        raise

    try:
        return patt.sub(r"\1", kernel.respond(sent))
    except Exception as e:
        logger.error("germanbot kernel.respond exc: %s", e)
        raise


if __name__ == "__main__":
    print(germanbot("Guten Tag"))
