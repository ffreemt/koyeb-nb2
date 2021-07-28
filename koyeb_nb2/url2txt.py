"""Fetch text from url.

from random import sample
# pop = string.ascii_lowercase + string.digits
pop = 'abcdefghijklmnopqrstuvwxyz0123456789'

"".join(sample(pop, 6)))
"""
from typing import Optional

from urllib.parse import urlparse
import httpx
import html2text
from readability import Document

from logzero import logger


# fmt: off
def url2txt(
    url: str,
    bodywidth: Optional[int] = 5000,
    remove: bool = False,
    show_url: bool = True,
    ignore_links: bool = True,
) -> str:
    # fmt: on
    """Fetch text from url.

    Args
        bodywidth: if set to None, fall back to default bodywidth of
            html2text.HTML2Text
        remove: remove blank lines if set to True
        show_url: prepend url if set to True
        ignore_links: remove [ur](url)

    Return
        main body in text

    bodywidth: Optional[int] = 5000
    remove: bool = False
    show_url: bool = True
    ignore_links: bool = True
    """
    if not url.startswith("http"):
        url = "http://" + url

    logger.info("url: %s", url)

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:  # no scheme or netloc present
        raise Exception("Invalid url: %s" % url)

    try:
        resp = httpx.get(url, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        logger.error(exc)
        raise

    try:
        doc = Document(resp.text)
    except Exception as exc:
        logger.error(exc)
        raise

    if not doc.summary().strip():
        raise Exception("No content for some reason...")

    if bodywidth is not None:
        handle = html2text.HTML2Text(bodywidth=bodywidth)
    else:
        handle = html2text.HTML2Text()

    handle.ignore_links = ignore_links

    try:
        res = handle.handle(doc.summary())
    except Exception as exc:
        logger.error(exc)
        raise

    # remove double blank lines
    if remove:
        res = "\n".join(elm for elm in res.splitlines() if elm.strip())

    if not res.strip():  # warn if empty output
        logger.warning("Output seems to be empty...")

    if show_url:
        return f"{url}\n# {doc.title()}\n{res}"

    return f"# {doc.title()}\n{res}"
