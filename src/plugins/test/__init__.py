from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Depends
import pymysql as sql



test = on_command(
    "test",
    aliases={},
    priority=1,
    block=True,
)

class DependClass:
    def __init__(self, event: MessageEvent):
        self.uid = event.get_user_id()
        self.nickname = event.sender.nickname
        s = str(event.get_message())
        self.message = s[5:]
        self.message.strip()

@test.handle()
async def _(user: DependClass = Depends(DependClass, use_cache=False)):
    print(user.uid, user.nickname, user.message)
    try:
        db = sql.connect(host='localhost', user='root', passwd='root', port=3306)
        print("connect success")
    except:
        print("connect failure")
    await test.finish(Message(f'[CQ:at,qq={user.uid}] 你的uid为{user.uid}, 你的昵称是{user.nickname}, 你发送的消息为:{user.message}'))