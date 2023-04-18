############################################
# 调用codeforces提供的API的程序
#
############################################
import requests
import json
from lib.databaseclass import Problem
import datetime
from time import sleep
import random
from lib.databaseclass import UserTable

#上次调用api的时间
last_time = datetime.datetime.now()
# 难度上限与难度下限
# difficulty_min = 1200
# difficulty_max = 1600

def get_user_status(user_name: str): # 获取用户提交列表
    # 设置时间间隔
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
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

def is_user_finished(user_name: str, prob: Problem) -> bool: # 查找用户该题是否通过
    problems = get_user_status(user_name)
    for problem in problems:
        if str(problem["contestId"]) + problem["index"] == prob.index:
            return True
    return False

def get_unsorted_problem_list() -> list:#得到未排序过的题目列表
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    API_BASE_URL = "https://codeforces.com/api/"
    url = API_BASE_URL + "problemset.problems"

    response = requests.get(url)

    response_data = response.json()
    problems = response_data["result"]["problems"]

    return problems

def split_to_pair(s: str) -> list:
    ret: list = s.split(' ')
    [x.strip() for x in ret]
    return list(filter(lambda x: len(x) > 0, ret))

def set_mmin(x):#设置最小难度
    # global difficulty_min
    # difficulty_min = x
    mmin = 0
    mmax = 0
    with open("data/difficulty.txt", encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        list = lines[0]
        number = split_to_pair(str(list))
        mmin = str(x)
        mmax = number[1]
    file_obj.close()
    f = open('data/difficulty.txt', 'w')
    f.write(mmin + " " + mmax)

def set_mmax(x):#设置最大难度
    # global difficulty_max
    # difficulty_max = x
    mmin = 0
    mmax = 0
    with open("data/difficulty.txt", encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        list = lines[0]
        number = split_to_pair(str(list))
        mmin = number[0]
        mmax = str(x)
    file_obj.close()
    f = open('data/difficulty.txt', 'w')
    f.write(mmin + " " + mmax)
def output_mmin():#返回最小难度
    mmin = 0
    mmax = 0
    with open("data/difficulty.txt", encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        list = lines[0]
        number = split_to_pair(str(list))
        mmin = number[0]
        mmax = number[1]
    return int(mmin)

def output_mmax():#返回最大难度
    mmin = 0
    mmax = 0
    with open("data/difficulty.txt", encoding='utf-8') as file_obj:
        lines = file_obj.readlines()
        list = lines[0]
        number = split_to_pair(str(list))
        mmin = number[0]
        mmax = number[1]
    return int(mmax)


def get_problem_list(difficulty_min, difficulty_max):#得到符合条件的题目列表
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    API_BASE_URL = "https://codeforces.com/api/"
    url = API_BASE_URL + "problemset.problems"

    print(difficulty_min, difficulty_max)
    # print(output_mmin())
    # print(output_mmax())
    # 向 API 发送查询请求
    response = requests.get(url)
    # 解析响应数据，获取题目列表
    response_data = response.json()
    # 解析每道题目的难度信息
    problems = response_data["result"]["problems"]
    problem_difficulties = {}
    for problem in problems:
        problem_id = problem["contestId"], problem["index"]
        if "rating" in problem:
            problem_difficulties[problem_id] = problem["rating"]

    # # 筛选符合条件的题目
    filtered_problems = []
    # for problem_id, difficulty in problem_difficulties.items():
    #     if difficulty_min <= difficulty <= difficulty_max:
    #         filtered_problems.append(problem_id)
    tagged_problems = {"dp":[],"math":[],"data structures":[],"graphs":[]}
    for problem in problems:
        problem_id = problem["contestId"], problem["index"]
        if "rating" in problem:
            problem_difficulty = problem["rating"]
            problem_tags = problem["tags"]
            if problem_difficulty >= difficulty_min and problem_difficulty <= difficulty_max:
                tmp = []
                for i in problem_id:
                    tmp.append(i)
                for i in problem_tags:
                    if i == "dp":
                        tagged_problems["dp"].append(tmp)
                    if i == "math":
                        tagged_problems["math"].append(tmp)
                    if i == "graphs":
                        tagged_problems["math"].append(tmp)
                    else:
                        tagged_problems["data structures"].append(tmp)
    for problem in problems:
        problem_id = problem["contestId"], problem["index"]
        if "rating" in problem:
            problem_difficulty = problem["rating"]
            problem_tags = problem["tags"]
            if problem_difficulty >= difficulty_min and problem_difficulty <= difficulty_max:
                # tagged_problems[problem_id] = problem_tags
                tmp = []
                for i in problem_id:
                    tmp.append(i)
                tmp.append(problem_tags)
                filtered_problems.append(tmp)
    print(tagged_problems)
    return filtered_problems, tagged_problems

def get_last_problem_time():#得到上一次更新每日一题的时间
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    with open("selected_problem.json", "r") as f:
        data = json.load(f)
        last_selected_problem_id = data["problem_id"]
        last_selected_time = datetime.strptime(data["selected_time"], "%Y-%m-%d %H:%M:%S")
    return last_selected_time

def choose_random_problem(problems):# 从题目列表中随机选择一道题目，并返回题目的 URL
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    problem = random.choice(problems)

    # 构建题目的 URL
    url = "https://codeforces.com/problemset/problem/{}/{}/".format(problem[0], problem[1])

    return url

def output_random_problem_url():#输出题目url
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    # 读取保存的题目 ID 和上次选择时间
    with open("data/selected_problem.json", "r") as f:
        data = json.load(f)
        last_selected_problem_id = data["problem_id"]
        last_selected_time = datetime.datetime.strptime(data["selected_time"], "%Y-%m-%d %H:%M:%S")

    # 检查上次选择的题目时间是否在今天
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if last_selected_time >= today:
        # 如果上次选择的题目时间在今天，则使用上次选择的题目
        selected_problem_id = last_selected_problem_id
        url = "https://codeforces.com/problemset/problem/{}/{}/".format(selected_problem_id[0], selected_problem_id[1])
        return url
    else:
        filtered_problems, tagged_problems = get_problem_list(output_mmin(), output_mmin())

        problem = random.choice(filtered_problems)

        url = "https://codeforces.com/problemset/problem/{}/{}/".format(problem[0], problem[1])

        # 保存选择的题目 ID 和选择时间
        with open("data/selected_problem.json", "w") as f:
            data = {
                "problem_id": problem,
                "selected_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            json.dump(data, f)

        return url
def update_random_problem_url():#难度更新时更新题目
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()

    # 读取保存的题目 ID 和上次选择时间
    with open("data/selected_problem.json", "r") as f:
        data = json.load(f)
        last_selected_problem_id = data["problem_id"]
        last_selected_time = datetime.datetime.strptime(data["selected_time"], "%Y-%m-%d %H:%M:%S")

    # 检查上次选择的题目时间是否在今天
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if last_selected_time >= today:
        # 如果上次选择的题目时间在今天，则使用上次选择的题目
        selected_problem_id = last_selected_problem_id
        url = "https://codeforces.com/problemset/problem/{}/{}/".format(selected_problem_id[0], selected_problem_id[1])
        return url
    else:
        filtered_problems, tagged_problems = get_problem_list(output_mmin(), output_mmin())

        problem = random.choice(filtered_problems)

        url = "https://codeforces.com/problemset/problem/{}/{}/".format(problem[0], problem[1])

        return url
# 这里没有将姓名与rating相关，后续可以继续调用
def get_user_rating():#得到数据库所有用户的rating以及codeforceid
    global last_time
    now_time = datetime.datetime.now()
    while (now_time - last_time).seconds < 2:
        sleep(1)
        now_time = datetime.datetime.now()
    last_time = datetime.datetime.now()
    try:
        user_ids = []
        table = UserTable()
        list1 = table.find_all()
        for list in list1:
            user_ids.append(list.codeforces_id)
            print(list.codeforces_id)
        user_rating = {}
        for user_id in user_ids:
            response = requests.get(f"https://codeforces.com/api/user.rating?handle={user_id}")
            if response.status_code == 200:
                response_data = response.json()
                rating = response_data["result"][-1]["newRating"] if response_data["result"] else 0
                user_rating[user_id] = rating

        sorted_user_rating = sorted(user_rating.items(), key=lambda x: x[1], reverse=True)

        for user_id, rating in sorted_user_rating:
            print(f"{user_id}: {rating}")
        return sorted_user_rating
    except:
        print("数据库连接出错！")
def get_cf_user_rating(user_id):#已知id得到单个用户的rating
    url = f"https://codeforces.com/api/user.rating?handle={user_id}"
    response = requests.get(url)
    response_data = response.json()
    if response_data["status"] == "OK":
        return response_data["result"]
    else:
        return None

def sort_cf_user_rating(user_ids):#对rating进行排序
    user_ratings = []
    for user_id in user_ids:
        user_rating = get_cf_user_rating(user_id)
        if user_rating is not None and len(user_rating) > 0:
            rating = user_rating[-1]["newRating"]
            user_ratings.append((user_id, rating))
    sorted_user_ratings = sorted(user_ratings, key=lambda x: x[1], reverse=True)
    return sorted_user_ratings

