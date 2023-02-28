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
    await contests.finish(res)