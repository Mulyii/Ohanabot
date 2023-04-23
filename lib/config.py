#################
# 数据库配置信息
#################
import json

welcome_word = """你好，我是ACM_Club的Q群机器人，很高心能为你服务"""

register_help = """命令格式:
·#register [姓名] [学号]
姓名和学号用一个空格隔开(不要输入[])
例：#register 张三 1234567890
注意：一定要用真实姓名学号，若发现用虚假或别人的，会直接删除所有数据"""

unregister_help = """命令格式:
·#unregister [姓名] [学号]
姓名和学号用一个空格隔开(不要输入[])
例：#unregister 张三 1234567890
注意：一旦注销账户，将会删除该账户的所有数据，不能找回"""

task_help = """123"""

class ConfigClass: # 数据库配置类
    def __init__(self):
        self.database = {
            "host": "47.115.207.251",
            "user": "root",
            "password": "ACMclub2021",
            "port": 3306
        }
