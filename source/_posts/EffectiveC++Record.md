---
title: Effective C++学习记录
categories:
- CPlusPlus
tags: 
- C++
---

#### 条款1: 习惯C++
C++ 领域的四大块：
* 1.C： 基础，语句，数组，指针等等
* 2.Object-Oriented C: 继承，多态，封装
* 3.Template C++: 泛型编程
* 4. STL： 一种特殊的Template程序库，容器，迭代器，算法，对象等等规约

#### 条款2：尽量以const, enum, inline替换 #define
宁用编译器替换预处理器。
* 1.使用声明式与定义式：如
```c++
//头文件
class GamePlayer{
private:
	static const int NumTurns = 5;//声明时候指定数值
}
//实现文件
const int GamePlayer::NumTurns;//无需再次定义了
```
* 2.使用enum当int数组用
```c++
class GamePlayer{
private:
	enum{NumTurns =5};
	int scores[NumTurns];
}
```
* 3.对于函数宏定义，使用Inline替代
 ```c++
 //替换以下define语句。
 //#define CALL_WITH_MAX(a,b) f(a>b?a:b);
 template<typename T>
 inline void callWithMax(const T&a,const T&b)
 {
 	f(a>b?a:b);
 }
 ```

