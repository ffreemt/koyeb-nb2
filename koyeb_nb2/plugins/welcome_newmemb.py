"""Test on_notice.

https://v2.nonebot.dev/guide/creating-a-matcher.html

https://blog.csdn.net/What_ever_Y/article/details/114807597
    https://www.codeleading.com/article/35095362545/
        https://zhuanlan.zhihu.com/p/373323656
https://github.com/cscs181/QQ-GitHub-Bot/blob/master/src/plugins/nonebot_plugin_status/__init__.py
"""
from nonebot import on_notice
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.event import GroupIncreaseNoticeEvent
from nonebot.adapters.cqhttp import Bot  # , Event

# from nonebot.rule import Rule

from jsonpath_ng import parse
import logzero
from logzero import logger

# from koyeb_nb2.jpmatch import jpmatch

logzero.loglevel(10)
GRP_NAME = dict(
    zip(
        [
            # 182910943,
            672076603,
            316287378,
        ],
        [
            # 'freemdict',
            "机器人大乱斗",
            "Transtoolweb+双语对齐",
        ],
    )
)

on_notice_ = on_notice()


def jpmatch(x, y):
    """Emulate jsonpath_ext_rw.

    >>> jpmatch("$..baz", {'foo': [{'baz': 1}, {'baz': 2}]})
    [1, 2]
    >>> jpmatch("foo[*].baz", {'foo': [{'baz': 1}, {'baz': 2}]})
    [1, 2]
    >>> jpmatch("$.foo[*].baz", {'foo': [{'baz': 1}, {'baz': 2}]})
    [1, 2]
    """
    return [elm.value for elm in parse(x).find(y)]


# async def _(session: NoticeSession):
@on_notice_.handle()
async def handle(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    """Test on_notice."""
    logger.info("state: %s", state)

    user_id = jpmatch("$.user_id", state)[0]
    group_id = jpmatch("$.group_id", state)[0]

    self_info = await bot.get_login_info()
    group_member_info = await bot.get_group_member_info(
        group_id=group_id, user_id=user_id, no_cache=True
    )
    logger.info(
        "***=> user_id %s, group_member_info: %s, self_info: %s",
        user_id,
        group_member_info,
        self_info,
    )

    nm_name = (
        jpmatch("$.card", group_member_info)[0]
        or jpmatch("$.nickname", group_member_info)[0]
    )
    group_id = jpmatch("$.group_id", group_member_info)[0]
    if group_id not in GRP_NAME:
        return None

    group_name = GRP_NAME.get(group_id)
    msg = f"欢迎 {nm_name} 加入{group_name}群。"
    if group_id in [182910943]:
        msg += "(请查看本群须知。)"
    # msg += '\n\n' + fetch_one()

    try:
        await bot.send(event=event, message=msg)
    except Exception as e:
        logger.error(e)

    try:
        # await session.send(msg)
        await handle.finish(f"sent via handle.finish: {msg}")
    except Exception as e:
        logger.error(e)


_ = """
    img_path = str(choices(IMG_LIST)[0])
    img_path = 'C:\\dl\\coolq-test\\utils\\welcome_img\\welcome-to-join-us.jpg'
    img = f'[CQ:image,file=file:///{img_path}]'

    try:
        await session.send(message=img)
    except Exception as exc:
        logger.error('session.send(message=img) exc: %s', exc)
"""

_ = """
answer = '[CQ: image, file=file:///D:/...]'
bot.send(context, message=answer)

In [59]: jpmatch('$..nickname', group_info)
Out[59]: ['无问西东']

nickname = jpmatch('$..nickname', group_info)[0]

nm_name = jpmatch('$.card', group_info)[0] or jpmatch('$.nickname', group_info)[0]
group_id = jpmatch('$.group_id', group_info)[0]


***=> ctx: {'group_id': 182910943, 'notice_type': 'group_increase', 'operator_id': 173881227, 'post_type': 'notice', 'self_id': 1919279707, 'sub_type': 'approve', 'time': 1547790883, 'user_id': 778943263}
"""
