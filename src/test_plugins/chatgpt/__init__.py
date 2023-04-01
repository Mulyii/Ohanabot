from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot import logger
from nonebot.params import ArgPlainText
from nonebot.params import Depends

from ...plugins.lib.dependclass import DependClass
from .Chatbot import ChatBot
from nonebot.typing import T_State
import openai


__plugin_meta__ = PluginMetadata(
    name="GPT聊天",
    description="和chatGPT对话",
    usage="发送chat命令开启一段对话"
)

openai.organization = "org-m1n1DhFATSP7eMph8SSP9mRF"
openai.api_key = "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"

chat_switch = True

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


chat = on_command("chat", priority=50, block=True)


chatbot: ChatBot = None


@chat.got("query", prompt="现在有最多十次的对话机会，你可以在任何时候输入exit提前结束对话")
async def _(state: T_State, query: str = ArgPlainText(), qq_account: DependClass = Depends(DependClass, use_cache=False)):
    if not chat_switch:
        chat.finish(f"很抱歉，该功能暂时关闭使用")
    global chatbot
    try_count = state.get("try_count", 1)
    if try_count == 1:
        try:
            chatbot = ChatBot(qq_account.uid)
        except RuntimeError as e:
            logger.opt(colors=True).error(f"<r>gpt启动失败\n{e}</r>")
            chat.finish(f"出现了不可解决的问题，gpt启动失败")

    if try_count >= 10:
        await chat.finish(f"已达次数上限，感谢使用")
    state["try_count"] = try_count + 1

    if query == "exit":
        await chat.finish(f"感谢使用")
    else:
        try:
            await chat.reject(f"{chatbot.ask(query)}")
        except Exception as e:
            logger.opt(colors=True).error(f"<r>发生异常, {e} </r>")
            await chat.reject(f"发生异常")
