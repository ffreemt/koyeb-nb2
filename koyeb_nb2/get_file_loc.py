"""Fetch zao bao news image and save to file_loc."""
from pathlib import Path
from joblib import Memory
from logzero import logger

from koyeb_nb2.fetch_zaobao_news_image import fetch_zaobao_news_image

location = "./cachedir"
memory = Memory(location, verbose=0)
zb_image = Path(__file__).parent / "zaobao_news.png"


@memory.cache
def get_file_loc(day=0):
    """Fetch zao bao news image and save to file_loc."""
    img = fetch_zaobao_news_image(day=day)
    try:
        zb_image.write_bytes(img)
    except Exception as e:
        logger.error(e)
        raise

    return zb_image.absolute().as_posix()
