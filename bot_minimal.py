import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init(port=80)
nonebot.get_driver().register_adapter(Adapter)

app = nonebot.get_asgi()

nonebot.run(app="bot:app")
# nonebot.run(app="__mp__main__:app")
