"""Chat away to your heart's content."""
# pylint: disable=invalid-name
# import pdir
from random import choice
import re
import jsonpath_ng
import logzero
from logzero import logger
from fastlid import fastlid

import nonebot
from nonebot.typing import T_State

# from nonebot import on_message
# from nonebot import on_command
# from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.onebot.v11 import Bot, Event

# from nonebot.log import logger

# from koyeb_nb2.fetch_convbot import fetch_convbot
# from koyeb_nb2.fetch_qinyunke import fetch_qinyunke
from koyeb_nb2.bot_response import bot_response

# test = on_message()
# test = nonebot.on_command("chat", aliases={"xianliao", "闲聊"}, priority=5,)

# on_message = nonebot.on_message(priority=5, block=False)


# @on_message.handle()
@nonebot.on_message(priority=5, block=False).handle()
async def handle(bot: Bot, event: Event, state: T_State = State()):
    """Handle messages.

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
    # not tome
    if not event.is_tome():
        return

    # all [None, None]
    logger.debug("[elm.value for elm in jsonpath_ng.parse('$..command').find(state)]: %s", [elm.value for elm in jsonpath_ng.parse("$..command").find(state)])
    logger.debug("not any([elm.value for elm in jsonpath_ng.parse('$..command').find(state)]): %s", not any([elm.value for elm in jsonpath_ng.parse("$..command").find(state)]))

    if any([elm.value for elm in jsonpath_ng.parse("$..command").find(state)]):  # _prefix or _suffix command, ignore
        return

    # [None, None]: deemed as chat
    # initialzie attr for recoding consecutive empty responses
    # and prev_resp
    try:
        handle.c_resp
        handle.prev_resp
    except AttributeError:
        handle.c_resp = 0
        handle.prev_resp = ""

    # process messages
    msg = event.get_plaintext()

    # detect language
    lang = fastlid(msg)
    # safeguard short Chinese phrases
    if len(msg) <= 10 and re.search(r"[一-龟]+", msg):
        lang = "zh", .5
        logger.debug(" safeguard branch ")

    if lang[0] not in ["en", "zh", "fr", "de"]:
        try:
            await bot.send(message=f"I detect you are talking in [{lang}], which I currently am unable to understand. (I am able to chat in Chinese, English, German and French -- 我只会一点点中、英、德、法啊，大佬.)", event=event)
        except Exception as e:
            logger.error(e)

    try:
        resp = await bot_response(msg)
    except Exception as e:
        logger.error("bot_response exc: %s", e)
        resp = str(e)

    # empty response from the bot
    if not resp.strip():
        resp = "..."
        handle.c_resp += 1
    else:  # reset counter
        handle.c_resp = 0

    if handle.c_resp > 2:
        msg = choice([
            "You are talking nonesense or something is probably wrong. In the latter case, conatct my master.",
            "You are talking nonesense or something is probably wrong. In the latter case, contact my master. In the former case, well...",
            "Either you are talking nonesense or something is probably wrong. In the latter case, contact my master.",
            "If you are not talking nonesense, then something is probably wrong.",
        ])
        try:
            await bot.send(
                message=f"...({msg})",
                event=event,
            )
            handle.c_resp = 0
        except Exception as e:
            logger.error(e)

        return

    try:
        await bot.send(message=resp, event=event)
    except Exception as e:
        logger.error(e)
