# C与C++分支和循环语句

**分支语句**

```CPP
if(条件一){
    语句一
}
else if(条件二){
    语句二
}
else if(条件三){
    语句三
}
...
else{
    语句n
}
```

如果条件一的值是`true`，那么就执行语句一

否则，判断条件二，如果是`true`，那么就执行语句二

否则，判断条件三，如果是`true`，那么就执行语句三

....

如果以上条件都不成立，就执行语句n

下面是一个判断分数等级的if语句

```CPP
#include<stdio.h>
int main(){
  	int score;
    scanf("%d", &score);
    if(score >= 90){
        printf("A");
    }
    else if(score >= 80){
        printf("B");
    }
    else if(score >= 70){
        printf("C");
    }
    else if(score >= 60){
        printf("D");
    }
    else{
        printf("F");
    }
}
```



另一种分支语句为`switch` `case`语句，在ACM竞赛中不常用，有兴趣可以翻阅书籍。



**循环语句**

1. for

```CPP
for(语句一;语句二;语句三){
    循环执行语句
}
// 语句一： 循环开始前执行
// 语句二： 单次循环开始前执行，bool表达式，为true继续，为false退出循环
// 语句三： 单次循环结束后执行
```

例: `1`加到`100`的和

```CPP
// C语言写法
int i, sum = 0;
for(i = 1; i <= 100; i++){ // i++是自增表达式，等价于i = i + 1
    sum += i; // 等价与 sum = sum + i
}
printf("%d\n", sum);
// C++语言写法
int sum = 0;
for(int i = 1; i <= 100; i++){
    sum += i;
}
std::cout << sum << "\n";
```

2. while

```CPP
while(条件){
    执行语句
}
// 当条件表达式满足时执行语句
```

例：`1`加到`100`的和

```CPP
int i = 1, sum = 0;
while(i <= 100){
    sum += i;
    i++;
}
printf("%d\n", sum);
```

