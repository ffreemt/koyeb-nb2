"""Bootstrap the bot.

to config
    edit .env .env.dev .env.prod

nb run
or python bot.py
or uvicorn bot:app

"""
import nonebot

# from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from nonebot.adapters.onebot.v11 import Adapter
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

config = {
    "host": "0.0.0.0",
    "port": 8680,
    "debug": True,
    # "debug": False,
    "nickname": {"elf", },
    "apscheduler_autostart": True,
    "apscheduler.timezone": "Asia/Shanghai",
    # "fastapi_docs_url": "docs",
    # "fastapi_docs_url": "/docs/",
    # "fastapi_docs_url": "static",
    # "docs_url": "docs",
    "fastapi_openapi_url": "/openapi.json",
}

# nonebot.init(**config)
nonebot.init(port=8680)
nonebot.get_driver().register_adapter(Adapter)

# import koyeb_nb2.nb2chan  # pylint: disable=wrong-import-position, unused-import  # noqa

# nonebot.load_builtin_plugins()
nonebot.load_builtin_plugin("echo")

# @bot /echo 000

# nonebot.load_plugin("nonebot_plugin_guess")
# nonebot.load_from_toml("pyproject.toml")

# 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
# does not seem to load, return set()
# nonebot.load_plugins("koyeb_nb2/plugins")

# load plugin installed via pip install, order matters
# nonebot.load_plugin("nonebot_plugin_autohelp")

# nonebot.load_plugin("koyeb_nb2.plugins.autohelp")
# import koyeb_nb2.plugins._autohelp  # pylint: disable=wrong-import-position, unused-import  # noqa

app = nonebot.get_asgi()

# define some fastapi path

if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")

    nonebot.run(app="__mp__main__:app")

    from multiprocessing import Process
    from threading import Thread
    from koyeb_nb2.start_gocq import start_gocq

    # Process(target=start_gocq).start()
    # Thread(target=start_gocq).start()

    # nonebot.run(app="bot:app")
