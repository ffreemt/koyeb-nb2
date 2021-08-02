"""Send news in image per request."""
from pathlib import Path

# import io
# from time import time
import arrow
import logzero
from logzero import logger
from nonebot import on_command

# from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment

# from koyeb_nb2.fetch_zaobao_news_image import fetch_zaobao_news_image
from koyeb_nb2.get_file_loc import get_file_loc

logzero.loglevel(10)
news = on_command("news", aliases={"xinwen", "新闻", "无聊"}, priority=4,)


@news.handle()
async def handle(bot: Bot, event: Event, state: dict):
    """Handle news requests."""
    # day = round(time() // (24 * 3600))
    day = int(arrow.utcnow().to("Asia/Shanghai").format("YYYYMMDD"))

    logger.debug("state: %s", state)

    file_loc = None
    try:
        # img = fetch_zaobao_news_image(day)
        file_loc = get_file_loc(day)
    except Exception as e:
        logger.error(e)
        # news.finish(e)
        await news.finish(f"{e}")
        # raise
        return None

    if not Path(file_loc):
        logger.warning(" %s does not exist.", file_loc)
        await news.finish(" %s does not exist." % file_loc)
        return None

    await news.finish(MessageSegment.image(f"file:///{file_loc}"))
