---
title: Python知识汇总1
categories:
- Python
tags: 
- Python
- Note
---

# 总概

## 1.Old-style, New-style class


```python
Old-style classes

class Person():
    _names_cache = {}
    def __init__(self,name):
        self.name = name
    def __new__(cls,name):
        return cls._names_cache.setdefault(name,object.__new__(cls,name))

ahmed1 = Person("Ahmed")
ahmed2 = Person("Ahmed")
print ahmed1 is ahmed2
print ahmed1
print ahmed2


# >>> False
# <__main__.Person instance at 0xb74acf8c>
# <__main__.Person instance at 0xb74ac6cc>
# >>>

New-style classes

class Person(object):
    _names_cache = {}
    def __init__(self,name):
        self.name = name
    def __new__(cls,name):
        return cls._names_cache.setdefault(name,object.__new__(cls,name))

ahmed1 = Person("Ahmed")
ahmed2 = Person("Ahmed")
print ahmed2 is ahmed1
print ahmed1
print ahmed2

# >>> True
# <__main__.Person object at 0xb74ac66c>
# <__main__.Person object at 0xb74ac66c>
# >>>
```


## 2.字符串拼接的性能对比


```python
import random

L = 400000

s1 = ''.join([chr(random.randint(45, 90)) for i in xrange(L)])
s2 = ''.join([chr(random.randint(45, 90)) for i in xrange(L)])
s3 = ''.join([chr(random.randint(45, 90)) for i in xrange(L)])
s4 = ''.join([chr(random.randint(45, 90)) for i in xrange(L)])
s5 = ''.join([chr(random.randint(45, 90)) for i in xrange(L)])

import timeit
m = 2000
print timeit.Timer('s="".join((s1,s2,s3,s4,s5))', 'from __main__ import s1,s2,s3,s4,s5').timeit(m)  # 性能最佳
print timeit.Timer('s=string.join((s1,s2,s3,s4,s5))', 'from __main__ import s1,s2,s3,s4,s5; import string').timeit(m) # 性能较好
print timeit.Timer('s=s1; s+=s2; s+=s3; s+=s4; s+=s5', 'from __main__ import s1,s2,s3,s4,s5').timeit(m) # 较差
print timeit.Timer('s=s1+s2+s3+s4+s5', 'from __main__ import s1,s2,s3,s4,s5').timeit(m)# 较差
print timeit.Timer('s="%s%s%s%s%s"%(s1,s2,s3,s4,s5)', 'from __main__ import s1,s2,s3,s4,s5').timeit(m)# 较差

```

## 3.对象类型
* 一切都是对象, int,float等基础类型都是对象。但除了关键字！

```python
isinstance(type(A), object)
isinstance(type(type(A)), object)
isinstance(type, object)
isinstance(staticmethod, object)
```

>> import, class, def, pass, return 等不是对象
>> python3.x 以后print是对象，python2.x则不是对象

## 4.迭代器
自定义迭代器实现：
* __init__函数 
* next 函数 

迭代器的使用，如图非标注的函数返回不是迭代器，则会产生一定的性能问题
![迭代器的使用](/img/2021/1.png)

简单实例
![简单实例](/img/2021/2.png)


* 方法一：自定义迭代器
```
class FooIterator(object):
    def __init__(self, foo):
        self._list = foo
        self._cur = 0

    def next(self):
        if self._cur < len(self._list):
            res = self._list[self._cur]
            self._cur += 1
            return res
        else:
            return StopIteration

class Foo(object):
    def __init__(self):
        self._list = [1,2,3,4,5]

    def __iter__(self):
        return FooIterator(self)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, item):
        return self._list[item]

a = Foo()
for a1 in a:
    for b1 in a:
        if a1 is StopIteration:
            break
        if b1 is StopIteration:
            break
        print (a1,b1)
```

* 方法二：使用对象自带的迭代器

```python
class Foo(object):
    def __init__(self):
        self._list = [1,2,3,4,5]

    def __iter__(self):
        return iter(self._list)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, item):
        return self._list[item]
```

* 方法三：yield 形式
运行时调用时会生成generator对象。
![image](/img/2021/3.png)
输出  1，2，3

> 问题：
```python
print foo().next() # 输出 1 地址0xxxabc
print foo().next() # 输出 1 地址0xxxabc
print foo().next() # 输出 1 地址0xxxabc
print foo().next() # 输出 1 地址0xxxabc
```
> foo()在没有引用时会被销毁，在下一行初始化时内存会命中同一块地址空间，虽然地址相同，但实际是一个全新的对象。

* 方法四：Closure闭包
函数内套函数
报错4.1：counter:
![image](/img/2021/1.png)
iter(callable, stop_value)
第一个参数：必须为可调用对象
第二个参数：当迭代器返回值与stop_value相同时将抛出StopIterator

## 5. Name-space vs Object-space

![image](/img/2021/5.png)
![image](/img/2021/6.png)

* C++中输出是不影响的，但python中是会影响到

```python
class CSV(object):
    def __init__(self):
        self._list = [91, 92, 93]

    def push(self, item):
        self._list = item

    def show(self):
        print self._list


if __name__ == '__main__':
    mylist = [1, 2, 3]
    obj = CSV()
    obj.push(mylist)
    obj.show()
    # >> [1, 2, 3]
    
    mylist[1] = 99
    obj.show()
    # >> [1, 99, 3]
```


![image](/img/2021/7.png)

* 搜索顺序：
local -> parent local -> ... -> global -> built-in
全局的namespace: __buildin__

>报错4.1：counter的解释：

>*写的操作将打断往外的搜索顺序
代码 counter += 1 建立了一个空引用的映射，但不是正确的映射，不再往外搜索，但此counter并未赋值。

>*解决方案：使用counter[0]替代counter


## 6. Reflection 反射
C++原生不支持，JAVA,PYTHON,C#都是支持的

python:
* dir: 返回所有可用.访问的所有名字
* __dict__：返回所有的name space空间

实例1：
```python
class A(object):
    def fox(self):
        print "fox"

def dog(self):
    print 'dog'

def cat(self):
    print 'cat'

if __name__ == '__main__':
    a1 = A()
    a2 = A()
    a1.fox()
    a2.fox()

    A.fox = dog
    a1.fox()
    a2.fox()

    A.fox = cat
    a1.fox()
    a2.fox()

```
输出：
fox
fox

dog
dog

cat
cat

实例2：

```python
a1 = A()
a2 = A()
a1.fox()
a2.fox()

import new
a2.fox = new.instancemethod(cat, a2, A)
a2.fox()
a1.fox()
```

输出：
fox
fox
cat
fox

实例3：

```python
print dir(a1)
print dir(a2)
print '-' * 30
print a1.__dict__
print a2.__dict__
```

输出：

```
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'fox']
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'fox']
------------------------------
{}
{'fox': <bound method A.cat of <__main__.A object at 0x000000000330FDC8>>}
```

实例4：

```python
print '-' * 30
print a1.__dict__
print a2.__dict__
A.fox = duck
a1.fox()
a2.fox()
print '-' * 30
print a1.__dict__
print a2.__dict__
```

输出：

```
------------------------------
{}
{'fox': <bound method A.cat of <__main__.A object at 0x00000000037CFE88>>}
duck
cat
------------------------------
{}
{'fox': <bound method A.cat of <__main__.A object at 0x00000000037CFE88>>}
```

解释：a2的由于局部空间还是cat

实例5：

```python
del a2.__dict__["fox"]
a1.fox()
a2.fox()
print '-' * 30
print a1.__dict__
print a2.__dict__
```

结果：
```
duck
duck
------------------------------
{}
{}
```


## 7.对象生命周期
引用计数，计数为0清空
创建时为0， 有引用+1，解引用-1

GC回收机制

## 8.mutable vs immutable
![image](/img/2021/8.png)
不可变对象，比如 str，赋值时将重新生成对象。
实例：

```python
def foo(v, items = [], added= True):
    if added:
        items.append(v)
    print items

foo(1)
foo(2)
foo(3, added=False)
```

输出：
[1]
[1,2]
[1,2]
解释：Python的默认值是保存在函数中的，因为每次调用的默认值时将取同一个表！同时由于[]是可变对象，因此结果是会被存进去的。

> 注：不要将可变对象做为默认参数值

修改：使用None这种非可变对象做为默认参数 
```python
def foo(v, items = None, added= True):
    if added:
        if items is None: 
            items = []
        items.append(v)
    print items

foo(1)
foo(2)
foo(3, added=False)
```

## 9.== 与 is

![image](/img/2021/9.png)
![image](/img/2021/10.png)
![image](/img/2021/11.png)
![image](/img/2021/12.png)
![image](/img/2021/13.png)
![image](/img/2021/14.png)
![image](/img/2021/15.png)

> 注：
> == 值相同
> is 对象引用相同  a is b ---->  id(a) == id(b)
> 小对象池，对于某个范围内的str, int这些类型，将从池子直接拿，返回的是相同的对象
如：int范围，-128 ~ 约200
> None的实例永远只有一个。返回的一个实例。 扩展C时，如果返回为None，需要手动为其加一个引用实例
> Bool只有两个实例，True,False

## 10.import语义
执行期的内容
![image](/img/2021/16.png)

Load the module:
* 1.首先检测是否有，没有则打开m相关的载体，
* 2.创建模块对象，放至到sys.modules
* 3.**在module的namespace中顺序执行所有语句**

> module层级不建议写大消耗代码 
> 不要将import全部写在module头。将导致启动时非常耗时。


![image](/img/2021/17.png)
![image](/img/2021/18.png)
* 使用from import时，会建立一个新的映射。因此不建议使用from import变量，可以使用函数。==**一定要小心使用**==
* 不建议使用 from m import * 导致严重污染到当前命名空间

![image](/img/2021/19.png) 
![image](/img/2021/20.png)
*重复的写操作，import时，也会有写操作，编译期(py->pyc)建立命名空间，多次import就会已经math了

# 总结
![image](/img/2021/21.png)