from nonebot import on_command
from nonebot.params import Depends
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.codeforcesAPI import *
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="每日一题",
    description="获取codeforces每日一题",
    usage="发送#everyday获取今日的题目"
)

problem_everyday = on_command(
    "everyday",
    aliases={'每日一题'},
    priority=5,
    block=True,
)

@problem_everyday.handle()
async def problem(user: DependClass = Depends(DependClass, use_cache=False)):
    code_url = output_random_problem_url()
    await problem_everyday.finish("今日随机选择的 Codeforces 题目是：{}\今天也要努力做题喵!".format(code_url))


set_difficulty = on_command(
    "set_difficulty",
    aliases={'设置难度'},
    priority=5,
    block=True,
)

def split_to_pair(s: str) -> list:
    ret: list = s.split(' ')
    [x.strip() for x in ret]
    return list(filter(lambda x: len(x) > 0, ret))

@set_difficulty.handle()
async def difficulty(user: DependClass = Depends(DependClass, use_cache=False)):
    if user.uid != "2737135395" and user.uid != "466010106" and user.uid != "2544372618" and user.uid != "915759345" and user.uid != "2698391451":
        await set_difficulty.finish("你不是管理员，无法设置难度!")
    else:
        try:
            mess = user.message
            list = split_to_pair(mess)
            min_rating = (int(list[0]) // 100) * 100
            max_rating = (int(list[1]) // 100) * 100
        except:
            await set_difficulty.finish(
                "请你输入难度区间命令，下限和上限用一个空格隔开(不要输入[])\n例：#set_difficulty 1500 2000")
        # print([min_rating, max_rating])
        if min_rating > 3000 or min_rating < 0:
            await set_difficulty.finish(
                "请你输入难度区间命令,下限和上限用一个空格隔开(不要输入[])\n例：#set_difficulty 1500 2000")
        if max_rating > 3000 or max_rating < 0:
            await set_difficulty.finish(
                "请你输入难度区间,下限和上限用一个空格隔开(不要输入[])\n例：#set_difficulty 1500 2000")
        if min_rating > max_rating:
            await set_difficulty.finish(
                "请你输入难度区间,下限和上限用一个空格隔开(不要输入[])\n例：#set_difficulty 1500 2000")
        print(min_rating, max_rating)
        set_mmin(min_rating)
        set_mmax(max_rating)
        update_random_problem_url()
        await set_difficulty.finish(
                "难度重设成功！")