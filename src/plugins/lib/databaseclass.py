import pymysql
from ..lib.config import ConfigClass
import datetime

class Problem: # 数据库题目类
    id: int
    name: str
    website: str
    index: str
    url: str

    def __init__(self, url: str, id: int, name: str, number: str):
        self.url = url
        self.id = id
        self.name = name
        self.number = number

    def to_string(self) -> str:
        return f"题目名称: {self.name}\n题目编号: {self.number}\n题目网址: {self.url}"

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
    time: str
    duration: str

    def __init__(self, id: int, name: str, time: datetime, duration: datetime):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.duration = duration

class Mission: # 数据库任务类
    id: int
    name: str
    description: str
    next_id: int

    def __init__(self, id: int, name: str, description: str, next_id: int):
        self.id = id
        self.name = name
        self.description = description
        self.next_id = next_id

class task: # 数据库任务类
    mission_id: int
    problem_id: int

    def __init__(self, mission_id: int, problem_id: int):
        self.mission_id = mission_id
        self.problem_id = problem_id

class User: # 数据库用户类
    id: int
    real_name: str
    qq: str
    student_id: str
    codeforces_id: str
    mission_id: int
    mission_name: str

    def __init__(self, real_name: str, qq: str, student_id: str, codeforces_id: str = "", id: int = 0):
        self.id = id
        self.real_name = real_name
        if not self.check_qq(qq):
            raise ValueError("qq账号格式不正确")
        self.qq = qq
        if not self.check_student_id(student_id):
            raise ValueError("学号格式不正确")
        self.student_id = student_id
        self.codeforces_id = codeforces_id

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
当前的任务:{self.mission_name}"""


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
            print("connect success")
        except:
            print("connect failure")
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

    def find_all(self): # users查询，返回所有实例
        sql = f"select * from users"
        return self.exec(sql, "In class UserTable function find_all").fetchall()

    def find_stuid(self, student_id: str): # users学号查询，返回所有实例
        sql = f"select * from users where stuid='{student_id}'"
        cursor = self.exec(sql, "In class UserTable function find_stuid users select failed")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            return dict(zip(columns, result))
        else:
            return None

    def find_qq(self, qq: str): # users qq号查询，返回所有实例
        sql = f"select * from users where qq='{qq}'"
        cursor = self.exec(sql, "In class UserTable function find_qq users select failed")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            return dict(zip(columns, result))
        else:
            return None

    def find_realname(self, real_name: str): # users姓名查询，返回所有实例
        sql = f"select * from users where realname='{real_name}'"
        return self.exec(sql, "In class UserTable function find_realname users select failed").fetchall()

    def update(self, id: int, user: User): # users更新
        sql = f"update users set realname='{user.real_name}', qq='{user.qq}', stuid='{user.student_id}', codeforces='{user.codeforces_id}' \
        where userid={id}"
        return self.exec(sql, "In class UserTable function update user update error").rowcount > 0

class MissionTable(DataBase):
    def __init__(self):
        super(Mission, self).__init__()

    def insert(self, mission: Mission):
        sql = f"insert into missions (missionid, missionname, description, nextmissionid) values ({mission.id}, '{mission.name}', '{mission.description}', {mission.next_id});"
        self.exec(sql, "In class MissionTable function insert mission insert error")

    def delete(self, mission: Mission):
        sql = f"delete from misssions where missionid={mission.id}";
        return self.exec(sql, "In class MissionTable function delete mission delete error").rowcount;

    def update(self, id: int, mission: Mission):
        sql = f"update users set missionname='{mission.name}', description='{mission.description}, nextmissionid={mission.next_id}' where missionid={id};"
        return self.exec(sql, "In class MissionTable function update mission update error").rowcount > 0

    def find(self, id: int):
        sql = f"select * from where missionid={id}"
        return self.exec(sql, "In class MissionTable function find mission find error").fetchall()

class ProblemTable(DataBase):
    def __init__(self):
        super(Promblem, self).__init__()

    def insert(self, problem: Problem):
        sql = f"insert into problems (problemid, problemname, website, problemindex, url) values ({problem.id}, '{problem.name}', '{problem.website}', '{problem.index}', '{problem.url}');"
        self.exec(sql, "In class ProblemTable function insert problem insert error")

    def delete(self, problem: Problem):
        sql = f"delete from problems where problemid={problem.id}"
        return self.exec(sql, "In class ProblemTable function delete problem delete error")

    def find(self, id: int):
        sql = f"select * from where problemid={id}"
        return self.exec(sql, "In class ProblemTable function find problem find error").fetchall()

class TaskTable(DataBase):
    def __init__(self):
        super(TaskTable, self).__init__()

    def find(self, id: int):
        sql = f"select * from where problemid={id}"
        return self.exec(sql, "In class TaskTable function find task find error").fetchall()
