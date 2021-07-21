"""Fetch zao bao news image.

httpx.get("https://api.2xb.cn/zaob").json().get("imageUrl")
MessageSegement.image
"""
import httpx

# from time import time
from joblib import Memory
from logzero import logger

location = "./cachedir"
memory = Memory(location, verbose=0)

url_zb = "https://api.2xb.cn/zaob"


@memory.cache
def fetch_zaobao_news_image(day: int = 0) -> bytes:
    """Fetch zao bao news image.

    Args
        day: current day, will fetch from cache if called with
        fetch_zaobao_news_image(round(time() // (24 * 3600)))

    Returns
        Today's news image
    >>> image = fetch_zaobao_news_image()
    >>> len(image) > 1000
    """
    try:
        resp = httpx.get(url_zb)
        resp.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise
    try:
        jdata = resp.json()
    except Exception as e:
        logger.error(e)
        raise

    image_add = jdata.get("imageUrl", "")
    if not image_add:
        logger.warning(jdata)
        return b""

    try:
        resp = httpx.get(image_add)
        resp.raise_for_status()
    except Exception as e:
        logger.error(e)
        raise

    return resp.content
