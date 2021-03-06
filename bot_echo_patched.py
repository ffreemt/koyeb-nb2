"""
to config
    edit .env .env.dev .env.prod

nb run
or python bot.py
or uvicorn bot:app

"""
import platform

import nonebot
from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, unescape, MessageEvent, Message, MessageSegment

from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from logzero import logger

# Custom your logger
#
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function

node = platform.node()

config = {
    "host": "0.0.0.0",
    "port":8680,
    "debug": True,
    "nickname": {"elf",},
    "apscheduler_autostart": True,
    "apscheduler.timezone": "Asia/Shanghai",
}
nonebot.init(**config)
echo = on_command("echo", to_me())


@echo.handle()
async def echo_escape_p(bot: Bot, event: MessageEvent):
    try:
        await bot.send(message=f"{node}: {event.get_message()}", event=event)
    except Exception as e:
        logger.error(e)

async def echo_escape_p2(bot: Bot, event: MessageEvent):
    try:
        await echo_escape_p(bot, event)
    except Exception as e:
        logger.error(e)

import nonebot.plugins.echo
nonebot.plugins.echo.echo_escape = echo_escape_p2
# loads of errors but messages sent ok

driver = nonebot.get_driver()

driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_builtin_plugins()
# @bot /echo 000

# load plugin installed via pip install
nonebot.load_plugin("nonebot_plugin_guess")

nonebot.load_from_toml("pyproject.toml")

# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
nonebot.load_plugins("koyeb_nb2/plugins")

app = nonebot.get_asgi()


if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp__main__:app")
    # nonebot.run(app="bot:app")
