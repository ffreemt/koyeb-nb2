"""Send free_dict_wotd to groups: GRP_LIST: list, GRP_LIST0: list for nonebot2.

    GRP_LIST: about 3 messages per day
    GRP_LIST0: about 1.5 messages per day

---
https://v2.nonebot.dev/advanced/scheduler.html

from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', hour='*/2', id='xxx', args=[1], kwargs={arg2: 2})
async def run_every_2_hour(arg1, arg2):
    pass

scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")

from nonebot import require

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', second='*/13', id='xxx')
async def run_every_2_hour():
    # pass
    # logger.info("args: %s, kwargs: %s", args, kwargs)
    logger.info(" tick tick ")

scheduler.add_job(run_every_2_hour, "interval", days=1, id="xxx1")
"""
from random import randint
from time import time
from datetime import datetime, timedelta
import pytz
import logzero
from logzero import logger

import nonebot
from nonebot import require

from aiocqhttp.exceptions import Error as CQHttpError

from koyeb_nb2.free_dict_wotd import free_dict_wotd

scheduler = require("nonebot_plugin_apscheduler").scheduler
logzero.loglevel(10)

GRP_LIST = [
    399983941,  # verbal advantage
    # 182910943,  # freemdict
    316287378,  # ttw, not yet in the group, will be Exception
]
GRP_LIST0 = [
    672076603,
]  # CQHTTP 机器人大乱斗


# @nonebot.scheduler.scheduled_job('cron', hour='*', minute='14,29,44,59', second='59')
# @nonebot.scheduler.scheduled_job('cron', hour='*', minute='0,15,30,45')
# @scheduler.scheduled_job('cron', minute='*/1', id='run_quarterly')
@scheduler.scheduled_job("cron", minute="*/15", id="run_quarterly")
async def _():
    """Send wotd to ."""
    now = datetime.now(pytz.timezone("Asia/Shanghai"))
    now += timedelta(days=0, seconds=0.5)  # adjust .5 s

    # about three times a day
    # 4 quaters an hour: 4 * 24 = 96 quaters a day
    # 3/93 -> 3 /100
    prob = 3 / 100

    # if randint(0, 100) > 100:
    if randint(0, 100) > prob * 100:
        logger.debug(" none trigger at %s", str(now))
        return None
    logger.debug(" this triggers at %s", str(now))

    try:
        texts = free_dict_wotd(time() // (24 * 3600))  # same day uses cache
    except Exception as exc:
        texts = str(exc), ""

    message = (
        "**word & idiom of the day (http://www.thefreedictionary.com )**\n\n"
        + "\n\n".join(texts)
    )
    logger.debug("\t\t >==> now: %s", message[:20])

    bots = [*nonebot.get_bots().values()]
    bot = None
    if bots:
        bot, *_ = bots

    if not bot:
        return

    for group_id in GRP_LIST:
        # if group_id in GRP_LIST0:  # flip a coin
        if group_id in GRP_LIST0:  # flip a coin
            if randint(0, 1) == 0:
                continue  # skip by 50%

        try:
            await bot.send_group_msg(group_id=group_id, message=message)
        except CQHttpError as exc:
            # nonebot.logger.exception(exc)
            logger.debug("\n--Bummer-- CQHttpError: %s", exc)
        except Exception as exc:
            logger.debug("\n--Bummer2-- OtherError: %s", exc)
    try:
        await bot.send_private_msg(user_id=41947782, message=message)
    except CQHttpError as exc:
        nonebot.logger.exception(exc)
        logger.debug("\n--Bummer-- CQHttpError: %s", exc)
    except Exception as exc:
        logger.debug("\n--Bummer2-- OtherError: %s", exc)


# scheduler.add_job(run_quarterly, "interval", days=1, id="run_quarterly1")
