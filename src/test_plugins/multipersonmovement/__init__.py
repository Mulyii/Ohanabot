import asyncio
import datetime
from asyncio import TimerHandle
from typing import List

from nonebot.matcher import Matcher
from nonebot import on_command
from nonebot.params import CommandArg, Depends
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

import lib.codeforcesAPI as cf
from lib.databaseclass import Problem, User, UserTable
from lib.to_picture import table_to_pic
from lib.dependclass import DependClass



multi_person_movement = on_command(
    "mpm",
    aliases={'多人运动', 'multi_person_movement', '多人比赛'},
    priority=5,
    block=True
)


class mpm:
    def __init__(self, problem: Problem, begin_time=datetime.datetime.now()):
        self.problem = problem
        self.joinPerson: List[User] = []
        self.begin_time = begin_time

    def addPerson(self, user: User):
        self.joinPerson.append(user)

    def info(self):
        return self.problem.url


contest: mpm = None
timer: TimerHandle = None


def mpm_running():
    return contest != None


def check_accept(user: User):
    global contest
    if contest == None:
        return False
    return cf.check_submission(user.codeforces_id, contest.problem.write(), contest.begin_time, datetime.datetime.now())


async def create_mpm(matcher: Matcher, dif: int = 1500):
    global contest
    # contest = mpm(cf.random_rating_problem(dif))
    contest = mpm(Problem("Timber", 1821, 'F',
                  'https://codeforces.com/problemset/problem/1821/F'))
    await matcher.send(f'创建了一场比赛，题目难度为{dif}，链接为:{contest.info()}, 输入#join可以加入这场比赛')


async def stop_mpm(matcher: Matcher):
    global contest
    global timer
    table: List[List[str]] = []
    headers = ['参赛选手', '通过状态']
    for user in contest.joinPerson:
        state = "accepted" if check_accept(user) else "rejected"
        table.append([user.qq, state])
    contest = None
    timer = None
    await matcher.finish(Message(f'比赛结束，结果如下') + MessageSegment.image(await table_to_pic(f"比赛结果", headers, table)))


def set_timeout(matcher: Matcher, timeout: float = 3600):
    global timer
    loop = asyncio.get_running_loop()
    mytimer = loop.call_later(
        timeout, lambda: asyncio.ensure_future(stop_mpm(matcher))
    )
    timer = mytimer


@multi_person_movement.handle()
async def _(matcher: Matcher, arg: Message = CommandArg()):
    global contest
    if contest != None:
        await matcher.finish(f"现在正在进行的比赛是：{contest.info()}, 你可以输入#join加入这场比赛")
    dif = arg.extract_plain_text().strip()
    if not dif:
        await create_mpm(matcher)
    elif not dif.isdigit():
        await matcher.finish(f'请输入一个合法的难度')
    else:
        dif = (int(dif) // 100) * 100
        if dif < 800:
            dif = 800
        elif dif > 3500:
            dif = 3500
        await create_mpm(matcher, dif)
    set_timeout(matcher, 10)

join = on_command(
    "join",
    priority=5,
    block=True
)


@join.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    global contest
    if contest == None:
        join.finish(f'没有正在进行的比赛，你可以发送#mpm创建一场比赛')
    user = UserTable.find_qq(qq_account)
    if user != None:
        contest.addPerson(user)
        join.finish(f'加入比赛成功')
