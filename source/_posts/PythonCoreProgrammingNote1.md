---
title: Python Core Programming Note 1
categories:
- Python
tags: 
- Python
- Core Programming
- Note
---

## Regular Expression
![常用表达式](/img/1570674939333.png)
![续](/img/1570674953248.png)

## match() & search()

```python
import re
m = re.match('\d','a541')
if m is not None:
    print(m.group())
else:
    print("none found")
	
## none found

import re
m = re.match('\d','a541')
if m is not None:
    print(m.group())
else:
    print("none found")
	
## 5
```
```
import re
m = re.search('..[\d]{1,3}','\na51')
if m is not None:
    print(m.group())
else:
    print("none found")
# . 匹配除\n外的任意字符，其他如\t,\.都可以
```

## 分组

```python
import re
m = re.search('\w+@(\w+\.)*(\w+)*\.com','aaa@aa.a.com')
if m is not None:
    print(m.group())
else:
    print("none found")
```

## sub() & subn()

```python
#使用函数作为参数
def repl_t(txt):
    if txt.group(0) == '-':
        return 'x'
    elif txt.group(0) == '--':
        return '-'
    elif txt.group(0) == '-1':
        return '\"good\"'
m = re.subn('(-{1,2})\d?',repl_t,"d----asf-s-a-123")
print(m)
```

### Regular Expression -> Split()

```python
data = (
 'Mountain View, CA 94040',
 'Sunnyvale, CA',
 'Los Altos, 94023',
 'Cupertino 95014',
 'Palo Alto CA',
 )

for d in data:
     v = re.split(r", |(?= (?:\d{5}|[A-Z]{2})) ",d)
     print(v)
```

### 扩展表达式
// 前瞻：
exp1(?=exp2) 查找exp2前面的exp1
// 后顾：
(?<=exp2)exp1 查找exp2后面的exp1
// 负前瞻：
exp1(?!exp2) 查找后面不是exp2的exp1
// 负后顾：
(?<!exp2)exp1 查找前面不是exp2的exp1

要理解?:则需要理解捕获分组和非捕获分组的概念：

> ()表示捕获分组，()会把每个分组里的匹配的值保存起来，使用$n(n是一个数字，表示第n个捕获组的内容)
> (?:)表示非捕获分组，和捕获分组唯一的区别在于，非捕获分组匹配的值不会保存起来


```python
m = re.findall(r'(?<!YES)yes','YESyes? YESYes . YESyesYES!! ')
print(m)

m = re.sub('\B(?=(?:\d{3})+(?!\d))',',',"123456789")
print(m)
```

?i ignorecase
?m multi-line search
?s dotall, 点号也可表示\n
?x 格式化正则中的空格
?: 分组查询但不保存在结果中

```python
m = re.findall(r'(?m)(^th[\w ]+)', """
This line is the first,
another line,
that line, it's the best
""")

print(m)
```

```python
m = re.search(r'''(?x)
 \((\d{3})\) # 区号
 [ ] # 空白符
 (\d{3}) # 前缀
 - # 横线
 (\d{4}) # 终点数字
 ''', '(800) 555-1212').group()
print(m)
```

```python
m = re.findall(r'http://(?:\w+\.)*(\w+\.com)','http://google.com http://www.google.com http://code.google.com')
print(m)
```

### 贪婪与非贪婪
一个方案是使用“非贪婪”操作符“?”。读者可以在“*”、“+”或者“?”之后使
用该操作符。该操作符将要求正则表达式引擎匹配尽可能少的字符。

```python
data = 'Thu Feb 15 17:46:04 2007::uzifzf@dpyivihw.gov::1171590364-6-8'
patt = '.+?(\d+-\d+-\d+)'
m = re.match(patt, data).group(1)
print(m)
```