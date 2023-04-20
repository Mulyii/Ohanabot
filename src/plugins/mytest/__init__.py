from nonebot import on_command
from lib.dependclass import DependClass, response, send
from nonebot.params import Depends, Event, Received
from lib.databaseclass import UserTable, TestTable, User, Test
import os
from lib.codeforcesAPI import random_rating_problem, is_user_finished, ask_for_problem_tag
from nonebot_plugin_apscheduler import scheduler
from lib.config import ConfigClass
from datetime import datetime, timedelta
import random

mytest_start = on_command("myteststart")
mytest_finish = on_command("mytestfinish")
config = ConfigClass()
user_table = UserTable()
test_table = TestTable()
def rating_func(diff: int):
    return diff // 100 * 100

@mytest_start.handle()
async def mytest_start_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    user = user_table.find_qq(qq_account.uid)
    if user is None:
        await response(mytest_start, "请先注册", qq_account)
        return
    if user.codeforces_id == "":
        await response(mytest_start, "请设置你的Codeforces账号名", qq_account)
        return
    test = test_table.find(user.id)
    if test is None:
        test_table.insert(Test(user.id, 0, 0, 0, 0, 0, 0, 0))
    save_file = "./data/" + str(qq_account.uid) + "info.txt";
    if not os.path.exists(save_file):
        file = open(save_file, 'w')
        file.close()
    with open(save_file, "r") as f:
        lines = f.readlines()
    if not lines == [] and len(lines[-1].split(' ')) < 5:
        await response(mytest_start, "你的上一个测试还没有完成, 请输入#mytestfinish结束上次测试", qq_account)
        return
    print("i1")
    difficulty = rating_func(random.randint(config.test["minrating"], config.test["maxrating"]))
    problem = random_rating_problem(difficulty)

    end_time = datetime.now() + timedelta(hours=1)
    print("i2")
    with open(save_file, "a") as f:
        f.write(f"{problem.contest_id}{problem.index} {difficulty} {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    await response(mytest_start, f"{problem.url}\n时间限制1h\n结束时间{end_time.strftime('%Y-%m-%d %H:%M:%S')}\n完成后使用#mytestfinish命令进入下一个测试", qq_account)

@mytest_finish.handle()
async def mytest_finish_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    print("finish")
    save_file = "./data/" + str(qq_account.uid) + "info.txt";
    with open(save_file, "r") as f:
        lines = f.readlines()

    args = lines[-1].split(' ')
    print(args)
    if len(args) != 4:
        response(mytest_finish, "您已经完成上一任务，输入#myteststart进行下一任务")
        return

    user = user_table.find_qq(qq_account.uid)
    timestr = args[2] + " " + args[3]
    tm = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    if not is_user_finished(user.codeforces_id, args[0]):
        state = 1
    elif datetime.now() > tm:
        state = 2
    else:
        state = 0

    with open(save_file, "a") as f:
        f.write(" T\n" if state == 0 else " F\n")

    if state == 0:
        score = {"数学": 0,
                 "杂耍": 0,
                 "数据结构": 0,
                 "动态规划": 0,
                 "几何": 0,
                 "图论": 0,
                 "字符串": 0 }

        args = lines[-1].split(' ')
        problem_id = [int(args[0][:-1]), args[0][-1]]
        tags = ask_for_problem_tag(problem_id)
        rating = int(args[1])
        for tag in tags:
            score[tag] = max(score[tag], rating)

        test = test_table.find(user.id)
        test.math = max(test.math, score["数学"])
        test.other = max(test.other, score["杂耍"])
        test.structure = max(test.structure, score["数据结构"])
        test.dp = max(test.dp, score["动态规划"])
        test.geometry = max(test.geometry, score["几何"])
        test.graphic = max(test.graphic, score["图论"])
        test.strings = max(test.strings, score["字符串"])
        test_table.update(test)

    relist = ["完成", "未完成", "未在规定时间内完成"]
    await response(mytest_finish, f"上一个任务已结束，你的任务状态为{relist[state]}", qq_account)
