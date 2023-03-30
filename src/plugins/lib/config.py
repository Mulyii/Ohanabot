#################
# 数据库配置信息
#################
import json

welcome_word = """你好，我是ACM_Club的Q群机器人，很高心能为你服务"""
class ConfigClass: # 数据库配置类
    def __init__(self):
        self.database = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "port": 3306
        }
