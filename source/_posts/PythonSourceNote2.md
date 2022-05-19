---
title: Python源码剖析-Note2
categories:
- Python
tags: 
- Python
- Note
---
# Python的内存

## 引用计数

由源码可知，Python的数据对象由PyVarObject（PyObject+size）组成，PyObject中又包含了双向链表，计数器，数据类型_typeobject对象（其中可以定制行为）

```c
/* Define pointers to support a doubly-linked list of all live heap objects. */
#define _PyObject_HEAD_EXTRA            \
    struct _object *_ob_next;           \
    struct _object *_ob_prev;

#define PyObject_HEAD                   \
    _PyObject_HEAD_EXTRA                \
    Py_ssize_t ob_refcnt;               \
    struct _typeobject *ob_type;
    
#define PyObject_VAR_HEAD               \
    PyObject_HEAD                       \
    Py_ssize_t ob_size; /* Number of items in variable part */

typedef struct {
    PyObject_HEAD
    long ob_ival;
} PyIntObject;

typedef struct {
    PyObject_HEAD
    double ob_fval;
} PyFloatObject;

typedef struct {
    PyObject_VAR_HEAD
    /* Vector of pointers to list elements.  list[0] is ob_item[0], etc. */
    PyObject **ob_item;

    /* ob_item contains space for 'allocated' elements.  The number
     * currently in use is ob_size.
     * Invariants:
     *     0 <= ob_size <= allocated
     *     len(list) == ob_size
     *     ob_item == NULL implies ob_size == allocated == 0
     * list.sort() temporarily sets allocated to -1 to detect mutations.
     *
     * Items must normally not be NULL, except during construction when
     * the list is not yet visible outside the function that builds it.
     */
    Py_ssize_t allocated;
} PyListObject;


typedef struct {
    PyObject_VAR_HEAD
    PyObject *ob_item[1];

    /* ob_item contains space for 'ob_size' elements.
     * Items must normally not be NULL, except during construction when
     * the tuple is not yet visible outside the function that builds it.
     */
} PyTupleObject;


/*
To ensure the lookup algorithm terminates, there must be at least one Unused
slot (NULL key) in the table.
The value ma_fill is the number of non-NULL keys (sum of Active and Dummy);
ma_used is the number of non-NULL, non-dummy keys (== the number of non-NULL
values == the number of Active items).
To avoid slowing down lookups on a near-full table, we resize the table when
it's two-thirds full.
*/
typedef struct _dictobject PyDictObject;
struct _dictobject {
    PyObject_HEAD
    Py_ssize_t ma_fill;  /* # Active + # Dummy */
    Py_ssize_t ma_used;  /* # Active */

    /* The table contains ma_mask + 1 slots, and that's a power of 2.
     * We store the mask instead of the size because the mask is more
     * frequently needed.
     */
    Py_ssize_t ma_mask;

    /* ma_table points to ma_smalltable for small tables, else to
     * additional malloc'ed memory.  ma_table is never NULL!  This rule
     * saves repeated runtime null-tests in the workhorse getitem and
     * setitem calls.
     */
    PyDictEntry *ma_table;
    PyDictEntry *(*ma_lookup)(PyDictObject *mp, PyObject *key, long hash);
    PyDictEntry ma_smalltable[PyDict_MINSIZE];
};


```

## 标记清除
对于list, dict, tuple 这种类型，有可能存在循环引用的情况，这时需要再做一次扫描及标记清除的处理。
* 在Python中使用另一个新的链表来存储需要标记清除的对象。然而这种扫描的往往比较耗时，需要执行可达性分析，以找到unreachable的对象，对这些对象进行标记清除。
* 因此为标记清除的处理需要找一个时间点来。 这就引入了分代机制


## 分代机制
标记清除的扫描的操作比较耗时。所以需要设置一个时间点。
* Python中设置第一代为 700个对象， 第二代为第一代的10次，第三代为第二代的10次
* 可使用python的gc模块，从业务层对这些值进行设置

## 缓存机制
一、int的缓存机制

二、字符串的缓存机制：

* intern dict ： PyDict对象，key, value就是字符串

* nullstring, characters， 空串和单串，有两个属性来存储

  > intern的默认识别只能在compile时，无法在runtime时识别，不过可以手动调用intern

![字符串缓存机制](/img/image-20210730174828153.png)

三、tuple的缓存机制

PyTupleObject， 维护一个链表，用free_list存储链表头， 20个

不用像int和string一整块的申请，利用链表的ob_item组起来

四、list的缓存机制

维护一个free_list ， 保存80个，运行时往里回放。

四、源码分析
obmalloc.c -> PyObject_Malloc

1. 申请大小大于256，直接使用 PyMem_Malloc

2. 小于256， 进入小块内存池

* 取size， 指定大小-1 后 除以8或者16字节。(设定一个block大小)

  

## 总结

![关于python机制的总结](/img/image-20210801173440707.png)
