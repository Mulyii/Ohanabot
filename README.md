## 数据库(robot)

账号：root

密码：root（暂时）

### 成绩信息

| 列名      | 类型 | 长度 | 约束 | 是否为空 | 备注   |
| --------- | ---- | ---- | ---- | -------- | ------ |
| contestid | int  |      | 外键 | 否       |        |
| userid    | int  |      | 外键 | 否       |        |
| rank      | int  |      |      | 否       | 排名   |
| number    | int  |      |      | 否       | 过题数 |
| penalty   | int  |      |      | 否       | 罚时   |



### 用户信息

| 列名     | 类型    | 长度 | 约束 | 是否为空 | 备注 |
| -------- | ------- | ---- | ---- | -------- | ---- |
| userid   | int     |      | 主键 | 否、自增 |      |
| realname | varchar | 255  |      | 否       | 实名 |
| qq       | varchar | 255  |      | 否       |      |
| stuid    | varchar | 255  |      | 否       | 学号 |



### 比赛信息

| 列名        | 类型     | 长度 | 约束 | 是否为空 | 备注     |
| ----------- | -------- | ---- | ---- | -------- | -------- |
| contestid   | int      |      | 主键 | 否、自增 |          |
| contestname | varchar  | 255  |      | 否       |          |
| time        | datetime |      |      | 否       | 开始时间 |
| duration    | time     |      |      | 否       | 时长     |



### 计划表

可以直接一个标号，对应计划表的编号

| 列名        | 类型    | 长度 | 约束 | 是否为空 | 备注 |
| ----------- | ------- | ---- | ---- | -------- | ---- |
| missionid   | int     |      | 主键 | 否、自增 |      |
| missionname | varchar | 255  |      | 否       |      |
| description | varchar | 255  |      |          | 描述 |



### 题单

联系-计划&题库

| 列名      | 类型 | 长度 | 约束 | 是否为空 | 备注 |
| --------- | ---- | ---- | ---- | -------- | ---- |
| missionid | int  |      | 外键 | 否       |      |
| problemid | int  |      | 外键 | 否       |      |





### 题库表

要求，要存题目地址网址，方便爬虫获取信息

| 列名        | 类型    | 长度 | 约束 | 是否为空 | 备注     |
| ----------- | ------- | ---- | ---- | -------- | -------- |
| problemid   | int     |      | 主键 | 否、自增 |          |
| problemname | varchar | 255  |      | 否       |          |
| url         | varchar | 255  |      | 否       |          |
| submiturl   | varchar | 255  |      | 否       | 提交位置 |



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



## Q群端

**成绩统计公示功能**

从数据库中读取对应的成绩，列成表，转化为图片发送。

**比赛提醒功能**

先用现成插件

**群合作游戏**

用现成插件

**每日一题**

暂时随机一道codeforces上的题。

**chatGPT**



## 私聊端

**成绩统计公式功能**

同上

**入门引导**

两个模块

1. 发送用户现阶段的任务

2. 检查用户是否完成，完成则进入下一阶段

**绑定身份信息**

设置codeforces账号，牛客账号信息。

绑定身份信息，姓名+班级

**chatGPT**

用Github上开源的ChatGPT



## 任务分配

qt端（三个人）：lgx 蔡嘉生 ljr

python端（两个人）：徐建奇 徐晨威



## 代码结构

**所有命名方法采用驼峰命名法**

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
