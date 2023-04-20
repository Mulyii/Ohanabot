from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from lib.databaseclass import Problem
from nonebot.params import CommandArg
from nonebot import on_command, get_driver
from nonebot.matcher import Matcher
import lib.codeforcesAPI as cf
from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

multi_person_movement = on_command(
    "mpm",
    aliases={'多人运动', 'multi_person_movement'},
    priority=5,
    block=True
)

@multi_person_movement.handle()
async def _(matcher : Matcher, arg: Message = CommandArg()):
    dif = arg.extract_plain_text().strip()
    problem: Problem = None
    if not dif:
        problem = cf.random_rating_problem(1500)
    elif not dif.idfigit():
        await matcher.finish(f'输入一个合法的难度')
    else:
        dif = (int(dif) // 100) * 100
        if dif < 800:
            dif = 800
        elif dif > 3500:
            dif = 3500
        problem = cf.random_rating_problem(dif)
    await matcher.finish(f'这次的题目是{problem.url}\n请认真完成哦~')