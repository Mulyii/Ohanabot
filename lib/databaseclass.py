import pymysql
from lib.config import ConfigClass
import datetime
import time
from typing import Optional

class Test:
    user_id: int
    math: int
    other: int
    structure: int
    dp: int
    geometry: int
    graphic: int
    strings: int

    def __init__(self, user_id, math, other, structure, dp, geometry, graphic, strings):
        self.user_id = user_id
        self.math = math
        self.other = other
        self.structure = structure
        self.dp = dp
        self.geometry = geometry
        self.graphic = graphic
        self.strings = strings

class Problem: # 数据库题目类
    name: str
    contest_id: int
    index: str
    url: str
    tags: list[str]

    def __init__(self, name: str, contest_id: int, index: str, url: str, tags: Optional[list] = None):
        self.name = name
        self.contest_id = contest_id
        self.index = index
        self.url = url
        self.tags = tags

    def to_string(self) -> str:
        return f"{self.website}{self.index} {self.name}: {self.url}\ntags: {','.join(self.tags)}\nrating: {self.rating}"

    def write(self) -> str:
        return f"{self.contest_id}{self.index}"

class Score: # 数据库成绩类
    contest_id: int
    user_id: int
    rank: int
    number: int
    penalty: int

    def __init__(self, contest_id: int, user_id: int, rank: int, number: int, penalty: int):
        self.contest_id = contest_id
        self.user_id = user_id
        self.rank = rank
        self.number = number
        self.penalty = penalty

class Contest: # 数据库比赛类
    id: int
    name: str
    time: datetime
    duration: time
    site: str

    def __init__(self, id: int, name: str, time: datetime, duration: time, site: str):
        self.id = id
        self.name = name
        self.time = time
        self.duration = duration
        self.site = site

    def to_string(self) -> str:
        return f"比赛名: {self.name}\n开始时间: {self.time}\n时长: {self.duration}"

class Mission: # 数据库任务类
    id: int = 0
    name: str
    description: str

    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def find_index(self, lines, mission_id: int):  #查找当前mission在序列中的位置
        for i, line in enumerate(lines):
            if line[0] == mission_id:
                return i
        return -1

    def calc_mission_rank(self, mission_id: int) -> str:  #查找mission的顺位，是第几个任务
        mission_table = MissionTable()
        lines = mission_table.find_all()

        return f"{self.find_index(lines, mission_id) + 1}/{len(lines)}"

    def find_next_mission(self, mission_id: int):  #查找下一个任务，如果不存在则输出“无”
        mission_table = MissionTable()
        lines = mission_table.find_all()

        ind: int = self.find_index(lines, mission_id)
        if ind == len(lines) - 1:
            return "无"
        else:
            mission = Mission(lines[ind + 1][0], lines[ind + 1][1], lines[ind + 1][2])
            return mission

        return "ERROR"

    def to_string(self):
        next_mission = self.find_next_mission(self.id)
        print(isinstance(next_mission, Mission))
        return f"""您现在的任务进度: {self.calc_mission_rank(self.id)}
任务名: {self.name}
详细信息: \n{self.description}
下一个任务: {next_mission.name if isinstance(next_mission, Mission) else next_mission}"""

class Task: # 数据库任务类
    id: int
    mission_id: int
    problem_id: int

    def __init__(self, id: int, mission_id: int, problem_id: int):
        self.id = id
        self.mission_id = mission_id
        self.problem_id = problem_id

class User: # 数据库用户类
    id: int
    real_name: str
    qq: str
    student_id: str
    codeforces_id: str
    mission_id: int

    def __init__(self, real_name: str, qq: str, student_id: str,codeforces_id: str = "",  id: int = 0, mission_id: int = 0):
        self.id = id
        self.real_name = real_name
        if not self.check_qq(qq):
            raise ValueError("qq账号格式不正确")
        self.qq = qq
        if not self.check_student_id(student_id):
            raise ValueError("学号格式不正确")
        self.student_id = student_id
        self.codeforces_id = codeforces_id
        self.mission_id = mission_id

    def check_qq(self, qq: str) -> bool: # 检查qq号格式是否正确
        for c in qq:
            if not('0' <= c <= '9'):
                return False
        return True

    def check_student_id(self, student_id: str) -> bool: # 检查学生学号是否正确
        if len(student_id) != 10:
            return False
        for c in student_id:
            if not('0' <= c <= '9'):
                return False
        return True

    def to_string(self) -> str:
        return f"""姓名: {self.real_name}
qq号: {self.qq}
学号: {self.student_id}
Codeforces账号: {self.codeforces_id}
当前的任务:{self.mission_id}"""

class InteractionMessage:
    sendtime: datetime
    sender: str
    reciever: str
    type_name: str
    come_from: str
    message: str
    command: str

    def __init__(self, sendtime, sender, reciever, type_name, come_from, message, command):
        self.sendtime = sendtime
        self.sender = sender
        self.reciever = reciever
        self.type_name = type_name
        self.come_from = come_from
        self.message = message
        self.command = command

class DataBase:
    db = None # 数据库对象
    con: ConfigClass # 数据库配置对象

    def __init__(self):
        try:
            con = ConfigClass()
            self.db = pymysql.connect(host=con.database["host"],
                                      user=con.database["user"],
                                      passwd=con.database["password"],
                                      port=con.database["port"],
                                      db="robot")
        except:
            raise ValueError("connect failure")

    def __del__(self):
        self.db.close()

    # 执行sql命令，如果执行失败抛出错误failure_info,执行成功控制台输出success_info
    def exec(self, sql: str, failure_info: str = "", success_info: str = ""):
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
            print(success_info)
            return cursor
        except:
            self.db.rollback()
            raise ValueError(failure_info)

class UserTable(DataBase):
    def __init__(self):
        super(UserTable, self).__init__()

    def insert(self, user: User): # users插入，无返回值
        sql = f"insert into users(realname, qq, stuid, codeforces) values('{user.real_name}', '{user.qq}', '{user.student_id}', '{user.codeforces_id}')"
        self.exec(sql, "In class UserTable function insert users insert failed")

    def delete(self, user: User): # users删除，返回删除行数
        sql = f"delete from users where realname='{user.real_name}' and qq='{user.qq}' and stuid='{user.student_id}'"
        return self.exec(sql, "In class UserTable function delete users delete failed").rowcount

    def find_all(self) -> list: # users查询，返回所有实例
        sql = f"select * from users"
        lines = self.exec(sql, "In class UserTable function find_all")
        ret = []
        for line in lines:
            ret.append(User(id=line[0], real_name=line[1], qq=line[2], student_id=line[3], codeforces_id=line[4], mission_id=line[5]))
        return ret

    def find_stuid(self, student_id: str) -> Optional[User]: # users学号查询，返回所有实例
        sql = f"select * from users where stuid='{student_id}'"
        cursor = self.exec(sql, "In class UserTable function find_stuid users select failed")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            tmp = dict(zip(columns, result))
            return User(id=tmp["userid"], real_name=tmp["realname"], qq=tmp["qq"], student_id=tmp["stuid"],
                        codeforces_id=tmp["codeforces"], mission_id=tmp["missionid"])
        else:
            return None

    def find_qq(self, qq: str) -> Optional[User]: # users qq号查询，返回所有实例
        sql = f"select * from users where qq='{qq}'"
        cursor = self.exec(sql, "In class UserTable function find_qq users select failed")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            tmp = dict(zip(columns, result))
            return User(id=tmp["userid"], real_name=tmp["realname"], qq=tmp["qq"], student_id=tmp["stuid"],
                        codeforces_id=tmp["codeforces"], mission_id=tmp["missionid"])
        else:
            return None

    def find_realname(self, real_name: str) -> list[User]: # users姓名查询，返回所有实例
        sql = f"select * from users where realname='{real_name}'"
        ret = []
        lines = self.exec(sql, "In class UserTable function find_realname users select failed").fetchall()
        for line in lines:
            ret.append(User(id=line[0], real_name=line[1], qq=line[2], student_id=line[3], codeforces_id=line[4], mission_id=line[5]))
        return ret

    def update(self, id: int, user: User): # users更新
        sql = f"update users set realname='{user.real_name}', qq='{user.qq}', stuid='{user.student_id}', codeforces='{user.codeforces_id}', missionid={user.mission_id} \
        where userid={id}"
        return self.exec(sql, "In class UserTable function update user update error").rowcount > 0

class MissionTable(DataBase):
    def __init__(self):
        super(MissionTable, self).__init__()

    def insert(self, mission: Mission):
        sql = f"insert into missions (missionid, missionname, description, nextmissionid) values ({mission.id}, '{mission.name}', '{mission.description}', {mission.next_id});"
        self.exec(sql, "In class MissionTable function insert mission insert error")

    def delete(self, mission: Mission):
        sql = f"delete from misssions where missionid={mission.id}"
        return self.exec(sql, "In class MissionTable function delete mission delete error").rowcount

    def update(self, id: int, mission: Mission):
        sql = f"update missions set missionname='{mission.name}', description='{mission.description}, nextmissionid={mission.next_id}' where missionid={id};"
        return self.exec(sql, "In class MissionTable function update mission update error").rowcount > 0

    def find(self, id: int) -> Mission:
        sql = f"select * from missions where missionid={id}"
        cursor = self.exec(sql, "In class MissinTable function find mission find error")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            tmp = dict(zip(columns, result))
            return Mission(id=tmp["mission"], name=tmp["missionname"], description=tmp["description"])
        else:
            return None

    def find_all(self) -> list[Mission]:
        sql = f"select * from missions"
        lines = self.exec(sql, "In class MissionTable function find_all mission find error").fetchall()
        ret = []
        for line in lines:
            ret.append(Mission(id=line[0], name=line[1], description=line[2]))
        return ret

class ProblemTable(DataBase):
    def __init__(self):
        super(Promblem, self).__init__()

    def insert(self, problem: Problem):
        sql = f"insert into problems (problemid, problemname, website, problemindex, url) values ({problem.id}, '{problem.name}', '{problem.website}', '{problem.index}', '{problem.url}');"
        self.exec(sql, "In class ProblemTable function insert problem insert error")

    def delete(self, problem: Problem):
        sql = f"delete from problems where problemid={problem.id}"
        return self.exec(sql, "In class ProblemTable function delete problem delete error").rowcount;

    def find(self, id: int) -> list[Problem]:
        sql = f"select * from problems where problemid={id}"
        lines = self.exec(sql, "In class ProblemTable function find problem find error").fetchall()
        ret = []
        for line in lines:
            ret.append(Problem(id=line[0], name=line[1], website=line[2], index=line[3], url=line[4]))
        return ret

class TaskTable(DataBase):
    def __init__(self):
        super(TaskTable, self).__init__()

    def find(self, id: int) -> list[Task]:
        sql = f"select * from tasks where problemid={id}"
        ret = []
        lines = self.exec(sql, "In class TaskTable function find task find error").fetchall()
        for line in lines:
            ret.append(Task(id=line[0], mission_id=line[1], problem_id=line[2]))
        return ret

class InteractionTable(DataBase):
    def __init__(self):
        super(InteractionTable, self).__init__()

    def insert(self, message: InteractionMessage):
        sql = f"insert into interactions(sendtime, sender, receiver, typename, comefrom, message, command) values " + \
              f"(\"{message.sendtime.strftime('%Y-%m-%d %H:%M:%S')}\", " + \
              f" \"{message.sender}\"," + \
              f" \"{message.reciever}\"," + \
              f" \"{message.type_name}\"," + \
              f" \"{message.come_from}\"," + \
              f" \"{message.message}\"," + \
              f" \"{message.command}\");"
        print(sql)
        self.exec(sql, "In class InteractionTable function insert error")

class ContestTable(DataBase):
    def __init__(self):
        super(ContestTable, self).__init__()

    def find_all(self) -> list[Contest]:
        sql = f"select * from contests"
        lines = self.exec(sql)
        ret = []
        for line in lines:
            ret.append(Contest(line[0], line[1], line[2], line[3], line[4]))

        return ret

class ScoreTable(DataBase):
    def __init__(self):
        super(ScoreTable, self).__init__()

    def find(self, user_id: int) -> list[Score]:
        sql = f"select * from scores where userid={user_id}"
        lines = self.exec(sql)
        ret = []
        for line in lines:
            ret.append(Score(line[0], line[1], line[2], line[3], line[4]))

        return ret

class TestTable(DataBase):
    def __init__(self):
        super(TestTable, self).__init__()

    def insert(self, test : Test):
        sql = f"insert into tests(id, math, other, struc, dp, geo, grap, str) values ({test.user_id}, {test.math}, {test.other}, {test.structure}, {test.dp}, {test.geometry}, {test.graphic}, {test.strings});"
        print(sql)
        self.exec(sql, "In class TestTable function insert test insert error")

    def update(self, test: Test):
        sql = f"update tests set math = {test.math}, other = {test.other}, struc = {test.structure}, dp = {test.dp}, geo = {test.geometry}, grap = {test.graphic}, str = {test.strings} where id = {test.user_id};"
        return self.exec(sql, "In class TestTable function update test update error").rowcount > 0

    def find(self, id: int) -> Optional[Test]:
        sql = "select * from tests"
        lines = self.exec(sql, "In class TestTable function find test update error").fetchall()
        print(lines)
        if len(lines) == 0:
            return None
        line = lines[0]
        print(line)
        return Test(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7])

__all__ = {
    "User",
    "Task",
    "Score",
    "Contest",
    "Problem",
    "Mission",
    "DataBase",
    "UserTable",
    "TaskTable",
    "ScoreTable",
    "MissionTable",
    "ProblemTable",
    "ContestTable",
    "InteractionTable",
    "InteractionMessage"
}
