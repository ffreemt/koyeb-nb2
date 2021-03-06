"""Autogenerate response to commands /help !help help.

For more info on usage:
/help -h
"""
# pylint: disable=invalid-name
# import asyncio
from typing import Optional
from nonebot.typing import T_State

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import re
from time import time
import logzero
from logzero import logger

import nonebot
from nonebot.adapters.cqhttp import Bot, Event

from koyeb_nb2.parse_cmd import parse_cmd
from koyeb_nb2.fetch_plugin_info import fetch_plugin_info

# for ratelimit, will not respond twice within 30 seconds
_vars = dict(last_sent=0.0, interval=30)
patt = re.compile(r"^[/!#]?\s*(?:help|menu|帮助|菜单|caidan|info)|[/#]i", re.I)

logzero.loglevel(10)
on_message = nonebot.on_message(priority=10, block=False)
config = nonebot.Config()

# nonebot.load_from_toml("pyproject.toml")
# nonebot.load_plugin("nonebot_plugin_guess")

# wait for other plugins to load
# async def wait_for_30(): await asyncio.sleep(30)

logger.info("Loaded plugins: %s", [elm.name for elm in nonebot.get_loaded_plugins()])

# module path (__init__.py or plugin_name.py path)
# [elm.module.__file__ for elm in nonebot.get_loaded_plugins()]

# module doc: info at the begenning of the file
# [elm.module.__doc__ for elm in nonebot.get_loaded_plugins()]

# func doc: elm.module.handle.__doc__


@on_message.handle()
async def handle(bot: Bot, event: Event, state: Optional[T_State]):
    """Handle messages."""
    logger.debug(" nonebot_plugin_autohelp entry ")
    logger.debug("state: %s", state)

    _ = time() - _vars.get("last_sent", 0)
    logger.debug("check time interval: %.1f", _)
    if _ < _vars["interval"]:
        logger.debug("Too soon... return ...")
        return

    # messages not startswith [/!#]?\s*help (case-insensitive
    msg = event.get_plaintext()
    logger.debug("msg: %s", msg)
    # if not re.findall(, msg, re.I):
    if not patt.findall(msg):
        logger.debug("patt.findall(msg) False, return...")
        return

    parser = ArgumentParser(prog="help", formatter_class=ArgumentDefaultsHelpFormatter,)
    parser.add_argument(
        "-d", "--details", action="store_true", help="show __doc__ for each plugin"
    )
    parser.add_argument("params", nargs="*", help="list of parameters of type str")

    command = str(event.get_message()).strip()
    logger.debug("command (str(event.get_message()).strip()): %s", command)

    args, stdout, stderr = parse_cmd(command, parser)
    logger.debug("args: %s", args)

    if stdout or stderr:
        await bot.send(message="\n---\n".join([stdout, stderr]), event=event)
        return

    keys = [
        "nickname",
        "command_start",
        "command_sep",
    ]
    info = "\n".join(
        f"{key}: {', '.join(val)}" for key, val in nonebot.Config() if key in keys
    )
    logger.debug("Respond... \n%s", info)

    logger.debug("args: %s", args)

    # args.params contains "details" or "detail" or "详细"
    det = False
    if args is not None:
        det = any(map(lambda x: x in args.params, ["details", "detail", "详细"]))

    try:
        args_details = args.details
    except AttributeError:  # args.details not in namespace
        args_details = False

    if args_details or det:
        try:
            plugin_info = fetch_plugin_info(details=True)
        except Exception as e:
            logger.error("fetch_plugin_info() exc: %s", e)
            plugin_info = str(e)
        try:
            await bot.send(message=f"{info}\n{plugin_info}", event=event)

            # reset timer if sent successfully
            _vars["last_sent"] = time()
        except Exception as e:
            logger.error(e)
    else:
        try:
            plugin_info = fetch_plugin_info()
        except Exception as e:
            logger.error("fetch_plugin_info() exc: %s", e)
            plugin_info = str(e)
        try:
            await bot.send(message=f"{info}\n{plugin_info}", event=event)

            # reset timer if sent successfully
            _vars["last_sent"] = time()
        except Exception as e:
            logger.error(e)
