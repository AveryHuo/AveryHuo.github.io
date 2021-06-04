---
title: Python源码剖析-Note1
categories:
- Python
tags: 
- Python
- Note
---

## 1.Python 架构

* 1.1 文件组：

  模块、库、自定义模块

* 1.2 核心
    
  解析器

  Scanner词法分析 -> Parser语法分析，建立AST（抽象语法树）
  -> Compiler 生成指令集合，Python字节码（byte code） -> 由Code Evaluator（虚拟机）执行字节码
   
* 1.3 运行时环境
  
    对象/类型系统 Object/Type structures
    内存分配器  Memory Allocator
    运行时状态信息  Current State of Python

## 2.Python的内建对象

* 2.1 关于对象
* 类型对象（整数类型，字符串类型）都是被静态初始化的
* 对象被创建后的内存中的大小是不可变的！

* 2.2 PyObject
* 只包含一个引用计数和一个类型指针（指向具体的结构信息）
```c
/* PyObject_HEAD defines the initial segment of every PyObject. */
#define PyObject_HEAD                   \
    _PyObject_HEAD_EXTRA                \
    Py_ssize_t ob_refcnt;               \
    struct _typeobject *ob_type;

/* Nothing is actually declared to be a PyObject, but every pointer to
 * a Python object can be cast to a PyObject*.  This is inheritance built
 * by hand.  Similarly every pointer to a variable-size Python object can,
 * in addition, be cast to PyVarObject*.
 */
typedef struct _object {
    PyObject_HEAD
} PyObject;
```

* 2.3 PyVarObject
* 对PyObject的扩展，可以理解为一个容器，比如对于一个string的实现，需要使用一个n * char的实现方式，因此需要一个字段存储长度。因此结构如下：

```c
/* PyObject_VAR_HEAD defines the initial segment of all variable-size
 * container objects.  These end with a declaration of an array with 1
 * element, but enough space is malloc'ed so that the array actually
 * has room for ob_size elements.  Note that ob_size is an element count,
 * not necessarily a byte count.
 */
#define PyObject_VAR_HEAD               \
    PyObject_HEAD                       \
    Py_ssize_t ob_size; /* Number of items in variable part */
#define Py_INVALID_SIZE (Py_ssize_t)-1

typedef struct {
    PyObject_VAR_HEAD
} PyVarObject;
```

* 2.4 创建类型对象的方式
* 使用范型的API（AOL）
```c
PyObject *intObj = PyObject_New(PyObject, &PyInt_Type);
```
* 使用与类型相关的API（COL）
```c
PyObject* intObj = PyInt_FromLong(20);
```

* 2.5 对象的行为
* PyTypeObject包含大量函数指针，指明了其不同的对象的行为实现。
* 标准行为函数族：基础类型的函数，列表的函数族，字典用的函数族
```c
    PyNumberMethods *tp_as_number;  
    PySequenceMethods *tp_as_sequence;
    PyMappingMethods *tp_as_mapping;
```

2.6 类型的类型
* 对于用户自定义class所对应的PyTypeObject对象通过PyType_Type创建。
```python
class A(object):
    pass

A.__class__ # 输出 <type 'type'>
int.__class__  # 输出 <type 'type'>
```
python中被称为metaclass

> int运行时类型关系： 
> int - ob_refent + ob_type
>    ob_type - PyInt_Type(ob_type)
>       PyInt_Type(ob_type) -> PyType_Type
>       PyInt_Type(tp_base) -> PyBaseObject_Type

2.7 多态的实现原理
所有的对象使用PyObject来存储，然后再对不同的对象类型执行不同的函数族，实现多态，如
```c
// PyTypeObject PyInt_Type = {
//     PyVarObject_HEAD_INIT(&PyType_Type, 0)
//     "int",
//     sizeof(PyIntObject),
//     0,
//     (destructor)int_dealloc,                    /* tp_dealloc */
//     (printfunc)int_print,                       /* tp_print */
//      ....

PyObject* intObj = PyInt_FromLong(20);
intObj->ob_type->tp_print(intObj, fp, 0);

```
2.8 引用计数
* 增加和减少一个对象的引用计数
```c
ob_refcnt <- Py_INCREF(op), Py_DECREF(op)
```

* 类型对象是超越引用计数规则的，即永远不会析构，每个对象指向类型对象的指针不会被视为对类型对象的引用。
> 注意：当引数为0时，会调用其对应的析构函数，但这并不意味着一定会调用free，因为这样频繁的调用会导致性能不好，所以会采取将其放到内存池的作法。

2.9 对象分类：
* Fundamental对象：类型对象         type
* Numeric对象：数值对象         boolean, float, int
* Sequence对象：序列集合对象     list, tuple, string
* Mapping对象：对应C++中的map     dict
* Internal对象：虚拟机运行时的内部使用对象       function, code, frame, module, method

## 3.Python中的整数对象

3.1 实现方式
* PyIntObject用于实现整数对象，不可变对象，即创建后就不能改变其值
> 引出问题？  非常频繁的创建和销毁Int对象将会导致性能问题

* 元信息：
```c
PyTypeObject PyInt_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "int",
    sizeof(PyIntObject),
    0,
    (destructor)int_dealloc,                    /* tp_dealloc */
    (printfunc)int_print,                       /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    (cmpfunc)int_compare,                       /* tp_compare */
    (reprfunc)int_to_decimal_string,            /* tp_repr */
    &int_as_number,                             /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    (hashfunc)int_hash,                         /* tp_hash */
    0,                                          /* tp_call */
    (reprfunc)int_to_decimal_string,            /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_CHECKTYPES |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_INT_SUBCLASS,          /* tp_flags */
    int_doc,                                    /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    int_methods,                                /* tp_methods */
    0,                                          /* tp_members */
    int_getset,                                 /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    int_new,                                    /* tp_new */
};
```

* PyNumberMethods展示所有可选的操作信息


3.2 int_add的实现

* PyInt_AS_LONG  vs PyInt_AsLong ,后者版本执行效率较慢，会有多方的检查

> python中对于频繁执行的代码，都会提供函数和宏两个版本

* 默认情况下，返回一个新的PyIntObject， 当越界时将转为PyLong_Type的结果返回
```c
static PyObject *
int_add(PyIntObject *v, PyIntObject *w)
{
    register long a, b, x;
    CONVERT_TO_LONG(v, a);
    CONVERT_TO_LONG(w, b);
    /* casts in the line below avoid undefined behaviour on overflow */
    x = (long)((unsigned long)a + b);
    if ((x^a) >= 0 || (x^b) >= 0)
        return PyInt_FromLong(x);
    return PyLong_Type.tp_as_number->nb_add((PyObject *)v, (PyObject *)w);

```
3.3 PyIntObject的创建

* PyInt_FromString 与 PyInt_FromUnicode 最终都是调用PyInt_FromLong创建，适配器模式的设计模式
```c
PyAPI_FUNC(PyObject *) PyInt_FromString(char*, char**, int);
#ifdef Py_USING_UNICODE
PyAPI_FUNC(PyObject *) PyInt_FromUnicode(Py_UNICODE*, Py_ssize_t, int);
#endif
PyAPI_FUNC(PyObject *) PyInt_FromLong(long);
PyAPI_FUNC(PyObject *) PyInt_FromSize_t(size_t);
PyAPI_FUNC(PyObject *) PyInt_FromSsize_t(Py_ssize_t);
```

3.4 大整数与小整数
* 小整数： 默认是[-5，257]的范围，这些整数直接缓存在内存中，并存放其指针在small_ints的中。
```c
// intobject.c
#ifndef NSMALLPOSINTS
#define NSMALLPOSINTS           257
#endif
#ifndef NSMALLNEGINTS
#define NSMALLNEGINTS           5
#endif
```

* 大整数：提供一块内存空间，配置如下：
```c
#define BLOCK_SIZE      1000    /* 1K less typical malloc overhead */
#define BHEAD_SIZE      8       /* Enough for a 64-bit pointer */
#define N_INTOBJECTS    ((BLOCK_SIZE - BHEAD_SIZE) / sizeof(PyIntObject))

struct _intblock {
    struct _intblock *next;
    PyIntObject objects[N_INTOBJECTS];
};
```

计算得出N_INTOBJECTS的值为24，对于一个64位指针使用8个字节来算

3.5 添加与删除

```c
PyObject *
PyInt_FromLong(long ival)
{
    register PyIntObject *v;
#if NSMALLNEGINTS + NSMALLPOSINTS > 0
    // 使用小整数池
    if (-NSMALLNEGINTS <= ival && ival < NSMALLPOSINTS) {
        v = small_ints[ival + NSMALLNEGINTS];
        Py_INCREF(v);
#ifdef COUNT_ALLOCS
        if (ival >= 0)
            quick_int_allocs++;
        else
            quick_neg_int_allocs++;
#endif
        return (PyObject *) v;
    }
#endif
    // 使用通用对象池
    if (free_list == NULL) {
        if ((free_list = fill_free_list()) == NULL)
            return NULL;
    }
    /* Inline PyObject_New */
    v = free_list;
    free_list = (PyIntObject *)Py_TYPE(v);
    (void)PyObject_INIT(v, &PyInt_Type);
    v->ob_ival = ival;
    return (PyObject *) v;
}
```