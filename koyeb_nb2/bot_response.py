"""Get not response."""
# pylint: disable=invalid-name
import time
from fastlid import fastlid
import logzero
from logzero import logger
from koyeb_nb2.fetch_convbot import fetch_convbot
from koyeb_nb2.fetch_qinyunke import fetch_qinyunke

time.clock = time.perf_counter  # monkey patch for aiml lib
from koyeb_nb2.frenchbot import frenchbot
from koyeb_nb2.germanbot import germanbot

logzero.loglevel(10)


async def bot_response(text: str, lang: str = None) -> str:
    """Gen a response from multibots.

    en: convtbot, microsoft/DialoGPT small model, hosted on koyeb
    zh: qingyunke, free as of 202108
    de: aiml, TODO
    fr: aiml, TODO
    """
    # for recording convbot's previous response
    try:
        bot_response.convbot_prev_resp
    except AttributeError:
        bot_response.convbot_prev_resp = ""

    if lang is None:
        lang, conf = fastlid(text)

    if lang in ["zh"]:
        try:
            resp = await fetch_qinyunke(text)
        except Exception as e:
            logger.error("fetch_qinyunke exc: %s", e)
            raise
    elif lang in ["fr"]:
        try:
            resp = frenchbot(text)
        except Exception as e:
            logger.error("frenchbot exc: %s", e)
            raise
    elif lang in ["de"]:
        try:
            resp = germanbot(text)
        except Exception as e:
            logger.error("germanbot exc: %s", e)
            raise
    else:
        try:
            # resp = await fetch_convbot(text, bot_response.convbot_prev_resp)
            # bot_response.convbot_prev_resp = resp
            resp = await fetch_convbot(text)
        except Exception as e:
            logger.error("fetch_convbot exc: %s", e)
            raise

    return resp
