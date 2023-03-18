import pymysql
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from ..lib.dependclass import DependClass
from nonebot.params import Depends
from ..lib.databaseclass import User
from ..lib.databaseclass import DataBase

register = on_command("#register")


def split_to_pair(s: str) -> list:
    ret: list = s.split(' ')
    [x.strip() for x in ret]
    return list(filter(lambda x: len(x) > 0, ret))


@register.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    print("register recieved")
    print(qq_account.uid, qq_account.nickname, qq_account.message)
    response = ""
    if qq_account.type == "group":
        response = "!!!仅私聊可用!!!"
    elif len(qq_account.message) == 0 or qq_account.message == "help":
        response = """
命令格式:
#register [姓名] [学号]
姓名和学号用一个空格隔开(不要输入[])
例：#register 张三 1234567890
注意：一定要用真实姓名学号，若发现用虚假或别人的，会直接删除所有数据"""
    else:
        try:
            db = DataBase()
            if db.users_find_qq(qq_account.uid):
                response = "您已注册，若要再次注册，请输入#unregister注销账户"
            else:
                ls: list = split_to_pair(qq_account.message)
                if len(ls) != 2:
                    response = "不合法的输入"
                else:
                    real_name, student_id = ls
                    if db.users_find_stuid(student_id):
                        response = "该学生已注册"
                    else:
                        try:
                            print(f"real_name={real_name}, qq={qq_account.uid}, student_id={student_id}")
                            user = User(real_name=real_name, qq=qq_account.uid, student_id=student_id)
                            db.users_insert(user)
                            response = f"""注册成功！！！
姓名: {user.real_name}
qq号: {user.qq}
学号: {user.student_id}"""
                        except ValueError as e:
                            print(e)
                            response = "出错"
        except pymysql.IntegrityError as e:
            response = "数据库连接出错，请管理员报告错误"
    await register.finish(Message(f'[CQ:at,qq={qq_account.uid}] {response}'))