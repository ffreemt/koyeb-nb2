"""Chat away to your heart's content."""
# import pdir
import logzero
from logzero import logger

import nonebot

# from nonebot import on_message
# from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event

# from nonebot.log import logger

logzero.loglevel(10)

# test = on_message()
# test = nonebot.on_command("chat", aliases={"xianliao", "闲聊"}, priority=5,)
test = nonebot.on_message(priority=5, block=False)


@test.handle()
async def handle(bot: Bot, event: Event, state: dict):
    """Handle messages.
     
    # not tome
    if not event.is_tome():
        return
    
    # all [None, None] 
    if not any([elm.value for elm in 
    jsonpath_ng.parse("$..command").find(state)]):
        return 
    
    # collect user msg
    msg = event.get_plaintext()
    resp = bot_response(msg)
    
    # logic for checking consecutive empty resp 
    if resp.strip():
        ...
    else:
        ... # append extra msg
    
    """
    _ = """
    logger.debug(pdir(event))
    function:
        get_event_description: :说明:
        get_event_name: :说明:
        get_log_string: :说明:
        get_message: :说明:
        get_plaintext: :说明:
        get_session_id: :说明:
        get_type: :说明:
        get_user_id: :说明:
        is_tome: :说明:
    """
    logger.debug(
        "event. get_event_name(): %s, get_message(): %s, get_plaintext(): %s, "
        "get_session_id(): %s, "
        "get_user_id(): %s, "
        "is_tome(): %s",
        event.get_event_name(),
        event.get_message(),
        event.get_plaintext(),
        event.get_session_id(),
        event.get_session_id(),
        event.is_tome(),
    )
    # message.group.normal

    logger.debug("state: %s", state)
    _ = """
     state: {'_prefix': {'raw_command': '/news', 'command': ('news',)}, '_suffix': {'raw_command': None, 'command': None}}

    state: {'_prefix': {'raw_command': None, 'command': None}, '_suffix': {'raw_command': None, 'command': None}}

    {
    "_prefix": {
      "raw_command": "/news",
      "command": [
        "news"
      ]
    },
    "_suffix": {
      "raw_command": null,
      "command": null
    }
    }

    [elm.full_path for elm in jsonpath_ng.parse("$..command").find(r)]

    """
