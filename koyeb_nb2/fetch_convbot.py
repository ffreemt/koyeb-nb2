"""Fetch convbot response."""
# pylint: disable=invalid-name
import httpx
from logzero import logger

url = "https://convbot-yucongo.koyeb.app/text/"


async def fetch_convbot(text: str, prev_resp: str = "") -> str:
    """Fetch convbot response from koyeb."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                url, json={"text": text, "prev_resp": prev_resp}, timeout=10
            )
            res.raise_for_status()
        except Exception as e:
            logger.error(e)
            raise
            # return {"result": {"resp": str(e)}}
    try:
        resp = res.json().get("result").get("resp")
    except Exception as e:
        logger.error(e)
        raise
        # resp = str(e)

    return resp
