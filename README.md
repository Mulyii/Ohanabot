组长：郭宇航

组员：徐建奇，蔡嘉生，李嘉瑞，徐晨威

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

直接访问所有数据库。

增删改查，查看所有属性和元素。

不支持对数据库属性的修改，只允许对实体的修改。

要做的尽可能和excel一样操作，比如双击该控件就可以修改内容什么的。

基本完成，但成绩表部分功能实现存在问题，就是说不能存在一场比赛对应多个用户或一个用户对应多场比赛的情况。


## QQ端
**个人信息注册修改**

命令：register

实现：注册个人信息，存入数据库users中。

目的：绑定qq号和个人身份，方便查看个人训练情况。

命令：unregister

实现：注销个人信息，同时在users中删除。

目的：若注册时信息有误或者换了qq号，可以重新注册。

命令：myinfo

实现：查看自己的信息。

命令：set[infoname]

实现：修改个人信息

**codeforces比赛自动提醒**

命令：cf

实现：获取codeforces网站上的比赛信息。

目的：提醒群友接下来的比赛，不要错过。

**自动添加好友**

命令：ACM_Club + 备注信息

实现：自动添加好友。

目的：要使用私聊功能需要添加好友才能实现，所以实现自动通过好友申请，但不能通过任何人的好友申请，所以添加了格式要求。

**codeforces rating校内排名查看**

命令： rating

实现：查找本校同学们的codeforce rating

**每日一题（建立半年的题库）**

命令：每日一题（everyday）

实现：随机从codeforce一个指定难度的问题，并且保存近半年的题目。

**指令菜单**

命令：help + 数字参数

实现：用法、功能展示。

目的：用图片形式展示出各种功能的用法和指令操作，方便使用者使用。

**小游戏，可以活跃气氛，拉近群友距离**

今日人品：

> 命令：jrrp
>
> 实现：随机生成今日的幸运数字

抽象：

> 命令：abstract + 抽象内容 
>
> 实现：抽象一段内容为emoji表情

对联：

> 命令：duilian + 上联内容
>
> 实现：人工智能和你对对联

猜成语：

> 命令：
>
> - handle 开始游戏
>
> - stop停止游戏
>
> 实现：有十次的机会猜一个四字词语，每次猜测后，汉字与拼音的颜色将会标识其与正确答案的区别。

猜单词：

> 命令：
>
> - wordle 开始游戏
> - stop 停止游戏
>
> 实现：猜一个指定长度（默认为5）的英文单词，每次猜测后，单词字母的颜色将会标识其与正确答案的区别。

**OpenAi**

命令：chat

目的：接入chatGPT3.5，和chatGPT进行对话。

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

**多人竞赛**

前提：创建账号

指令集: 

- mpc 创建比赛
- join 加入比赛
- mpc.stop 强制终止比赛

mpc创建比赛， 随机抽取题目，发送生成的题目链接。

用户可以通过join命令加入比赛，在比赛结束后会显示所有加入比赛人员的题目通过情况。





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

与日常交流的文字区分开。

**databaseClass**

```python
# 对数据库操作进行封装
class [name]Table:
    def __init__():
        pass
    def insert():
        pass
    def delete():
        pass
    def find():
        pass
# 各个数据库存储的实例建立对象
class [name]:
    def __init__():
        pass
    def print():
        pass
```

**dependClass**

封装用户请求信息

**codeforcesAPI**

封装codeforcesAPI的调用函数

## 演示截图

### python端

![help](help.png)

![myinfo](myinfo.png)

![sethelp](sethelp.png)

![chat](chat.png)

![rating](rating.png)

![jrrp](jrrp.png)

![duilian](duilian.png)

![abstract](abstract.png)

![mpc](mpc.png)

![mytest](mytest.png)

![testresult](testresult.png)

![wordle](wordle.png)

### 桌面端

![qt1](qt1.png)

![qt2](qt2.png)

![qt3](qt3.png)

![qt4](qt4.png)

![qt5](qt5.png)

![qt6](qt6.png)

![qt7](qt7.png)

![qt8](qt8.png)

![qt9](qt9.png)

![qt10](qt10.png)

![qt11](qt11.png)

![qt12](qt12.png)

