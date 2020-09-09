---
title: GEA-P3
categories:
- IT阅读
tags: 
- Game
---

## (3.1) C++ Review and Best Practive

imperative languages: C
object-oriented languages: C# , Java
scripting languages: python lua,perl
functional languages: Lisp, scheme, F# 

### Multiple Inheritance(MI)
Most C++ software developers avoid multiple inheritance completely or
only permit it in a limited form. 
> 多继承容易让结构混乱，提升技术难度，引发deadly diamond问题（当父类们存在相同函数时，子类不知道实现哪个？）
> 实际应用中，多继承应继承自无父的类对象
> Most C++ software developers avoid multiple inheritance completely or
only permit it in a limited form. A common rule of thumb is to allow only
simple, parentless classes to be multiply inherited into an otherwise strictly
single-inheritance hierarchy. Such classes are sometimes called mix-in classes
because they can be used to introduce new functionality at arbitrary points in
a class tree. 

![Deadly diamond](./img/1575255814499.png)
![Mix-in class](/img/1575255482902.png)

### Composition and Aggregation

组合和聚合
has-a, uses-a

### Coding Standards

代码规范
> 1.Some standards make the code more readable, understandable and maintainable.
>2. Other conventions help to prevent programmers from shooting themselves in the foot. For example, a coding standard might encourage the
programmer to use only a smaller, more testable and less error-prone
subset of the whole language. The C++ language is rife with possibilities for abuse, so this kind of coding standard is particularly important
when using C++.

> Interfaces are king. 接口保持干净，整洁
> Good names encourage understanding and avoid confusion.  命名要求规范
> Don’t clutter the global namespace. C++中避免互包等混乱
> Follow C++ best practices. Books like the Effective C++ series by Scott Meyers [31,32], Meyers’ Effective STL [33] and Large-Scale C++ Software Design3.1. C++ Review and Best Practices 105
by John Lakos [27] provide excellent guidelines that will help keep you
out of trouble.   关注最好的代码
> Be consistent.  坚定规范要求
> Make errors stick out. 让错误更易在代码中查觉。

