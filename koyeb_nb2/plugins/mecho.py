"""Send msg back via echo with hostname attached."""
from platform import node

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from logzero import logger

# echo = on_command("echo", to_me())
mecho = on_command("mecho", aliases={"ping", "ryt", "在不", "p"}, priority=1,)
node_ = node()


@mecho.handle()
async def handle(bot: Bot, event: MessageEvent, state: dict):
    """Echo with hostname attached."""
    # await bot.send(message=f"{node_}: {event.get_message()}", event=event)
    _ = dict(message=f"{node_}: {event.get_message()}", event=event, state=state)
    msg = _.get("message", "")
    logger.debug(msg)
    try:
        # await bot.send(**_)  # OK
        await bot.send(message=msg, event=event)

        # await bot.finish(message=msg, event=event)  # Object of type PrivateMessageEvent is not JSON serializable
    except Exception as e:
        logger.error(e)

    # await bot.finish(f"{node_}: {event.get_message()}")  # nogo
    # await bot.finish(message=f"{node_}: {event.get_message()}", event=event)  # nogo
    # await bot.finish(message=f"{node_}: {event.get_message()}")  # nogo
