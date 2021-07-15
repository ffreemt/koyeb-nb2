"""
https://v2.nonebot.dev/guide/getting-started.html

edit .env .env.dev .env.prod to config

python minibot.py to run
    or 
        add  to 
            app = nonebot.get_asgi()
        uvicorn minibot:app
"""
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()
# @bot /echo 000

app = nonebot.get_asgi()
# uvicorn --port 8680 minibot:app

if __name__ == "__main__":
    # @bot /echo 000
    nonebot.run()
