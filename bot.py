"""
to config
    edit .env .env.dev .env.prod

nb run
or python bot.py
or uvicorn bot:app

"""
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# Modify some config / config depends on loaded configs
# 
config = driver.config
# do something...
config.HOST = '0.0.0.0'
config.PORT = 5580
config.PORT = 5680  #
config.NICKNAME = {'ELF', 'elf'}
config.SUPERUSERS = {41947782}
config.API_ROOT = 'http://127.0.0.1:5700'

app = nonebot.get_asgi()

nonebot.load_builtin_plugins()
# @bot /echo 000
nonebot.load_from_toml("pyproject.toml")


if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp__main__:app")
    # nonebot.run(app="bot:app")
