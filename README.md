## 数据库(robot)

账号：root

密码：root（暂时）

### 成绩信息(scores)

| 列名      | 类型 | 长度 | 约束 | 是否为空 | 备注   |
| --------- | ---- | ---- | ---- | -------- | ------ |
| contestid | int  |      | 外键 | 否       |        |
| userid    | int  |      | 外键 | 否       |        |
| rank      | int  |      |      | 否       | 排名   |
| number    | int  |      |      | 否       | 过题数 |
| penalty   | int  |      |      | 否       | 罚时   |

### 用户信息(users)

| 列名         | 类型      | 长度  | 约束  | 是否为空   | 备注     |
|------------|---------|-----|-----|--------|--------|
| userid     | int     |     | 主键  | 否、自增   |        |
| realname   | varchar | 20  |     | 否      | 实名     |
| qq         | varchar | 11  |     | 否      |        |
| stuid      | varchar | 10  |     | 否、不可重  | 学号     |
| codeforces | varchar | 30  |     | 是      | cf账号   |
| missionid  | int     |     |     | 否      | 当前任务进度 |

### 比赛信息(contests)

| 列名       | 类型       | 长度  | 约束  | 是否为空 | 备注   |
|----------|----------|-----|-----|------|------|
| id       | int      |     | 主键  | 否、自增 |      |
| name     | varchar  | 100 |     | 否    |      |
| time     | datetime |     |     | 否    | 开始时间 |
| duration | time     |     |     | 否    | 时长   |
| site     | varchar  | 30  |     | 否    | 比赛地点 |

### 计划表(missions) *弃用*

可以直接一个标号，对应计划表的编号

| 列名            | 类型      | 长度  | 约束  | 是否为空 | 备注      |
|---------------|---------|-----|-----|------|---------|
| missionid     | int     |     | 主键  | 否、自增 |         |
| missionname   | varchar | 30  |     | 否    |         |
| description   | varchar | 255 |     |      | 描述      |
| nextmissionid | int     |     |     |      | 下一个计划标号 |


### 题单(tasks) *弃用*

联系-计划&题库

| 列名        | 类型   | 长度     | 约束  | 是否为空 | 备注 |
|-----------|------|--------|-----|------| ---- |
| id        | int  | 主键、自增  | 否   |      |
| missionid | int  |        | 外键  | 否    |      |
| problemid | int  |        | 外键  | 否    |      |

### 题库表(problems) *弃用*


| 列名     | 类型      | 长度  | 约束  | 是否为空 | 备注   |
|--------|---------|-----|-----|------|------|
| id    | int     |     | 主键  | 否、自增 |      |
| name  | varchar | 20  |     | 否    | 题目名  |
| contest_id | int |   |     | 否    | 比赛id |
| index | varchar | 10  |     | 否    | 题目编号 |
| url    | varchar | 100 |     | 否    | 题目网址 |
|  |  |  | |  |  |

### 消息表(interactions)

| 列名       | 类型       | 长度  | 约束     | 是否为空  | 备注                               |
|----------|----------|-----|--------|-------|----------------------------------|
| id       | int      |     | 主键、自增  | 否     | 编号                               |
| sendtime | datetime |     |        | 否     | 消息发送时间                           |
| sender   | varchar  | 30  |        | 否     | 消息发送人                            |
| receiver | varchar  | 30  |        | 否     | 消息接受者                            |
| typename | varchar  | 20  |        | 否     | 消息类型(group, private, add friend) |
| comefrom | varchar  | 20  |        | 否     | 消息来源(群号，QQ号)                     |
| message  | text     |     |        | 否     | 消息内容                             |
| command  | varchar  | 20  |        | 否     | 触发命令                             |

### 测试结果记录表(tests)

| 列名  | 类型 | 长度 | 约束 | 是否为空 | 备注     |
| ----- | ---- | ---- | ---- | -------- | -------- |
| id    | int  |      | 主键 | 否       | 用户id   |
| math  | int  |      |      | 否       | 数学     |
| other | int  |      |      | 否       | 杂耍     |
| struc | int  |      |      | 否       | 数据结构 |
| dp    | int  |      |      | 否       | 动态规划 |
| geo   | int  |      |      | 否       | 平面几何 |
| grap  | int  |      |      | 否       | 图论     |
| str   | int  |      |      | 否       | 字符串   |





## 教练端

### 要求

桌面应用程序，主要用于管理数据库。

### 环境

编译环境： C++，Qt6+

数据库版本： MySQL8.0+

### 详细

#### 页面一 *弃用*

**导入成绩页面**

要求EXECL文件，拖到指定区域，或者选择路径两种方式添加文件。

提供一个上传按钮，点击按钮后传输到后端进行解析，提取关键列（排名，题数，罚时，等），输入数据库。（注意表格格式可能不统一，但是列名一致）

#### 页面二 *弃用*

**修改数据库页面**

比如数据库导入有问题，需要提供历史版本备份，如果导入出错，可以退回历史版本。（这个可以先不管，基本完成后添加该功能）

修改数据库。

查看表。

#### 页面三 *弃用*

**编辑学生计划表**

**查询学生进度**

#### 页面四

**添加比赛**

比赛名，时间，时长

#### 页面五（可以先不做）*弃用*

**查询学生个平台Rating**

#### 页面六（这个优先）

直接访问所有数据库。

增删改查，查看所有属性和元素。

不支持对数据库属性的修改，只允许对实体的修改。

要做的尽可能和excel一样操作，比如双击该控件就可以修改内容什么的。

基本完成，但成绩表部分功能实现存在问题，就是说不能存在一场比赛对应多个用户或一个用户对应多场比赛的情况。


## QQ端
**个人信息注册修改**

register, myinfo

已完成（xcw）

**最近各大网站和学校公开赛的比赛自动提醒**

**入门训练学习引导** *弃用*

task

已完成（xcw）

**自动添加好友**

已完成（xcw）

**codeforces rating校内排名查看**

**比赛成绩排名统计和查询** *弃用*

**名单、成绩公示** *弃用*

**每日一题（建立半年的题库）**

~~**指令菜单**~~

**问题集合（对一些经常问的问题进行总结）**

**小游戏，可以活跃气氛，拉近群友距离**

~~**OpenAi**~~

**自我测评**

前提：创建账号

指令集：#myteststart, #mytestfinish, #mytestresult, #alltestresult

题目数量：n未定，测试用两题

题目分类：数据结构，图论，数学，动态规划，平面几何，字符串，杂耍

评测方式：

> 随机选择n道题目，难度范围视具体情况而定，建议（800-1900）。
>
> 当前题目通过后， 可以通过#mytestnext继续测评（考虑到不一定有人有很长的连续时间测评，所以允许分段测评）。
>
> 时间限制：1h

评分方式：

> 获取题目的分类，将分类归类为上面给出的七个大类，更具每一分类分别计算。
>
> 就像打天梯赛一样，一层一层往上爬，rating取最大值
>
> 暂时只能这样了，想不到更好的方法了QAQ

**自建比赛**

前提：创建账号

指令集: #createcontest, #addcontest, #contestresualt, #deletecontest, #mycontest， #mycontestsubmit

createcontest:

创建比赛，每人同时只能创建一场比赛。

附加命令[date] [time] [duration] [rating range]

例 $\#createcontest\ 2023.04.16\ 14:00\ 2:00\ [800,1900]$

若创建成功，回复比赛id

若输入不合法，则返回创建失败

addcontest:

后面跟一个比赛ID

不能重复添加，没有人数上限

不存在返回不存在

contestresualt：

后面跟比赛ID

返回比赛结果排名图片

deletecontest：

删除比赛，仅比赛创建者可以删除。

mycontest：

查询自己报名的比赛信息。

返回图片。



比赛开始时， 随机抽取题目，生成图片私聊发送参赛用户。

用户通过mycontestsubmit [题目编号] [代码] 提交代码。

返回题目通过情况，按照区域赛标准，只提供错误信息，不提供错误点。

时间到，结束比赛，计算分数排名，存入数据库。





## 任务分配

qt端（三两个人）：lgx 蔡嘉生

python端（三个人）：徐建奇 徐晨威 ljr



## 代码结构

**Python所有命名方式用小写+下划线分割的方式，Class采用驼峰命名法**

**Qt所有命名方法采用驼峰命名法**

**数据库所有命名包括指令采用全小写表达**

**写注释，写注释，写注释**

**如需更多类可以自行添加，同时更新文档**

**窗口允许放大缩小**

### QT

采用.hpp的写法，除主函数外不得有全局函数，不得有全局变量。

#### DataBaseConnection类

``` CPP
typedef string DataBaseConnectionErrorInfo;
```

``` CPP
private:
// 数据库指针
// SqlQuery指针
public:
DataBaseConnection(); // 构造函数中连接Mysql数据库，连接失败throw错误(DataBaseConnectionErrorInfo)
void sqlCommand(string sql); // 执行sql指令
~DataBaseConnection(); // 释放所有指针
```

#### (Table)Connection类(这里的Table是变量，对于不同表建一个类)

```CPP
class TableConnection : public DataBaseConnection{
private:
public:
    TableConnection(); // table名
    ~TableConnection();
    void tableCommand(string sql); // 仅对该table操作，调用sqlCommand
}
```

#### (Table)Operation类

``` CPP
class TableOperation : public TableConnection{
private:
public:
    TableOperation(string table); // 构造函数
    ~TableOperation();
    void insert(); // 插入
    void update(); // 更新
    void delete(); // 删除
}
```

#### (Table)Class类(对于每个表建实体类)

``` CPP
class TableClass{
private:
    // 所有属性对应变量
public:
    // 默认构造函数，普通构造函数， 拷贝构造函数（深拷贝），析构函数
    // set 和 get 函数
    // 重载 = 号， 深拷贝
}
```

（在此处添加）



### python端

所有与机器人交互指令前面都加上“#”（例"#jrrp"）
