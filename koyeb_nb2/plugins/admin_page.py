"""Test personal push service.

curl 127.0.0.1:5580/admin?q=123
curl 127.0.0.1:8680/admin?q=123
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
# from quart import request

from platform import node
import logzero
from logzero import logger

import nonebot
from contextvars import ContextVar
from aiocqhttp.exceptions import Error as CQHttpError

logzero.loglevel(10)
# nonebot2
# bot = nonebot.get_driver()

app = nonebot.get_asgi()
node_ = node()
# current_bot: ContextVar = ContextVar("current_bot")


# @bot.server_app.route('/admin')
@app.get("/admin/")
async def admin_page(q: str = None):
    """Get q."""
    if q:
        query = q
    else:
        query = ""

    logger.debug("nonebot.get_bots(): %s", nonebot.get_bots())

    _ = """
    # bot = nonebot.get_bots().get("2129462094")
    bots = [*nonebot.get_bots().values()]
    bot = None
    if bots:
        bot, *_ = bots

    if not bot:
        return
    """

    _ = [*nonebot.get_bots().values()]
    bot = _[0] if _ else None
    if not bot:
        _ = "Unable to acquire bot, exit."
        logger.warning(_)
        return f"{node_:} {_}"

    _ = """
    try:
        bot = current_bot.get()
        # event = current_event.get()
    except Exception as e:
        logger.error(e)
        return f"exc: {e}"
    """

    msg = f"{node_} seen q: {query}"
    try:
        await bot.send_private_msg(user_id=41947782, message=msg)
    except CQHttpError as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node_} exc: {exc}"
    except Exception as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node_} exc: {exc}"

    return f"{msg}"
