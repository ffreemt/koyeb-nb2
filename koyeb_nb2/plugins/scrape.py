"""Scrape text from a url."""
import asyncio
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import textwrap
import logzero
from logzero import logger

import nonebot
from nonebot import on_command

# from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event

# from nonebot.adapters.cqhttp import MessageSegment

from koyeb_nb2.url2txt import url2txt
from koyeb_nb2.parse_cmd import parse_cmd

logzero.loglevel(10)
logger.debug("debug test: %s", __file__)
logger.info("%s loaded", __file__)

scrape = on_command(
    "scrape", aliases={"爬", "fetch", "crawl", }, priority=2,
)  # shell_like=True)

_vars = {}  # store args in handle() for possible use in receive()


@scrape.handle()
async def handle(bot: Bot, event: Event, state: dict):
    """Scrape a url's mainbody text.

    url2txt(
        url: str,
        bodywidth: Optional[int] = 5000,
        remove: bool = False,
        show_url: bool = True,
        ignore_links: bool = True,
    ) -> str:
    """

    logger.debug("state: %s", state)

    parser = ArgumentParser(
        prog="scrape", formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", nargs="?", help="url of the desired page")
    parser.add_argument(
        "--bodywidth", type=int, default=5000, help="for displaying text"
    )
    parser.add_argument("--remove", action="store_true", help="removal of blank lines")
    parser.add_argument(
        "--show_url", action="store_true", help="show url in the begenning"
    )
    parser.add_argument(
        "--ignore_links", action="store_false", help="ignore links in text"
    )

    command = str(event.message).strip()

    args, stdout, stderr = parse_cmd(command, parser)
    logger.debug("args: %s", args)

    _vars.update({"args": args})
    logger.debug("_vars: %s", _vars)

    if stdout or stderr:
        await scrape.finish("\n---\n".join([stdout, stderr]))
        return None

    if not args.url:
        await scrape.send("Provide a url")
        return None

    try:
        text = url2txt(
            args.url, args.bodywidth, args.remove, args.show_url, args.ignore_links,
        )
    except Exception as e:
        logger.error(e)
        await scrape.finish(
            f"Errors: {e}. Perhaps the url is incorrect or it cant be scraped. Give amended url or another url."
        )
        return None

    width = min(args.bodywidth, 1000)

    try:
        await send_text(text, scrape, width)
    except Exception as e:
        logger.error("send_text exc: %s", e)
        # await scrape.finish(f"Errors: {e}")


@scrape.receive()
async def receive(bot: Bot, event: Event, state: dict):
    """Process when handle exits with scrape.send."""
    logger.debug("state: %s", state)
    try:
        url = str(event.message).strip()
        logger.debug("url: %s", url)
    except Exception as e:
        logger.error(e)
        await scrape.finish(f"Errors: {e}")
        return None

    args = _vars.get("args")
    if args is None:
        _ = "args is None, something has gone awry, exiting."
        logger.error(_)
        await scrape.finish(_)
        return None

    try:
        text = url2txt(
            url, args.bodywidth, args.remove, args.show_url, args.ignore_links,
        )
    except Exception as e:
        logger.error(e)
        await scrape.send(
            f"Errors: {e}. Perhaps the url is incorrect or it cant be scraped. Give amended url or another url."
        )
        return None

    width = min(args.bodywidth, 1000)

    try:
        await send_text(text, scrape, width)
    except Exception as e:
        logger.error("send_text exc: %s", e)
        # await scrape.finish(f"Errors: {e}")


async def send_text(text: str, matcher: nonebot.matcher.Matcher, width: int = 70):
    """Send text via matcher."""
    text_list = textwrap.wrap(
        text,
        width=width,
        replace_whitespace=False,
        break_long_words=False,
        break_on_hyphens=False,
        drop_whitespace=False,
    )

    try:
        for seg in text_list[:-1]:
            await matcher.send(seg)
            await asyncio.sleep(0.2)
    except Exception as e:
        logger.error(" for seg loop exc: %s", e)
        await matcher.finish(f"{e}")
    await matcher.finish(text_list[-1])
