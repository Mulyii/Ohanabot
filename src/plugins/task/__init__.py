from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from lib.dependclass import DependClass, response
from nonebot.params import Depends
from lib.databaseclass import User, Mission, Problem
from lib.databaseclass import MissionTable, UserTable, TaskTable, ProblemTable, DataBase
from lib.codeforcesAPI import is_user_finished

my_task = on_command("mytask")
my_task_finish = on_command("mytaskfinish")


def mission_problems(mission_id: int) -> list:
    try:
        db = DataBase()
        sql = f"select * from tasks, problems where tasks.missionid={mission_id} and tasks.problemid=problems.id"
        lines = db.exec(sql).fetchall()
        ret = []
        for line in lines:
            ret.append(Problem(id=0, name=str(line[4]), website=str(line[5]), index=str(line[6]), url=str(line[7])))
        return ret
    except ValueError as e:
        print("in task problems function error")
        return None


def problems_to_string(lines: list) -> str:
    if lines is None:
        return "ERROR\n"
    if len(lines) == 0:
        return "无作业\n"
    ret = ""
    for line in lines:
        ret += line.to_string() + '\n'

    return ret


def get_user(qq_account) -> User:
    user_table = UserTable()

    ret = user_table.find_qq(qq_account.uid)
    if ret is None:
        raise ValueError("出错！请联系管理员")

    return User(id=ret["userid"], real_name=ret["realname"], qq=ret["qq"], student_id=ret["stuid"], codeforces_id=ret["codeforces"], mission_id=ret["missionid"])


def get_mission(user: User) -> Mission:
    mission_table = MissionTable()

    ret = mission_table.find(user.mission_id)
    if ret is None:
        raise ValueError("出错！请联系管理员")

    return Mission(id=ret["missionid"], name=ret["missionname"], description=ret["description"])


@my_task.handle()
async def my_task_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    try:
        user = get_user(qq_account)
        mission = get_mission(user)
        await response(my_task, f"{mission.to_string()}\n需要完成的作业:\n{problems_to_string(mission_problems(mission.id))}(完成后才可进入下一任务)", qq_account)
    except ValueError as e:
        await response(my_task, str(e), qq_account)


@my_task_finish.handle()
async def my_task_finish_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    try:
        user = get_user(qq_account)
        mission = get_mission(user)
        probs = mission_problems(mission.id)
        flg = True
        for prob in probs:
            if not is_user_finished(user.codeforces_id, prob):
                flg = False
        if flg:
            next_mission = mission.find_next_mission(mission.id)
            if next_mission == "无":
                await response(my_task_finish, "完成所有任务啦!", qq_account)
                return
            if next_mission == "ERROR":
                await response(my_task_finish, "出错!", qq_account)
                return
            user.mission_id = next_mission.id
            user_table = UserTable()
            user_table.update(user.id, user)
            print(user.to_string())
            await response(my_task_finish, "你已完成所有作业，已跳转至下一任务", qq_account)
        else:
            await response(my_task_finish, "还有作业未完成", qq_account)
    except ValueError as e:
        await response(my_task_finish, str(e), qq_account)
