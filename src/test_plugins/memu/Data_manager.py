import nonebot.plugin
from .DataStruct import Plugin_Memu_item
from nonebot.plugin import PluginMetadata
from nonebot import logger
from pydantic import error_wrappers
from typing import List
from nonebot.adapters.onebot.v11.message import Message
from nonebot_plugin_htmlrender import md_to_pic


class Data_manager(object):
    def __init__(self):
        self.plugins_memu_list: List[Plugin_Memu_item] = []
        self.plugins_memu_list_name: List[str] = []

    def load_plugin_info(self):
        def load_from_dict(_meta_data: PluginMetadata):
            self.plugins_memu_list.append(
                Plugin_Memu_item(
                    name=_meta_data.name,
                    description=_meta_data.description,
                    usage=_meta_data.usage,
                    extra=_meta_data.extra,
                )
            )
        for plugin in nonebot.plugin.get_loaded_plugins():
            meta_data = plugin.metadata
            if meta_data is None:
                continue
            else:
                try:
                    load_from_dict(meta_data)
                    logger.opt(colors=True).success(
                        f"{plugin.name} 菜单数据已加载"
                    )
                except error_wrappers.ValidationError as e:
                    logger.opt(colors=True).error(
                        f"{plugin.name} 菜单数据加载失败\n"
                        f"{e}"
                    )
        self.plugins_memu_list.sort(key=lambda x: x.name.encode("gbk"))
        self.plugins_memu_list_name = [
            id.name for id in self.plugins_memu_list]

    async def get_memu_names(self):
        memu_names = '<div align="center">\n <h1> 菜单 </h1> \n</div>'
        id = 1
        for name in self.plugins_memu_list_name:
            memu_names += f"* {id} .  **{name}**\n"
            id += 1
        return await md_to_pic(memu_names)

    async def get_details(self, plugin_id):
        details: Message = f''
        if plugin_id <= len(self.plugins_memu_list_name):
            plugin_item = self.plugins_memu_list[plugin_id - 1]
            details = f'* **名称**：{plugin_item.name}\n'\
                f'* **功能**：{plugin_item.description}\n' \
                f'* **用法**：{plugin_item.usage}'
        else:
            details = f'请输入正确的编号\n'
        return await md_to_pic(details)
