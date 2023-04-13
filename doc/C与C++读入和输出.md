# C与C++的读入和输出



### scanf和printf

```CPP
#include<stdio.h> // c头文件
#include<cstdio> // c++头文件
```

它们包含在以上对应的两个头文件内。

以下以C语言代码为例：

```CPP
#include<stdio.h>

int main(){
    int n;
    scanf("%d", &n);
    printf("%d", n);
}
```

尝试以上代码，运行后，输入一个整数，该程序会将你输入的数字输出。

```CPP
#include<stdio.h>

int main(){
    int a, b;
	scanf("%d%d", &a, &b);
    printf("%d", a + b);
}
```

尝试以上代码，运行后，输入两个整数，该程序会输出两整数的和。



接下来我们来解释一下该语句：

首先scanf第一个传的参数是一个字符型数组，它规定了程序读入字符的规则。

```CPP
scanf("%d", &n); // %d表示一个读入整数，这个读进来的数复制给变量n
scanf("%d%d", &a, &b); // 表示读入两个整数，这两个整数按先后顺序传给变量a和b
scanf("%c", &c); // %c表示读入一个字符类型的数， 存在变量c中
```

**注意：读入数据的类型一定要和后面变量的类型一致，后面变量前面一定要加&，具体原因到后面就会学到**

当然还可以读入其他类型的数

| 表达式 | 类型                                           |
| ------ | ---------------------------------------------- |
| %d     | 整形 int  $[-2^{31},2^{31})$                   |
| %lld   | 长整型 long long  $[-2^{63},2^{63})$           |
| %f     | 浮点型 float                                   |
| %lf    | 双精度浮点型 double                            |
| %u     | 无符号整型 unsigned int  $[0,2^{32})$          |
| %ull   | 无符号长整形 unsigned long long  $[0, 2^{64})$ |
| %c     | 字符型 char                                    |
| %s     | 字符型数组 char[]                              |
| ...    | ...                                            |

上面是比较常用的，还有很多不常用的表达，可以参考书本。

printf也同理上表

**注意：printf中变量不要加&符号**



接下来是进阶一点的用法

在printf中可以添加其他的字符

```CPP
int n = 100;
printf("your score is %d", n); // 输出 your score is 100
```

同样在scanf中也可以添加其余字符

```CPP
int a, b;
scanf("%d;%d", &a, &b); // 输入两个变量，用分号隔开
printf("%d", a + b); // 输出a与b的和
/*
输入：
1;2
输出：
3
*/
```

scanf读入会将空白字符认定为分隔符，比如空格、制表符、换行符等。

```CPP
scanf("%d%d", &a, &b);
/*
输入
1 2
等价输入
1
2
*/
```

当然，scanf读入后，会将空白字符留在缓冲区，所以如果你想读入字符型数组的话，需要额外读入一个空白字符才能接下去读入

```CPP
char s1[10], s2[10]
scanf("%s%s", s1, s2); // 字符型数组前不需要加&
printf("%s\n", s1);
printf("%s\n", s2);
/*
当输入为:
abcde
fghij
输出为：
abcde

*/
```

为什么会只读入第一行和，原因就是s2单独读入了一个换行符

改成

```CPP
scanf("%s\n%s", s1, s2);
```

即可成功。

下面是一些常用的制表符

| 制表符 | 意思   |
| ------ | ------ |
| \n     | 换行符 |
| \t     | Tab    |
| \b     | 退格   |

尝试以下代码

```CPP
printf("%04d %04d", 100, 10); // 0100 0010
printf("% 4d % 4d", 100, 10); //  100   10
printf("%.4f %.2f", 1.1, 1.1); // 1.1000 1.10
printf("%4.1f %4.2f", 1.1, 1.1); //  1.1 1.10
```

%04d表示左边不足4位的补0

% 4d表示左边不足4位的补空格

%.4f表示保留小数点后4为

%4.1f表示保留小数点后一位，不足四位左边补空格



scanf和printf还有更多进阶用法，如果有同学好奇，可以自行搜索。



### cin 和 cout

这是在C++中才有的输入输出

头文件

```CPP
#include<iostream>
```

它包含在一个叫std的命名空间内

```CPP
#include<iostream>
int main(){
	std::cout << "Hello World";
}
// or
#include<iostream>
using namespace std;
int main(){
	cout << "Hello World";
}
```

这种输入输出会自动判别类型，无需告知函数

```CPP
int a; float b; char c;
cin >> a >> b >> c; // 这样写就可以了
cout << "int: " << a << "\n" << "float: " << b << "\n" << "char: " << c << "\n";
```



### 在ACM竞赛中的应用

scanf读入和printf输出的效率要比cin和cout高上不少

但是，当cin和cout关闭同步流之后，读入效率反而高与scanf和printf

```CPP
using namespace std;
int main(){
	ios::sync_with_stdio(false);
    cin.tie(nullptr); cout.tie(nullptr);
    // 以上是关闭同步流的代码
}
```

两种读入输出方式基本涵盖大部分情况，可以自行选择喜欢的函数使用。
