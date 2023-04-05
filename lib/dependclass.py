####################################
# 这个Class将MessageEvent转换成一个处理
# 过的字典
####################################
import datetime
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import MessageEvent
from lib.databaseclass import InteractionMessage, InteractionTable


class DependClass:
    uid: str               # QQ号
    nickname: str          # QQ昵称
    message: str           # QQ消息
    type: str              # 群消息”group“， 私聊消息"private"
    title: str             # 触发头
    come_from: str         # 消息来源

    def __init__(self, event: MessageEvent):
        self.uid = str(event.get_user_id())
        self.nickname = str(event.sender.nickname)
        s = str(event.get_message())
        try:
            i = s.index(' ')
        except ValueError as e:
            i = len(s)

        self.message = s[i:].strip()
        self.title = s[:i].strip()
        self.type = event.message_type
        interaction = None
        if self.type == 'group':
            _, group_id, user_id = event.get_session_id().split("_")
            self.come_from = group_id
            interaction = InteractionMessage(datetime.datetime.now(), user_id, 'bot', 'group', group_id, self.message, self.title)
        elif self.type == 'private':
            user_id = event.get_session_id()
            self.come_from = user_id
            interaction = InteractionMessage(datetime.datetime.now(), user_id, 'bot', 'private', user_id, self.message, self.title)

        interaction_table = InteractionTable()
        interaction_table.insert(interaction)


async def response(receiver, mes: str, depend: DependClass):
    interaction = InteractionMessage(datetime.datetime.now(), 'bot', depend.uid,  depend.type, depend.come_from, mes, depend.title)
    interaction_table = InteractionTable()
    interaction_table.insert(interaction)
    if depend.type == "private":
        await receiver.finish(Message(f'{mes}'))
    elif depend.type == "group":
        await receiver.finish(Message(f'[CQ:at,qq={depend.uid}] {mes}'))

