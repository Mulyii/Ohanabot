from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.databaseclass import User
from lib.databaseclass import DataBase

cmd = "unregister"
unregister = on_command(cmd=cmd)


async def response(mes: str, uid=None):
    if uid == None:
        await unregister.finish(Message(f'{mes}'))
    else:
        await unregister.finish(Message(f'[CQ:at,qq={uid}] {mes}'))


def split_to_pair(s: str) -> list:
    ret: list = s.split(' ')
    [x.strip() for x in ret]
    return list(filter(lambda x: len(x) > 0, ret))


@unregister.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if qq_account.type == "group":
        await response("!!!仅限私聊!!!", qq_account.uid)
        return
    elif len(qq_account.message) == 0 or qq_account.message == "help":
        await response("""命令格式:
#unregister [姓名] [学号]
姓名和学号用一个空格隔开(不要输入[])
例：#unregister 张三 1234567890
注意：一旦注销账户，将会删除该账户的所有数据，不能找回""")
        return
    else:
        ls: list = split_to_pair(qq_account.message)
        if len(ls) != 2:
            await response("不合法的输入")
            return
        real_name, student_id = ls
        user = User(real_name=real_name, qq=qq_account.uid, student_id=student_id)
        db = DataBase()
        try:
            is_delete = db.users_delete(user)
            if is_delete > 0:
                await response("删除成功")
            else:
                await response("删除失败\n可能原因：姓名与学号不匹配或使用的qq非注册时使用的qq")
        except ValueError as e:
            await response(str(e))
