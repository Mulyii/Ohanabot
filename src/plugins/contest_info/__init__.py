from nonebot import on_command
from nonebot.params import Depends
from lib.dependclass import DependClass
from nonebot.params import Depends
import requests
import random
import datetime
from lib.codeforcesAPI import *
contest_info = on_command(
    "#contest",
    aliases={'最近比赛'},
    priority=1,
    block=True,
)

@contest_info.handle()
async def contest(user: DependClass = Depends(DependClass, use_cache=False)):
    contest_infomation = get_recent_contests()
    final_contest = ""
    contest_infomation.sort(key=lambda x: x['start_time'])
    for member in contest_infomation:
        final_contest += member['contest_name']
        final_contest += '\n'
        timeStamp = member['start_time']
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        final_contest += otherStyleTime
        final_contest += '\n'
    await contest_info.finish("最近一个月的比赛：\n{}".format(final_contest))