---
title: Python Note 5
categories:
- Python
tags: 
- Python
- Note
---
# Python Note 5

## kwargs的使用
* 1. kwargs表示有key, value形式的参数，如：
```python
def test(*args,**kwargs):
    print "args:", args
    print "kwargs", kwargs

test(12,2,abc={"good":7})

# 输出：
# args: (12, 2)
# kwargs {'abc': {'good': 7}}
```

* 2. 使用Pop取出kwargs的值
```python
def test(*args,**kwargs):
    print "args:", args
    print "kwargs", kwargs
    val1 = kwargs.pop('abc', False)
    print "kwargs val:", val1
    if kwargs:
        raise TypeError("Unexpectd ** kwargs, %r" % kwargs)

test(12,2,abc={"good":7}, cde=5)

# 输出：
# args: (12, 2)
# kwargs {'cde': 5, 'abc': {'good': 7}}
# kwargs val: {'good': 7}
# Traceback (most recent call last):
#   File "D:/Avery/Workspaces/pythonProject2/test.py", line 54, in # <module>
#     test(12,2,abc={"good":7}, cde=5)
#   File "D:/Avery/Workspaces/pythonProject2/test.py", line 52, in test
#     raise TypeError("Unexpectd ** kwargs, %r" % kwargs)
# TypeError: Unexpectd ** kwargs, {'cde': 5}
```

