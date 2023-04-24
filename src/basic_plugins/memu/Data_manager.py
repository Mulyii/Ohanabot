import nonebot.plugin
from .DataStruct import Plugin_Menu_item
from nonebot.plugin import PluginMetadata
from nonebot import logger
from pydantic import error_wrappers
from typing import List
from nonebot.adapters.onebot.v11.message import Message
from nonebot_plugin_htmlrender import md_to_pic


class Data_manager(object):
    def __init__(self):
        self.plugins_menu_list: List[Plugin_Menu_item] = []
        self.plugins_menu_list_name: List[str] = []
        self.width = 500

    def load_plugin_info(self):
        def load_from_dict(_meta_data: PluginMetadata):
            self.plugins_menu_list.append(
                Plugin_Menu_item(
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
                        f"<g>{plugin.name} 菜单数据已加载</g>"
                    )
                except error_wrappers.ValidationError as e:
                    logger.opt(colors=True).error(
                        f"<r>{plugin.name} 菜单数据加载失败\n</r>"
                        f"<r>{e}</r>"
                    )
        self.plugins_menu_list.sort(key=lambda x: x.name.encode("utf-8"))
        self.plugins_menu_list_name = [
            id.name for id in self.plugins_menu_list]

    def set_with(self, width:int):
        self.width = width

    async def get_menu_names(self):
        menu_names = '<div align="center"><h1> 菜单 </h1></div>\n'
        id = 1
        for name in self.plugins_menu_list_name:
            menu_names += f'<div>\n'\
                f'{id} .  <strong>{name}</strong>\n'\
                f'</div>\n'
            id += 1
        return await md_to_pic(menu_names, width=self.width)

    async def get_details(self, plugin_id):
        plugin_item = self.plugins_menu_list[plugin_id - 1]
        details = f'* **名称**：{plugin_item.name}\n'\
            f'* **功能**：{plugin_item.description}\n' \
            f'* **用法**：{plugin_item.usage}'
        return await md_to_pic(details)
