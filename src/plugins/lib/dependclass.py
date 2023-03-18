####################################
# 这个Class将MessageEvent转换成一个处理
# 过的字典
####################################
from nonebot.adapters.onebot.v11 import MessageEvent


class DependClass:
    uid: str               # QQ号
    nickname: str          # QQ昵称
    message: str           # QQ消息
    type: str              # 群消息”group“， 私聊消息"private"

    def __init__(self, event: MessageEvent):
        self.uid = str(event.get_user_id())
        self.nickname = str(event.sender.nickname)
        s = str(event.get_message())
        self.message = s.strip()
        self.type = event.message_type

    def delete_front_message(self, p: int):    # 删除message字符串开头p个数（去空白）
        self.message = self.message[p:].strip()
