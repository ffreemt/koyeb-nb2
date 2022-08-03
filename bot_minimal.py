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
from nonebot.params import Command, CommandArg, RawCommand
from nonebot.plugin import on_command
from nonebot.rule import to_me

# from koyeb_nb2.nb2chan import nb2chan

port = 8680  # .env.dev
nonebot.init(port=port)
nonebot.get_driver().register_adapter(Adapter)

_ = platform.node()
if len(_) > 10:
    node = f"{_[:7]}..."
else:
    node = _[:]

# echo = on_command("echo", to_me())
# echo = on_command("echo", )
# override built-in echo
# @echo.handle()

ping1 = on_command(
    "ping1",
    aliases={
        "p1",
    },
    priority=1,
    block=False,
)


@ping1.handle()
async def handle1(bot: Bot, event: MessageEvent):
    try:
        await bot.send(message=f"-{node}: {event.get_message()}", event=event)
    except Exception as e:
        logger.error(e)


ping2 = on_command(
    "ping2",
    aliases={
        "p2",
    },
    priority=1,
    block=False,
)


@ping2.handle()
async def handle(message: Message = CommandArg()):
    try:
        _ = f"{node}{': ' if str(message).strip() else ''}{message}"
        await ping2.send(message=_)
    except Exception as e:
        logger.error(e)


nonebot.load_plugin("koyeb_nb2.plugins.nb2chan")

# nonebot.load_plugin("koyeb_nb2.plugins.autohelp")

app = nonebot.get_asgi()

if __name__ == "__main__":
    # nonebot.run("bot_minimal:app")
    nonebot.run()
