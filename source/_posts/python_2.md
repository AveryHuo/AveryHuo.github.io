---
title: Python Note 2
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Note
---
# Python Note 2

Python中每一个数据类型实际上都是一个类。

+ ### Function definition
+ As python recommended, left two blank lines after function

```python
def greet_user():
    print("GO")
    print("Hi THERE!")


greet_user()
```

+ ### Function parameters

```python
def greet_user(name):
    print(f"GO:{name}")
    print("Hi THERE!")


greet_user("John")
greet_user() #Error, no parameter

def greet_user2(first_name,second_name):
    print(f"GO:{first_name} {second_name}")
    print("Hi THERE!")


greet_user2("John","Smith")
greet_user2(second_name="John",first_name="Smith") #使用keyword形式作为参数，
greet_user2(second_name="John","Smith") #错误，混合情况必须先用position形式再用keyword形式
```

+ ### Funtion Returns
+ By default, python return none.

```python
def square(number):
	return number * number


result = square(3)
print(result)
```

+ ### Error Handling
+ try except

```python
try:
	day = int(input("input day:"))
	income = 2000 / day
	print(day)
except ZeroDivisionError:
	print("day can't be zero")
except ValueError:
	print("Invalid input")
```

+ ### Comments
+ User comment to explain why and how, not what!

+ ### UML 复习
+ 线->空心菱形：表示聚合关系
+ 实心箭头<-实线：表示父子类关系
+ 实心箭头<-虚线：表示接口实现关系