import pymysql
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import GROUP_MEMBER
from ..lib.dependclass import DependClass
from nonebot.params import Depends
from ..lib.databaseclass import User
from ..lib.databaseclass import DataBase


my_info = on_command("myinfo")
set_help = on_command("sethelp")
set_name = on_command("setname")
set_stuid = on_command("setstuid")
set_codeforces = on_command("setcodeforces")

async def response(mes: str, uid=None):
    if uid == None:
        await my_info.finish(Message(f'{mes}'))
    else:
        await my_info.finish(Message(f'[CQ:at,qq={uid}] {mes}'))


@my_info.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response("!!!仅限私聊!!!", qq_account.uid)
    else:
        db = DataBase()
        try:
            info = db.users_find_qq(qq_account.uid)
            user = User(info["realname"], info["qq"], info["stuid"], info["codeforces"])
            await response(user.to_string() + "\n若要修改信息，可使用#sethelp来查询修改方法")
        except pymysql.IntegrityError as e:
            print(e)
            await response("出错了QAQ，向管理员提交错误报告")


@set_help.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response("!!!仅限私聊!!!", qq_account.uid)
    else:
        await response("""修改姓名 (不加[])
    #setname [姓名]
修改学号 (不加[])
    #setstuid [学号]
修改codeforces账号 (不加[])
    #setcodeforces [cf账号]""")

@set_name.handle()
@set_stuid.handle()
@set_codeforces.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response("!!!仅限私聊!!!", qq_account.uid)
    else:
        db = DataBase()
        info = db.users_find_qq(qq_account.uid)

        if info == None:
            await response("该账号未注册，请先用#register help查看注册方法")
            return

        print(qq_account.title)
        print(qq_account.message)

        if qq_account.title == "#setname":
            info["realname"] = qq_account.message
        elif qq_account.title == "#setstuid":
            info["stuid"] = qq_account.message
        elif qq_account.title == "#setcodeforces":
            info["codeforces"] = qq_account.message

        user = User(info["realname"], info["qq"], info["stuid"], info["codeforces"])

        if db.users_update(info["userid"], user):
            await response("修改成功")
        else:
            await response("修改失败")
