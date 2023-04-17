from nonebot import on_command
from nonebot.params import Depends
from lib.dependclass import DependClass
from nonebot.params import Depends
import requests
import random
from lib.codeforcesAPI import *
problem_everyday = on_command(
    "#everyday",
    aliases={'每日一题'},
    priority=1,
    block=True,
)

@problem_everyday.handle()
async def problem(user: DependClass = Depends(DependClass, use_cache=False)):
    code_url = output_random_problem_url()
    await problem_everyday.finish("今日随机选择的 Codeforces 题目是：{}".format(code_url))
