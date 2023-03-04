from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from .web_crawler.cf_contests import codeforces_contests

contests = on_command (
    "contests",
    aliases = {'cf'},
    priority=20,
    block=True,
)
@contests.handle()
async def consest_handle(bot : Bot, event : Event) :
    res = codeforces_contests()
    meg = ""
    for na_ti in res :
        meg += "比赛名称：{}\n比赛时间：{}\n".format(na_ti[0], na_ti[1])
    await contests.finish(meg)