import requests
import json
from ..lib.databaseclass import Problem


def get_user_status(user_name: str):
    url = f"https://codeforces.com/api/user.status?handle={user_name}"
    response = requests.get(url)

    data = json.loads(response.text)
    submissions = data["result"]
    ls = []
    for submission in submissions:
        if submission["verdict"] == "OK":
            ls.append(submission["problem"])
    return ls

def is_user_finished(user_name: str, prob: Problem):
    problems = get_user_status(user_name)
    for problem in problems:
        if str(problem["contestId"]) + problem["index"] == prob.number:
            return True
    return False

if __name__ == "__main__":
    print(is_user_finished("WinterLove", Problem("", "", "", "1801B")))