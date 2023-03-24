import nonebot.plugin
from .DataStruct import Plugin_Memu_item
from nonebot.plugin import PluginMetadata
from nonebot import logger
from pydantic import error_wrappers
from typing import List
class Plugins_memu_list(object):
    def __init__(self) :
        self.plugins_memu_list: List[Plugin_Memu_item] = []
        self.plugins_memu_list_name: List[str] = []

    def load_plugin_info(self) :
        def load_from_dict(_meta_data: PluginMetadata) :
            self.plugins_memu_list.append(
                Plugin_Memu_item (
                    name = _meta_data.name,
                    description = _meta_data.description,
                    usage = _meta_data.usage,
                    extra = _meta_data.extra,
                )
            )
        for plugin in nonebot.plugin.get_loaded_plugins():
            meta_data = plugin.metadata
            if meta_data is None:
                continue
            else :
                try :
                    load_from_dict(meta_data)
                    logger.opt(colors=True).success (
                        f"{plugin.name} 菜单数据已加载"
                    )
                except error_wrappers.ValidationError as e :
                    logger.opt(colors=True).error(
                        f"{plugin.name} 菜单数据加载失败\n"
                        f"{e}"
                    )
        self.plugins_memu_list.sort(key = lambda x : x.name.encode("gbk"))
        self.plugins_memu_list_name = [id.name for id in self.plugins_memu_list]
    

