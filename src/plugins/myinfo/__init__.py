import pymysql
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import PluginMetadata
from lib.dependclass import DependClass, response
from nonebot.params import Depends
from lib.databaseclass import User
from lib.databaseclass import UserTable

__plugin_meta__ = PluginMetadata(
    name="个人信息修改查看",
    description="查看和修改个人信息",
    usage="输入#myinfo查看个人信息\n输入#sethelp查看如何修改个人信息",
    extra={
        "unique_name": "myinfo",
        "author": "xcw <915759345@qq.com>",
        "version": "1.0.0"
    }
)

my_info = on_command("myinfo", aliases={"我的信息"})
set_help = on_command("sethelp", aliases={"修改信息帮助"})
set_info = on_command("setname", aliases={"setstuid", "setcodeforces"})


@my_info.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response(my_info, "!!!仅限私聊!!!", qq_account)
    else:
        db = UserTable()
        try:
            user = db.find_qq(qq_account.uid)
            if user is None:
                await response(my_info, "该账号未注册，请先用#register help查看注册方法", qq_account)
                return
            await response(my_info, user.to_string() + "\n若要修改信息，可使用#sethelp来查询修改方法", qq_account)
        except pymysql.IntegrityError as e:
            print(e)
            await response(my_info, "出错了QAQ，向管理员提交错误报告", qq_account)


@set_help.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response(set_help, "!!!仅限私聊!!!", qq_account)
    else:
        await response(set_help, """修改姓名 (不加[])
    #setname [姓名]
修改学号 (不加[])
    #setstuid [学号]
修改codeforces账号 (不加[])
    #setcodeforces [cf账号]""", qq_account)


@set_info.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response(set_info, "!!!仅限私聊!!!", qq_account)
    else:
        db = UserTable()
        user = db.find_qq(qq_account.uid)

        if user is None:
            await response(set_info, "该账号未注册，请先用#register help查看注册方法", qq_account)
            return

        print(qq_account.title)
        print(qq_account.message)

        if qq_account.title == "#setname":
            user.real_name = qq_account.message
        elif qq_account.title == "#setstuid":
            user.student_id = qq_account.message
        elif qq_account.title == "#setcodeforces":
            user.codeforces_id = qq_account.message

        if db.update(user.id, user):
            await response(set_info, "修改成功", qq_account)
        else:
            await response(set_info, "修改失败", qq_account)
