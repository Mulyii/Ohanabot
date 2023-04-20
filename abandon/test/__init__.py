import pymysql
from nonebot import on_command
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.databaseclass import User
from lib.databaseclass import ContestTable
from nonebot.adapters.onebot.v11.message import Message
from lib.config import register_help, unregister_help
from lib.dependclass import response

test = on_command("test")


@test.handle()
async def _(qq_count: DependClass = Depends(DependClass, use_cache=False)):
    contest_table = ContestTable()
    for i in contest_table.find_all():
        print(i.to_string())
    await response(test, "finish", qq_count)
