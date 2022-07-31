"""Fetch convbot response."""
# pylint: disable=invalid-name
import httpx
from logzero import logger

url = "https://convbot-yucongo.koyeb.app/text/"
url = "https://hf.space/embed/mikeee/convbot/+/api/predict"


# async def fetch_convbot(text: str, prev_resp: str = "") -> str:
async def fetch_convbot(text: str) -> str:
    """Fetch convbot response from koyeb/hf space."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(
                # url, json={"text": text, "prev_resp": prev_resp},
                url, json={"data": [text]},
                timeout=10
            )
            res.raise_for_status()
        except Exception as e:
            logger.error(e)
            raise
            # return {"result": {"resp": str(e)}}
    try:
        # resp = res.json().get("result").get("resp")
        resp = res.json().get("data")[0]
    except Exception as e:
        logger.error(e)
        raise
        # resp = str(e)

    return resp
