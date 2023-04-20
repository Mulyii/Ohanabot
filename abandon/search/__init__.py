from nonebot import on_command
from lib.dependclass import DependClass
from nonebot.params import Depends
from lib.databaseclass import UserTable
from lib.dependclass import response
from lib.to_picture import table_to_pic
from nonebot.adapters.onebot.v11.message import MessageSegment

my_task_rank = on_command("mytaskrank")
all_task_rank = on_command("alltaskrank")


@my_task_rank.handle()
async def my_task_rank_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    user_table = UserTable()
    lines = user_table.find_all()
    my = user_table.find_qq(qq_account.uid)
    if my is None:
        await response(my_task_rank, "该账号未注册，请先用#register help查看注册方法", qq_account)
        return
    rank = 0
    for line in lines:
        if line.mission_id > my["missionid"]:
            rank += 1

    await response(my_task_rank, f"你的任务进度排名为第{rank + 1}名", qq_account)


@all_task_rank.handle()
async def all_task_rank_receiver(qq_account: DependClass = Depends(DependClass, use_cache=False)):
    user_table = UserTable()
    lines = user_table.find_all()
    lines.sort(key=lambda x: x.mission_id, reverse=True)
    title = "任务进度完成排名"
    headers = ["排名","姓名", "完成任务数"]
    table = []
    rank = 0
    for i in range(0, len(lines)):
        if i == 0 or (i > 0 and lines[i].mission_id < lines[i - 1].mission_id):
            rank += 1
        table.append([rank, lines[i].real_name, lines[i].mission_id])
    image = await table_to_pic(title=title, headers=headers, table=table)
    print(type(image))
    print(image)
    await response(all_task_rank, image, qq_account)
