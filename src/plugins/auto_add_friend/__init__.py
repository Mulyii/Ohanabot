from nonebot import on_request, on_command
from nonebot.adapters.onebot.v11 import Bot, RequestEvent, FriendRequestEvent
from lib.dependclass import DependClass
from nonebot.params import Depends
from nonebot.adapters.onebot.v11.message import Message

add_friend = on_request(priority=1, block=True)
admin_qq = 915759345
@add_friend.handle()
async def handle_friend_request(bot: Bot, request_event: RequestEvent):
    if isinstance(request_event, FriendRequestEvent):
        # 好友申请
        print("收到好友申请")
        reqid = str(request_event.user_id)
        message = str(request_event.comment)
        flag = request_event.flag
        print(f"申请id: {reqid}， 验证消息: {message}")
        i = message.index(' ')
        if message[:i] == "ACMClub":
            await request_event.approve(bot, message[i + 1:])
            msg = f"已自动同意好友申请\nuid: {reqid}\ninfo:{message[i + 1:]}"
            await bot.send_private_msg(user_id=admin_qq, message=msg)
        else:
            await request_event.reject(bot)

add_help = on_command("addhelp")
@add_help.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    response = """添加bot的命令格式：
ACMClub [班级] [姓名] [学号]
如格式不符将不会添加好友，注意区分大小写和添加空格
请用真实的班级、姓名、学号"""
    await add_help.finish(Message(f'[CQ:at,qq={qq_account.uid}] {response}'))