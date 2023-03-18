import pymysql
from ..lib.config import ConfigClass


class User:
    real_name: str
    qq: str
    student_id: str
    codeforces_id: str

    def __init__(self, real_name: str, qq: str, student_id: str, codeforces_id: str = ""):
        self.real_name = real_name
        if not self.check_qq(qq):
            raise ValueError("qq账号格式不正确")
        self.qq = qq
        if not self.check_student_id(student_id):
            raise ValueError("学号格式不正确")
        self.student_id = student_id
        self.codeforces_id = codeforces_id

    def check_qq(self, qq: str) -> bool:
        for c in qq:
            if not('0' <= c <= '9'):
                return False
        return True

    def check_student_id(self, student_id: str) -> bool:
        if len(student_id) != 10:
            return False
        for c in student_id:
            if not('0' <= c <= '9'):
                return False
        return True

    def to_string(self) -> str:
        return f"real_name={self.real_name}, qq={self.qq}, student_id={self.student_id},codeforces_id={self.codeforces_id}"


class DataBase:
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

    def users_insert(self, user: User): # users插入，无返回值
        sql = f"insert into users(realname, qq, stuid, codeforces) values('{user.real_name}', '{user.qq}', '{user.student_id}', '{user.codeforces_id}')"
        self.exec(sql, "In function users_insert users insert failed")

    def users_delete(self, user: User): # users删除，返回删除行数
        sql = f"delete from users where realname='{user.real_name}' and qq='{user.qq}' and stuid='{user.student_id}'"
        return self.exec(sql, "In function users_delete users delete failed").rowcount

    def users_find_all(self): # users查询，返回所有实例
        sql = f"select * from users"
        return self.exec(sql, "In function users_find_all").fetchall()

    def users_find_stuid(self, student_id: str): # users学号查询，返回所有实例
        sql = f"select * from users where stuid='{student_id}'"
        cursor = self.exec(sql, "In function users_find_stuid users select failed")
        result = cursor.fetchone()
        colums = [col[0] for col in cursor.description]
        if result:
            return dict(zip(columns, result))
        else:
            return None

    def users_find_qq(self, qq: str): # users qq号查询，返回所有实例
        sql = f"select * from users where qq='{qq}'"
        cursor = self.exec(sql, "In function users_find_qq users select failed")
        result = cursor.fetchone()
        columns = [col[0] for col in cursor.description]
        if result:
            return dict(zip(columns, result))
        else:
            return None

    def users_find_realname(self, real_name: str):# users姓名查询，返回所有实例
        sql = f"select * from users where realname='{real_name}'"
        return self.exec(sql, "In function users_find_realname users select failed").fetchall()

    def users_update(self, id: int, user: User):
        sql = f"update users set realname='{user.real_name}', qq='{user.qq}', stuid='{user.student_id}', codeforces='{user.codeforces_id}' \
        where userid={id}"
        return self.exec(sql).rowcount > 0

