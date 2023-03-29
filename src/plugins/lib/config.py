import json


class ConfigClass: # 数据库配置类
    def __init__(self):
        self.database = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "port": 3306
        }
