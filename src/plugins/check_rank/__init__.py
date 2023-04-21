from nonebot import on_command
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.codeforcesAPI import *
from lib.to_picture import *
from lib.dependclass import DependClass
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Codeforces rating 排名",
    description="查看已注册选手的 Codeforces rating 排名",
    usage="发送#rating查看排名"
)
check_rank = on_command(
    "rating",
    aliases={'查看排名'},
    priority=1,
    block=True,
)
@check_rank.handle()
async def rating(user: DependClass = Depends(DependClass, use_cache=False)):
    sorted_user_rating = get_user_rating()
    list = []
    print(sorted_user_rating)
    for user_rating in sorted_user_rating:
        user_id, rating = user_rating
        list.append([user_id, str(rating)])
    # print(list)
    await check_rank.finish(MessageSegment.image(await table_to_pic("ZJGSUcodeforce 排行", ["codeforce id","rating"], list)))