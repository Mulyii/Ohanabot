from nonebot import on_request, on_command
from nonebot.adapters.onebot.v11 import Bot, RequestEvent, FriendRequestEvent
from lib.dependclass import DependClass, response
from nonebot.params import Depends
from lib.config import welcome_word
from lib.databaseclass import InteractionTable, InteractionMessage
from nonebot.plugin import PluginMetadata
import datetime

__plugin_meta__ = PluginMetadata(
    name="添加机器人为好友",
    description="添加机器人为好友",
    usage="以ACMClub开头，后面加备注信息（班级姓名学号）\n例：ACMClub 计科1001 张三 1000000000",
    extra={
        "unique_name": "addhelp",
        "author": "xcw <915759345@qq.com>",
        "version": "1.0.0"
    }
)

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

        interaction = InteractionMessage(datetime.datetime.now(), reqid, 'bot', 'add friend', reqid, message, 'add friend')
        interaction_table = InteractionTable()
        interaction_table.insert(interaction)
        try:
            i = message.index(' ')
        except:
            await request_event.reject(bot)
            return

        if message[:i] == "ACMClub":
            await request_event.approve(bot, message[i + 1:])
            msg = f"已自动同意好友申请\nuid: {reqid}\ninfo:{message[i + 1:]}"
            await bot.send_private_msg(user_id=admin_qq, message=msg)
        else:
            await request_event.reject(bot)

add_help = on_command("addhelp")


@add_help.handle()
async def _(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    mes = """添加bot的命令格式：
ACMClub [班级] [姓名] [学号]
如格式不符将不会添加好友，注意区分大小写和添加空格
请用真实的班级、姓名、学号"""
    await response(add_help, mes, qq_account)
