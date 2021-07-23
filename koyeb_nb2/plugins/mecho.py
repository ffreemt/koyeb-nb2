"""Send msg back via echo with hostname."""
from platform import node

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

# echo = on_command("echo", to_me())
mecho = on_command("mecho")
node_ = node()


@mecho.handle()
async def handle(bot: Bot, event: MessageEvent):
    """Echo with hostname attached."""
    await bot.send(message=f"{node_}: {event.get_message()}", event=event)
