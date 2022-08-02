import platform

import nonebot
from logzero import logger
from nonebot.adapters.onebot.v11 import (
    Adapter,
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    unescape,
)
from nonebot.plugin import on_command
from nonebot.rule import to_me

# from koyeb_nb2.nb2chan import nb2chan

port = 8680  # .env.dev
nonebot.init(port=port)
nonebot.get_driver().register_adapter(Adapter)

node = platform.node()

# echo = on_command("echo", to_me())
# echo = on_command("echo", )
# override built-in echo
# @echo.handle()

ping = on_command("ping", aliases={"p",}, priority=1, block=False)


@ping.handle()
async def handle(bot: Bot, event: MessageEvent):
    try:
        await bot.send(message=f"{node}: {event.get_message()}", event=event)
    except Exception as e:
        logger.error(e)


nonebot.load_plugin("koyeb_nb2.plugins.nb2chan")
# nonebot.load_plugin("koyeb_nb2.plugins.autohelp")

app = nonebot.get_asgi()

nonebot.run(app="bot:app")
# nonebot.run(app="__mp__main__:app")
