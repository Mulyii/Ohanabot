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

| 列名         | 类型      | 长度  | 约束  | 是否为空  | 备注     |
|------------|---------|-----|-----|-------|--------|
| userid     | int     |     | 主键  | 否、自增  |        |
| realname   | varchar | 20  |     | 否     | 实名     |
| qq         | varchar | 11  |     | 否     |        |
| stuid      | varchar | 10  |     | 否、不可重 | 学号     |
 | codeforces | varchar | 30  |     | 是     | cf账号   |
| missionid  | int     |     |     | 否     | 当前任务进度 |

### 比赛信息(contests)

| 列名        | 类型     | 长度 | 约束 | 是否为空 | 备注     |
| ----------- | -------- | ---- | ---- | -------- | -------- |
| contestid   | int      |      | 主键 | 否、自增 |          |
| contestname | varchar  | 255  |      | 否       |          |
| time        | datetime |      |      | 否       | 开始时间 |
| duration    | time     |      |      | 否       | 时长     |



### 计划表(missions)

可以直接一个标号，对应计划表的编号

| 列名            | 类型      | 长度  | 约束  | 是否为空 | 备注      |
|---------------|---------|-----|-----|------|---------|
| missionid     | int     |     | 主键  | 否、自增 |         |
| missionname   | varchar | 30  |     | 否    |         |
| description   | varchar | 255 |     |      | 描述      |
| nextmissionid | int     |     |     |      | 下一个计划标号 |


### 题单(tasks)

联系-计划&题库

| 列名        | 类型   | 长度     | 约束  | 是否为空 | 备注 |
|-----------|------|--------|-----|------| ---- |
| id        | int  | 主键、自增  | 否   |      |
| missionid | int  |        | 外键  | 否    |      |
| problemid | int  |        | 外键  | 否    |      |





### 题库表(problems)


| 列名     | 类型      | 长度  | 约束  | 是否为空 | 备注   |
|--------|---------|-----|-----|------|------|
| id    | int     |     | 主键  | 否、自增 |      |
| name  | varchar | 20  |     | 否    | 题目名  |
| website | varchar | 20  |     | 否    | 网站名称 |
| index | varchar | 10  |     | 否    | 题目编号 |
| url    | varchar | 100 |     | 否    | 题目网址 |

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

## 教练端

### 要求

桌面应用程序，主要用于管理数据库。

### 环境

编译环境： C++，Qt6+

数据库版本： MySQL8.0+

### 详细

#### 页面一

**导入成绩页面**

要求EXECL文件，拖到指定区域，或者选择路径两种方式添加文件。

提供一个上传按钮，点击按钮后传输到后端进行解析，提取关键列（排名，题数，罚时，等），输入数据库。（注意表格格式可能不统一，但是列名一致）

#### 页面二

**修改数据库页面**

比如数据库导入有问题，需要提供历史版本备份，如果导入出错，可以退回历史版本。（这个可以先不管，基本完成后添加该功能）

修改数据库。

查看表。

#### 页面三

**编辑学生计划表**

**查询学生进度**

#### 页面四

**添加比赛**

比赛名，时间，时长

#### 页面五（可以先不做）

**查询学生个平台Rating**

#### 页面六（这个优先）

直接访问所有数据库。

增删改查，查看所有属性和元素。

不支持对数据库属性的修改，只允许对实体的修改。

要做的尽可能和excel一样操作，比如双击该控件就可以修改内容什么的。



## QQ端
**个人信息注册修改**

register, myinfo

已完成（xcw）

**最近各大网站和学校公开赛的比赛自动提醒**

**入门训练学习引导**

task

已完成（xcw）

**自动添加好友**

已完成（xcw）

**codeforces rating校内排名查看**

**比赛成绩排名统计和查询**

**名单、成绩公式**

**每日一题（建立半年的题库）**

~~**指令菜单**~~

**问题集合（对一些经常问的问题进行总结）**

**小游戏，可以活跃气氛，拉近群友距离**

~~**OpenAi**~~




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
