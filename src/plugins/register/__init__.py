import pymysql
from nonebot import on_command
from nonebot.plugin import PluginMetadata

from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.databaseclass import User
from lib.databaseclass import UserTable
from lib.config import register_help, unregister_help
from lib.dependclass import response

__plugin_meta__ = PluginMetadata(
    name="注册/注销",
    description="完善个人信息以解锁更多功能, 注册前先添加机器人为好友，可以再help里查看",
    usage=register_help + "\n" + unregister_help,
    extra={
        "unique_name": "register",
        "example": "#register 张三 1234567890\n#unregister 张三 1234567890",
        "author": "xcw <915759345@qq.com>",
        "version": "1.0.0"
    }
)

register = on_command("register", aliases={"注册"})
unregister = on_command("unregister", aliases={"注销"})


def split_to_pair(s: str) -> list:
    ret: list = s.split(' ')
    [x.strip() for x in ret]
    return list(filter(lambda x: len(x) > 0, ret))


@register.handle()
async def register_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    print("register received")
    print(qq_account.uid, qq_account.nickname, qq_account.message)
    if qq_account.type == "group":
        await response(register, "仅私聊可用，请先添加机器人为好友，命令请通过#help查看", qq_account)
        return
    if len(qq_account.message) == 0 or qq_account.message == "help":
        await response(register, register_help, qq_account)
        return
    try:
        db = UserTable()
        if db.find_qq(qq_account.uid):
            await response(register, "您已注册，若要再次注册，请输入#unregister注销账户", qq_account)
            return
        ls: list = split_to_pair(qq_account.message)
        if len(ls) != 2:
            await response(register, "不合法的输入", qq_account)
            return
        real_name, student_id = ls
        if db.find_stuid(student_id):
            await response(register, "该学生已注册", qq_account)
            return
        try:
            print(f"real_name={real_name}, qq={qq_account.uid}, student_id={student_id}")
            user = User(real_name=real_name, qq=qq_account.uid, student_id=student_id)
            db.insert(user)
            await response(register, f"""注册成功！！！
姓名: {user.real_name}
qq号: {user.qq}
学号: {user.student_id}""", qq_account)
        except ValueError as e:
            print(e)
            await response(register, "出错", qq_account)
    except pymysql.IntegrityError as e:
        await response(register, "数据库连接出错，请管理员报告错误", qq_account)


@unregister.handle()
async def unregister_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response(unregister, "仅限私聊，请先添加机器人好友，命令请通过#help查看", qq_account)
        return
    elif len(qq_account.message) == 0 or qq_account.message == "help":
        await response(unregister, unregister_help, qq_account)
        return
    else:
        ls: list = split_to_pair(qq_account.message)
        if len(ls) != 2:
            await response(unregister, "不合法的输入", qq_account)
            return
        real_name, student_id = ls
        user = User(real_name=real_name, qq=qq_account.uid, student_id=student_id)
        db = UserTable()
        try:
            is_delete = db.delete(user)
            if is_delete > 0:
                await response(unregister, "删除成功", qq_account)
            else:
                await response(unregister, "删除失败\n可能原因：姓名与学号不匹配或使用的qq非注册时使用的qq", qq_account)
        except ValueError as e:
            await response(unregister, str(e), qq_account)
