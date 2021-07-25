r'''Provide brief help on all plugins.

nonebot.argparse
https://docs.nonebot.dev/api.html#nonebot-argparse-%E6%A8%A1%E5%9D%97
USAGE = r"""
创建计划任务

使用方法：
XXXXXX
""".strip()

@on_command('schedule', shell_like=True)
async def _(session: CommandSession):
    parser = ArgumentParser(session=session, usage=USAGE)
    parser.add_argument('-S', '--second')
    parser.add_argument('-M', '--minute')
    parser.add_argument('-H', '--hour')
    parser.add_argument('-d', '--day')
    parser.add_argument('-m', '--month')
    parser.add_argument('-w', '--day-of-week')
    parser.add_argument('-f', '--force', action='store_true', default=False)
    parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('--name', required=True)
    parser.add_argument('commands', nargs='+')

    args = parser.parse_args(session.argv)  # nb1?
    name = args.name
    # ...
'''