"""Test personal push service.

curl 127.0.0.1:5580/admin?q=123
curl 127.0.0.1:8680/admin?q=123

# works only on http not https
# works http://127.0.0.1:8680/admin/
# does not work: https://127.0.0.1:8680/admin/

    koyeb-nb2
or
curl externalip:5580/admin?q=123
    if firewall is set open

display 欢迎来到管理页面 q:123
message sent to 41947782: 欢迎来到管理页面 q:123

---
app = nonebot.get_asgi()
@app.get('/')
async def _():
    pass

@bot.server_app.route('/admin')
改成
   @nonebot.get_asgi().get('/admin')
"""
# pylint: disable=invalid-name
# from quart import request

import platform
import pendulum
from fastapi import Security, Depends, HTTPException, status
# from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader, APIKeyQuery

# from contextvars import ContextVar
import logzero
from logzero import logger

import nonebot
# from aiocqhttp.exceptions import Error as CQHttpError

# from .config import Settings
from typing import List, Union

from pydantic import BaseSettings, Field, validator

_ = platform.node()
if len(_) > 10:
    node = f"{_[:7]}..."
else:
    node = _[:]


class Settings(BaseSettings):
    """Preset default valid tokens."""

    token_list: List[Union[str, int]] = Field(
        default_factory=lambda: ["DEMO_TOKEN", "SECRET_TOKEN"]
    )

    @validator("token_list")
    def validate_namelist(cls, v):
        res = []
        for elm in v:
            try:
                # may use numerbers
                elm = str(elm).strip()
            except Exception as exc:
                logger.error(exc)
                raise

            _ = """
            if len(elm) < 1:
                raise ValueError(
                    "Empty token not allowed"
                )
            """

            if len(elm) == 0:
                logger.warning(
                    "This entry [%s] is empty: probably not what you want, but we let it pass.",
                    elm,
                )

            res.append(elm)

        return res

    class Config:  # pylint: disable=too-few-public-methods
        """Config."""

        env_prefix = "nb2chan_"
        # extra = "allow"
        env_file = ".env.nb2chan"
        env_file_encoding = "utf-8"

        logger.info("env_prefix: %s, env_file: %s", env_prefix, env_file)


settings_nb2chan = Settings()

# logzero.loglevel(20)
logzero.loglevel(10)

app = nonebot.get_asgi()
# app.fastapi_openapi_url = "/openapi.json"

# API_TOKEN = "SECRET_API_TOKEN"
API_TOKENS = ["DEMO_TOKEN", "SECRET_API_TOKEN"]

# may use other methods (e.g., sqlite, redis etc.)
API_TOKENS = settings_nb2chan.token_list

logger.debug("API_TOKENS: %s", API_TOKENS)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="static"), name="root")

api_key_header = APIKeyHeader(name="Token", auto_error=False)
api_key_query = APIKeyQuery(name="Token", auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    # api_key_cookie: str = Security(api_key_cookie),
):
    """Retrieve api key."""
    logger.debug("api_key_query: %s", api_key_query)
    logger.debug("api_key_header: %s", api_key_header)
    if api_key_query in API_TOKENS:
        logger.debug("valid Token provided in query")
        return api_key_query
    elif api_key_header in API_TOKENS:
        logger.debug("valid Token provided in headers")
        return api_key_header
    # elif api_key_cookie == API_KEY:
    # return api_key_cookie
    else:
        logger.debug("no valid Token provided, raising exception")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to validate Token",
        )


@app.get("/")
async def landing():
    """Define landing page."""
    return f"Hello nb2chan (from {node})!"


@app.get("/nb2chan/")
async def nb2chan(
    token: str = Depends(get_api_key),
    qq: str = None,
    msg: str = None,
):
    """Define fastapi query.

    openapi docs at: /docs

    ```bash
    http -v "http://.../nb2chan/?Token=DEMO_TOKEN&qq=123&msg=hello world"

    # send Token via HEADERS
    http -v "http://.../nb2chan/?qq=123&msg=hello world" "token: DEMO_TOKEN"
    curl "http://.../nb2chan/?qq=123&msg=hello world" -H "token: DEMO_TOKEN"
    curl "http://127.0.0.1:8680/nb2chan/?qq=123&msg=hello%20world" -H "token: DEMO_TOKEN"
    ```
    """
    try:
        bot = nonebot.get_bot()
    except Exception as e:
        logger.debug(e)

        # if not bot:
        _ = "Unable to acquire bot, exiting..."
        logger.warning(_)
        return {"error": f"{node}: {_}"}

    if not qq:
        return {"error": "qq# required（e.g. ...&qq=123456...）, 否则发给谁呢？"}

    if msg:
        query = str(msg)
    else:
        query = ""

    msg = f"{node} seen msg: {query}"
    try:
        # await bot.send_private_msg(user_id=41947782, message=msg)
        await bot.send_private_msg(user_id=f"{qq}", message=msg)
        _ = pendulum.now().in_timezone("Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss z")
        res = {"success": f"'{msg}' sent to {qq} {_}"}
    except Exception as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node} exc: {exc}, (大佬这个qq号[{qq}]加机器人好友了吗？ 没加的话用不了nb2酱。)"
        res = {"error": msg}

    return res
