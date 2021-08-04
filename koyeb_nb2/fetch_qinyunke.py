"""fetch 青云客聊天。

目前免费，每天使用限度不清楚，能用多久不清楚。
"""
# pylint: disable=invalid-name
from urllib.parse import urlencode
import httpx

import logzero
from logzero import logger

logzero.loglevel(10)
url = "http://api.qingyunke.com/api.php"


async def fetch_qinyunke(text: str) -> str:
    """Fetch response.

    http://api.qingyunke.com/api.php?key=free&appid=0&msg=%E4%BD%A0%E5%A5%BD
    """
    data = {"key": "free", "appid": 0, "msg": text}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{url}?{urlencode(data)}")
            resp.raise_for_status()
        except Exception as e:
            logger.error("client.get exc: %s", e)
            raise

    try:
        _ = resp.json().get("content", "")
    except Exception as e:
        logger.error(e)
        raise

    return _
