from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot import logger
from nonebot.params import ArgPlainText
from nonebot.params import Depends
from nonebot.exception import RejectedException
from lib.dependclass import DependClass
from .Chatbot import ChatBot
from nonebot.typing import T_State
import openai


__plugin_meta__ = PluginMetadata(
    name="GPT聊天",
    description="和chatGPT对话",
    usage="发送#chat命令开启一段对话"
)

openai.organization = "org-m1n1DhFATSP7eMph8SSP9mRF"

openai.api_key = "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"

chat_switch = True


async def chat_switch_rule():
    return chat_switch

switch_on = on_command(("chat", "on"), priority=5,
                       permission=SUPERUSER, block=True)
switch_off = on_command(("chat", "off"), priority=5,
                        permission=SUPERUSER, block=True)


@switch_on.handle()
async def _():
    global chat_switch
    chat_switch = True
    await switch_on.finish("聊天服务已经开启")


@switch_off.handle()
async def _():
    global chat_switch
    chat_switch = False
    await switch_off.finish("聊天服务已经关闭")


chat = on_command("chat", priority=50, block=False, rule=chat_switch_rule)



chatbots: dict[str, ChatBot] = {}
counters: dict[str, int] = {}


def bot_running(qq_account: DependClass):
    return bool(chatbots.get(qq_account.uid, None))


def stop_bot(qq_account: DependClass):
    if bot_running(qq_account):
        chatbots.pop(qq_account.uid)
        counters.pop(qq_account.uid)


@chat.got("query", prompt="现在有最多十次的对话机会，你可以在任何时候输入exit提前结束对话")
async def _(query: str = ArgPlainText(), qq_account: DependClass = Depends(DependClass, use_cache=False)):
    uid = qq_account.uid
    if not bot_running(qq_account):
        try:
            chatbots[uid] = ChatBot(uid)
            counters[uid] = 0
        except RuntimeError as e:
            logger.opt(colors=True).error(f"<r>gpt启动失败\n{e}</r>")
            chat.finish(f"出现了不可解决的问题，gpt启动失败")

    if counters[uid] >= 10 or query == 'exit':
        stop_bot(qq_account)
        await chat.finish(f"对话结束，感谢使用")
    else:
        counters[uid] += 1
    logger.info(counters[uid])
    try:
        await chat.reject(f"{chatbots[uid].ask(query)}")
    except Exception as e:
        if not isinstance(e, RejectedException):
            logger.opt(colors=True).error(f"<r>发生异常, {e} </r>")
            await chat.finish(f"发生异常")
