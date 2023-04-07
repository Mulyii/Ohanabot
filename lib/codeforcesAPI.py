############################################
# 调用codeforces提供的API的程序
#
############################################
import requests
import json
from lib.databaseclass import Problem
import datetime
from time import sleep

last_time = datetime.datetime.now()


def get_user_status(user_name: str):  # 获取用户提交列表
    # 设置时间间隔
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 1:
        sleep(0.5)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    url = f"https://codeforces.com/api/user.status?handle={user_name}"
    response = requests.get(url)

    data = json.loads(response.text)
    submissions = data["result"]
    ls = []
    for submission in submissions:
        if submission["verdict"] == "OK":
            ls.append(submission["problem"])
    return ls


def is_user_finished(user_name: str, prob: Problem):  # 查找用户该题是否通过
    problems = get_user_status(user_name)
    for problem in problems:
        if str(problem["contestId"]) + problem["index"] == prob.index:
            return True
    return False
