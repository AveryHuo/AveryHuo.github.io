---
title: Python Note 1
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Note
---
# Python Note 1

+ 逻辑运算符的使用：
+ and or not 会将几个值作为False ：0 None "" []

+ 多变量赋值
```python
minValue, maxValue = 10 , 20
```

+ 命名规范
+ 变量名，函数名： 小驼峰或下划线小写的形式
+ 常量：全大写
+ 类名：大驼峰

+ 代码换行：
+ 当一行写不完时，使用 \ 将代码延续
```python
product  = max(100,200) \
					*30
```

+ 输出：
+ 以% 输出
+ 字符宽度指定："%3d" 右对齐数字， “%-3d”左对齐数字。换成s则为字符串。 
+ 小数精度指定：%<field_width>.<precision>f  ，注意字符宽度将包含.
```python
a = 10
print("%d"%a)
b = 100.025
print("%0.2f"%b)
print("%-10.3f"%b)
```

+ 自动转义的函数
+ "greater".__len__() 等价于len("greater")
+ "a"+"b" 等价于"a".__add__("b")
+ "e" in "great" 等价于 "great".__contains__("e")


+ ==获取对象可用函数列表==
+ dir(str) 

+ ==获取函数文档==
+ help(str.upper)

+ 以独立程序加载的python文件
+ 使用“main”标记为模块name的名字
```python
if __name__ == "__main__"
	main()
```

+ ### while结构
 注： """  多行string

```python
n = 0
while n < 5:
	print("""
This is test!
This is test2!
This is test3!
	""")
	n = n + 1
```

+ ### For结构
 * 普通使用
 
 ```python
 for i in range(5):
 	print()
 ```
 * Use curly braces, 显示变量

```python
 for i in range(5):
 	print(f"i:{i}")
 ```
 * 使用重复*个数输出字符

```python
 for i in range(5):
 	print(f"i:{i}"*4)
 ```

+ ### List
+ 注意List的切片和连接运算符返回的就是一个新的数组
* 普遍用法

```python
names = ['John', 'Bob', 'Mosh', 'Sarah', 'Mary']
print(names[2:])  #Print will start from 'Mosh'''
print(names[:])  #Print all'
names[0] = 'Joh' #Change item
print(names)  #output
# 2d list
matrix = [
   [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
matrix[0][-3] = 20
print(matrix)
```

* 编辑类

```python
numbers = [5,2,1,7]
numbers.insert(-2,20)
numbers.remove(2)
numbers.append(45)
numbers.pop() #remove the last and return it
print(numbers.index(5))
numbers.sort()
numbers.reverse() #get deasc order
if 5 in numbers:
    print(numbers.index(5))
numbers2 = numbers.copy()
numbers.append(45)
print(numbers)
print(numbers2)

#去重复
numbers = [5,20,1,5,7,5,6,4,5]
uniques = []
for i in numbers:
    if i not in uniques:
        uniques.append(i)
print(uniques)
```

+ ### Tuple
+ 类似于List，但不可修改

```python
numbers = (5,20,1,5,7,5,6,4,5)
numbers[0] = 1 #TypeError: 'tuple' object does not support item assignment
```

+ ### Unpacking
+ 映射数组成员

```python
coordinates = (1,2,3)
a = coordinates[0]
b = coordinates[1]
c = coordinates[2]

# use Unpacking feature, unpacking the tuple/list to three variable
x, y, z = coordinates
print(f"{a},{b},{c} <=> {x}, {y}, {z}")
```

+ ### Dictionary

```python
customer = {
    "name": "John",
    "age": 30,
    "is_verified": True
}
print(customer["name"])
# print(customer["Name"]) #KeyError,don't contain
# print(customer["birthdate"])#KeyError,don't contain
print(customer.get("name"))
print(customer.get("Name","Hey")) #Print,with default value:'Hey'
customer["name"] = "AA"
print(customer.get("name"))

#Exercise
input_str = str(input("Phone:"))
digits_map = {
    "1":"One",
    "2":"Two",
    "3":"Three",
    "4":"Four",
}
output = ''
for s in input_str:
    output += digits_map.get(s,"") + " "

print(output)
```
+ [mac]ctrl+cmd+space>> to show emojis

+ ### 函数
+ 注释：
+ 三个引号的注释，意为文档注释，使用help函数时显示
+ 无返回函数，默认返回为None

+ 递归函数：
+ 输出的小技巧：使用“ ” * 递归序号的形式生成缩进的日志，这样就有一个层级的输出结构了。

+ 函数之中也可嵌套函数！

+ 高阶函数：filter函数与map函数，reduce函数
+ map将第二个列表中的值放到第一个参数的函数中逐个执行。最后把结果映射成map出来
+ filter将把第二个列表中的值逐个放到第一个参数的函数中进行运算得出 True的放到一个结果里。
+ reduce函数是每一个参数是一个带双参的函数，第一个参为下一项，第二参为上一次的结果。
```python
def is_no_zero(v):
    if v != 0:
        return True
    return False

oldlist = [5,0,3,5,0,8,6,4,0,3,9,1]

newlist = list(filter(is_no_zero, oldlist))
newlist = list(map(str, oldlist))
print(newlist)

import  functools
oldlist = [5,0,3,5,0,8,6,4,0,3,9,1]
result = functools.reduce(lambda x,y:x+y, oldlist)
print(result)
```

+ lambda做内联函数
```python
# lambda x,y:x+y
```


+ 使用pickle 读写对象
+ 文件读写类型如：
模式	描述
t	文本模式 (默认)。
x	写模式，新建一个文件，如果该文件已存在则会报错。
b	二进制模式。
\+	打开一个文件进行更新(可读可写)。
U	通用换行模式（不推荐）。
r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
r+	打开一个文件用于读写。文件指针将会放在文件的开头。
rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。
w	打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
w+	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。

```python

mylist = [5, 6, "abc", 7]
f = open("myfile.txt", "w")

for n in mylist:
    print("写入数据：", n)
    pickle.dump(n, f)
    # f.write(n)
f.close()

mylist = list()
f = open("myfile.txt", "r")
while True:
    try:
        item = pickle.load(f)
        # item = f.read()
        mylist.append(item)
    except EOFError:
        f.close()
        break
print("读出的结果：", mylist)

```

+ 常用三种运算符说明
+ //运算符执行地板除法(向下取整除),它会返回整除结果的整数部分
```print(7//2)```
>#3
>这里整除后会返回3.5

+ 同样的，执行取幂运算，ab会返回a的b次方
```print(2**10)```

>#1024
+ 最后，%执行取模运算，返回除法的余数
```python
print(13%7)#6
print(3.5%1.5)#0.5
```

+ ### 使用Profiler探测
+ 安装Profiler库
+ 度量算法性能。