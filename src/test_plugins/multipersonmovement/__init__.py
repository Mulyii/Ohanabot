import asyncio
import datetime
from asyncio import TimerHandle
from typing import List

from nonebot.matcher import Matcher
from nonebot import on_command
from nonebot.params import Depends
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.plugin import PluginMetadata

import lib.codeforcesAPI as cf
from lib.databaseclass import Problem, User, UserTable
from lib.to_picture import table_to_pic
from lib.dependclass import DependClass
from lib.config import ConfigClass

__plugin_meta__ = PluginMetadata(
    name="多人运动(multi-person movement)",
    description="创建一场比赛或者加入一场正在进行的比赛",
    usage="输入#mpm创建一场比赛(难度可选, 默认1500), 例: #mpm 1400, 输入#join加入正在进行的比赛",
    extra={
        "unique_name": "multi-person_movement",
        "author": "xjq <466010106@qq.com>",
        "version": "1.0.0"
    }
)

multi_person_movement = on_command(
    "mpm",
    aliases={'多人运动', 'multi_person_movement', '多人比赛'},
    priority=5,
    block=True
)


class mpm:
    def __init__(self, problem: Problem, begin_time=datetime.datetime.now(), length: float = 3600):
        self.problem = problem
        self.joinPerson: List[tuple(User, str)] = []
        self.begin_time = begin_time
        self.length = length

    def addPerson(self, user: User, nickname:str):
        self.joinPerson.append((user, nickname))

    def get_url(self):
        return self.problem.url

    def get_tags(self):
        return self.problem.tags

    def get_length(self):
        return self.length


contest: mpm = None
timer: TimerHandle = None

config = ConfigClass()
user_table = UserTable()


def mpm_running():
    return contest != None


def check_accept(user: User):
    global contest
    if contest == None:
        return False
    # return cf.check_submission(user.codeforces_id, [int(contest.problem.contest_id), contest.problem.index], contest.begin_time, datetime.datetime.now())
    return cf.is_user_finished(user_name=user.codeforces_id, prob=contest.problem)


async def create_mpm(matcher: Matcher, dif: int = 1500):
    global contest
    contest = mpm(cf.random_rating_problem(dif))
    # contest = mpm(Problem("Timber", 1821, 'F', 'https://codeforces.com/problemset/problem/1821/F'))
    await matcher.finish(f'创建了一场比赛，比赛时间1h, 题目难度为{dif}，链接为:{contest.get_url()}, 输入#join可以加入这场比赛')


async def stop_mpm(matcher: Matcher):
    global contest
    global timer
    table: List[List[str]] = []
    headers = ['参赛选手', '通过状态']
    for user_name in contest.joinPerson:
        user = user_name[0]
        name = user_name[1]
        state = "Accepted" if check_accept(user) else "Rejected"
        table.append([name, state])
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
async def _(matcher: Matcher, qq_account: DependClass = Depends(DependClass, use_cache=False)):
    global contest
    if contest != None:
        await matcher.finish(f"现在正在进行的比赛是：{contest.get_url()}, 你可以输入#join加入这场比赛")
    dif = qq_account.message.strip()
    if not dif:
        set_timeout(matcher)
        await create_mpm(matcher)
    elif not dif.isdigit():
        await matcher.finish(f'请输入一个合法的难度')
    else:
        dif = (int(dif) // 100) * 100
        if dif < 800:
            dif = 800
        elif dif > 3500:
            dif = 3500
        set_timeout(matcher)
        await create_mpm(matcher, dif)

join = on_command(
    "join",
    aliases={'参加'},
    priority=5,
    block=True
)


@join.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    global contest
    if contest == None:
        await join.finish(f'没有正在进行的比赛，你可以发送#mpm创建一场比赛')
    user: User = user_table.find_qq(qq_account.uid)
    if user == None:
        await join.finish(f'请先注册')
    elif user.codeforces_id == '':
        await join.finish(f'请先绑定你的Codeforces账号')
    else:
        contest.addPerson(user, qq_account.nickname)
        await join.finish(Message(f'[CQ:at,qq={qq_account.uid}] 加入比赛成功'))
