from nonebot.adapters.onebot.v11.message import Message
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot import on_command, get_driver
from .Load_Data import Plugins_memu_list

__plugin_meta__ = PluginMetadata(
    name="菜单",
    description="这是一个菜单插件",
    usage="菜单啊",
)

driver = get_driver()

@driver.on_startup
async def _():
    plugins_memu_list.load_plugin_info()


plugins_memu_list = Plugins_memu_list()
memu_switch = True
memu = on_command("菜单", aliases={"memu", "帮助", "功能"}, priority=5, block=True)
switch_on = on_command("开启菜单", priority=5, permission=SUPERUSER, block=True)
switch_off = on_command("关闭菜单", priority=5, permission=SUPERUSER, block=True)

@switch_on.handle()
async def _(matcher: Matcher):
    global memu_switch
    memu_switch = True
    await matcher.finish("菜单已经开启")


@switch_off.handle()
async def _(matcher: Matcher):
    global memu_switch
    memu_switch = False
    await matcher.finish("菜单已经关闭")


@memu.handle()
async def _():
    msg = f'菜单\n'
    id = 1
    for plugin_name in plugins_memu_list.plugins_memu_list_name:
        msg += f'{id}.{plugin_name}\n'
        id += 1
    if memu_switch:
        await memu.finish(Message(msg))
