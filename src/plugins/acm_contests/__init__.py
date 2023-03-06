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
<<<<<<< HEAD
    await contests.finish(res)
=======
    await contests.finish(res)
>>>>>>> 66b4f32c319738b298e6874c34cedf02b60bed34
