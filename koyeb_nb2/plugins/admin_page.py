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

import logzero
from logzero import logger

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

logzero.loglevel(10)
# nonebot2
# bot = nonebot.get_driver()

app = nonebot.get_asgi()


# @bot.server_app.route('/admin')
@app.get("/admin/")
async def admin_page(q: str = None):
    """Get q."""
    if q:
        query = q
    else:
        query = ""

    logger.debug("nonebot.get_bots(): %s", nonebot.get_bots())

    # bot = nonebot.get_bots().get("2129462094")
    bots = [*nonebot.get_bots().values()]
    bot = None
    if bots:
        bot, *_ = bots

    if not bot:
        return

    try:
        await bot.send_private_msg(user_id=41947782, message=f".你的主页被访问了nb2 q: {query}")
    except CQHttpError as exc:
        logger.error(exc)
        # logger.exception(exc)
    except Exception as exc:
        logger.error(exc)
        # logger.exception(exc)
    return f"_欢迎来到nb2管理页面 q: {query}\n"
