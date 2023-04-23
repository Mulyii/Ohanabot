from nonebot import on_command
from nonebot.params import Depends
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.databaseclass import ContestTable
import requests
import random
import datetime
import time
from lib.codeforcesAPI import *
contest_info = on_command(
    "#contest",
    aliases={'最近比赛'},
    priority=1,
    block=True,
)

@contest_info.handle()
async def contest(user: DependClass = Depends(DependClass, use_cache=False)):
    # try:
    contest_infomation = get_recent_contests()
    try:
        final_contest = ""
        table = ContestTable()
        list1 = table.find_all()
    except:
        print("failed!")
    for member in list1:
        tmp = {'contest_id': 0, 'contest_name': '', 'start_time': datetime.datetime.now()}
        tmp['contest_id'] = member.id
        tmp['contest_name'] = member.name
        time_str = str(member.time)
        time_stamp = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
        # print(time_stamp)
        tmp['start_time'] = time_stamp
        contest_infomation.append(tmp)
    contest_infomation.sort(key=lambda x: x['start_time'])
    # print(contest_infomation)
    # final_contest += 'cf:'
    # final_contest += '\n'
    for member in contest_infomation:
        final_contest += member['contest_name']
        final_contest += '\n'
        timeStamp = member['start_time']
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        final_contest += otherStyleTime
        final_contest += '\n'
    # final_contest += '\n'

    await contest_info.finish("最近的比赛：\n{}".format(final_contest))
    # except:
    #     print("failed!")
