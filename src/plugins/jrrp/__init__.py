import random
from datetime import date
from nonebot import on_command
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event

def luck_simple(num) :
    if num == 0 :
        return "喆喆喆"
    elif num <= 18 :
        return "大吉"
    elif num <= 30 :
        return "吉"
    elif num <= 40 :
        return "中吉"
    elif num <= 50 :
        return "小吉"
    elif num <= 60 :
        return "末吉"
    elif num <= 83 :
        return "凶"
    elif num <= 99 :
        return "大凶"
    else :
        return "终凶"

Map = {}
def re_load() :
    now_day = True
    with open("src/plugins/jrrp/data/id_lucknum.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            line.strip("\n")
            if line.startswith("date:") :
                if line[5:-1] != date.today().strftime("%y%m%d"):
                    Map.clear()
                    now_day = False
                    break
            else :
                id_num = line.split(" ")
                Map[id_num[0]] = eval(id_num[1])
    if now_day == False:
        with open("src/plugins/jrrp/data/id_lucknum.txt", "w", encoding="utf-8") as f :
            f.write("date:" + date.today().strftime("%y%m%d") + "\n")

re_load()

jrrp = on_command (
    "今日人品",
    aliases={"jrrp"},
    priority=1,
    block=True,
    )

@jrrp.handle()
async def jrrp_handle(bot: Bot, event : Event):
    lucknum = -1
    id = event.get_user_id()
    if id in Map :
        lucknum = Map[id]
    else :
        rnd = random.Random()
        # 固定随机种子，每天刷新
        # rnd.seed(int(date.today().strftime("%y%m%d")) + int(id))
        lucknum = rnd.randint(0, 100)
        Map[id] = lucknum
        with open("src/plugins/jrrp/data/id_lucknum.txt", "a", encoding="utf-8") as f :
            f.write("{} {}\n".format(id, lucknum))
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]您今日的幸运指数是{lucknum}/100（越低越好），为"{luck_simple(lucknum)}"'))


from nonebot_plugin_apscheduler import scheduler
job = scheduler.add_job(re_load, "cron", hour = 0, minute = 0)
    