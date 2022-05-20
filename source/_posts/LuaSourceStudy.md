---
title: Lua源码研究
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---


## 一、版本更替

Lua 5.4 : Lua 5.4 was released on 29 Jun 2020     The current release is Lua 5.4.2, released on 03 Dec 2020.
> Main changes
new generational mode for garbage collection           垃圾收集的新分代模式
to-be-closed variables           可close的变量
const variables                  常量变量
userdata can have multiple user values Userdata                    可以有多个用户值
new implementation for math.random                          Math.random 的新实现
warning system               报警系统
debug information about function arguments and returns     有关函数参数和返回值的调试信息
new semantics for the integer 'for' loop                 整数‘ for’循环的新语义
optional 'init' argument to 'string.gmatch'           可选的“ init”参数设置为“ string.gmatch”
new functions 'lua_resetthread' and 'coroutine.close'        新函数‘ lua _ resetthread’和‘ coroutine.close’
string-to-number coercions moved to the string library       字符串到数字的强制转移到字符串库
allocation function allowed to fail when shrinking a memory block          缩小内存块时允许失败的分配函数
new format '%p' in 'string.format'                      新格式“% p”中的“ string.format”
utf8 library accepts codepoints up to 2^31                          Utf8库接受最多2 ^ 31的代码点


Lua 5.3 : Lua 5.3 was released on 12 Jan 2015    The current release is Lua 5.3.6, released on 25 Sep 2020
>There will probably be no further releases of Lua 5.3.
integers (64-bit by default)  整数(默认为64位)  Lua5.2中所有数字都是浮点数
official support for 32-bit numbers  32位数字的官方支持
bitwise operators    按位运算符
basic utf-8 support 基本 utf-8支持
functions for packing and unpacking values   包装和拆包 数值的函数
垃圾收集器的分代模式被删除了

Lua 5.2 : was released on 16 Dec 2011.  The last release was Lua 5.2.4, released on 07 Mar 2015. There will be no further releases of Lua 5.2.
> Main changes:
yieldable pcall and metamethods
new lexical scheme for globals:  全局变量的新词法模式
ephemeron tables : 
new library for bitwise operations
light C functions
emergency garbage collector
goto statement
finalizers for tables
> module函数已被弃用。使用常规的Lua代码设置一个模块很容易。不再期望模块设置全局变量。
setfenv和getfenv函数被删除，因为环境概念的更改。
math.log10函数已被弃用。可以使用math.log并向第2个参数传入10来代替。
loadstring函数已被弃用。使用load代替，它现在可以接受字符串参数且等同于loadstring。
table.maxn函数已被弃用。如果你确实需要请在Lua中自己实现。
os.execute函数现在如果命令成功终止则返回true，否则返回nil和一个错误消息。
unpack函数被移到table库中，因此要改成这样调用 table.unpack。
模式中的字符类%z已被弃用，因为现在模式可以包含\0作为正常字符。
表package.loaders重命名为package.searchers。
Lua不再有字节码验证。所以，所有加载代码的函数(load和loadfile)在加载不信任的二进制数据时都可能有潜在的不安全。(实际上，由于验证算法的缺陷，这些函数一直都是不安全的)。如有疑惑，请将这些函数的mode参数限制为只加载文本的块。
官方发布包中的标准路径可能会在不同版本间修改。


Lua jit: 
LuaJIT 是按照 5.1 的语法设计的，并且在可以预期的将来也永远不会适配 5.2，LuaJIT 作者声称会增加 5.2 所增加的那些功能，但永远不会适配 5.2 的语法，换句话说，他的发展思路是语法与兼容性不变，仅仅在 5.1 的语法基础之上增加后续 Lua 版本的新特性，LuaJIT 在 API/ABI 方面都只兼容 Lua 5.1.4。

## 二、LUA 5.4新特性

参考： https://zhuanlan.zhihu.com/p/283055561

Lua 5.4语法上最大的变化是增加了const和TBC变量，前者完全由编译器支持，后者则由专门的TBC指令支持。Lua 5.4对整数for循环语义进行了调整，控制变量溢出会导致循环结束。算术和按位运算在Lua 5.3里会自动将字符串转换为浮点数，在Lua 5.4里，这一自动转换不再由语言直接支持，改为由string标准库的元方法支持（仅支持算术运算，且转换时会保留整数类型）。Lua 5.4不再使用__lt模拟__le元方法（但可通过配置兼容Lua 5.3）。此外，Lua 5.4还增加了新的分代GC模式，重新实现了math.random()函数，等等。

### 1. const语法

``` lua
local a <const> = 4
local b = a + 7
print(b)
```
编译器会把a消除掉，直接给b赋11。这种优化是有限的，对于基本类型和字符串，能够有效减少寄存器的访问，但对于table貌似益处不大。代码文件如果需要一些数值常量，可以写成const变量，比如：

``` lua
local MAX_LEN <const> = 20
function check_name(name)
    return #name <= MAX_LEN
end
```
在check_name中就没有upvalue的访问，而是直接转换成和20的比较。

### 2. close语法

close变量(To-be-closed Variables)需要和close元方法结合使用，在变量超出作用域时，会调用变量的close元方法，这听起来是不是有点像C++的RAII用法。下面是一个例子：

``` lua
local function newlock()
    local lock = {
        acquire = function()
            print("acquire lock")
        end,
        release = function()
            print("release lock")
        end,
    }
    return lock
end

local function lockguard(lock)
    local wrap = {
        lock = lock
    }
    lock.acquire()
    return setmetatable(wrap, {__close = function(t, err)
        t.lock.release()
    end})
end

local lock = newlock()
do
    for i = 1, 3 do
        local l <close> = lockguard(lock)
        print(i)
        error("err")
    end
end
```
定义local l /<close/>后，无论是否有错误，release都能得到调用；从这个例子也可以看出，close变量一般用于需要及时释放资源的情况；否则Lua的GC可以应付大多数情况。

### 3.userdata
userdata现在可以关联多个user值，C的API也有相应的修改，如果我们新建的userdata没有关联值，则尽量使用lua_newuserdatauv，这样更高效，lua_newuserdata仅仅为了兼容，且默认会关联1个值。

### 4. math.random
math.random使用了新的实现，会从某个随机种子开始，简单说即程序启动后第1次调用math.random会得到不同值；以前版本都从相同值开始。

### 5.协程库新API
协程库提供了新的APIcoroutine.close和lua_resetthread，coroutine.close只能在挂起或死亡状态下调用，挂起状态下会使用协程进入死亡状态，并且关闭所有的close变量。


### 6.整数for循环
循环达到最近的整数就会停止

如果在Lua 5.3里执行这段代码，那么会进入死循环。但是在Lua 5.4里，只打印4个整数就结束循环了：

``` lua
$ lua-5.4.1/lua -
for i = math.maxinteger - 10, math.maxinteger, 3 do
  print(i)
end
^D
9223372036854775797
9223372036854775800
9223372036854775803
9223372036854775806
```

### 7.str-to-num语言特性变更
变化一： 在Lua 5.3里，str-to-num类型转换是由语言（和虚拟机）直接支持的。在Lua 5.4里，改为由string标准库通过元方法支持。

以下代码在5.3中只输出一个index元方法，5.4中却输出很多
``` lua
local s = "foo"
local mt = getmetatable(s)
print(mt)
for k,v in pairs(mt) do
  print(k,v)
end
```

``` lua
--5.4输出
table: 0133A450
__idiv  function: 0033AA40
__index table: 0133A590
__pow   function: 0033A960
__div   function: 0033A9D0
__mul   function: 0033A880
__sub   function: 0033A810
__unm   function: 0033AAB0
__add   function: 0033A7A0
__mod   function: 0033A8F0
```
变化二：在一的元方法列表中并未找到按位运算的元方法，因此会导致自动按位运算不支持
变化三：str-to-num会尽量为整数类型返回

### 8. le元方法
Lua 5.3认为a <= b和not (b < a)等价，因此如果元表没有提供__le元方法，那么将尝试用__lt元方法进行模拟。Lua 5.4不再认同这个假设，因此必要时必须显示提供__le元方法。下面来看一个例子：

``` lua
local mt = {
  __lt = function(a, b)
    print("__lt", a, b)
    return #a < #b
  end
}
local a = {1, 2, 3}
local b = {1, 2, 3, 4}
setmetatable(a, mt)
setmetatable(b, mt)
print(a < b)
print(a <= b)
```
Lua 5.4源代码提供了一个LUA_COMPAT_LT_LE宏，用来控制__le的行为是否和Lua 5.3保持一致，所以上面这个例子的具体执行结果取决于lua被编译时给定的配置。这个宏在Lua 5.3的构建文件（Makefile）里默认是被打开的。

### 9.警告系统

Lua 5.4增加了warn()标准库函数，用于发布警告，用法为：warn (msg1, ···)。相应的，lua命令增加了一个-W选项。只有该选项开启，警告才会被打印到控制台。下面是一个简单的例子：

``` lua
warn("foo", "bar")
^D
Lua warning: foobar
```

### 10.string库

#### gmatch()函数
增加了可选的init参数，用法如下所示：

``` lua
string.gmatch (s, pattern)          -- Lua 5.3
string.gmatch (s, pattern [, init]) -- Lua 5.4

s = "hello world from Lua"
for w in string.gmatch(s, "%a+", 3) do
  print(w)
end
```
在Lua 5.4里执行，结果如下所示（注意第一行的llo）：
llo
world
from
Lua

#### format()函数

增加了%p格式，可以打印指针，下面是一个例子：

``` lua
local t = {1, 2, 3}
print(t, ",", string.format('%p', t))
```

在Lua 5.4里执行，打印出的结果看起来是下面这样：

``` lua
table: 0x7fde1cd04a30   ,   0x7fde1cd04a30
```
### 11.垃圾回收
Lua 5.4给垃圾收集器（GC）增加了分代模式，可以通过collectgarbage()函数在老的增量模式和新模式之间切换（以及调整控制GC的参数）：

``` lua
-- Change the collector mode to generational.
collectgarbage("generational", minor_mul, major_mul)
-- Change the collector mode to incremental.
collectgarbage("incremental", pause, step_mul, step_size)
--同时，原先的两个选项setpause和setstepmul已经被废弃：

collectgarbage("setpause", pause)      -- deprecated
collectgarbage("setstepmul", step_mul) -- deprecated
```

## 三、相关知识点复习

### 元表与元方法

1. index元方法
这是metatable最常用的键

当你通过键来访问table的时候，如果这个键没有值，那么Lua就会寻找该table的metatable(假定有metatable)中的__index键。如果index 包含一个表格，Lua会在表格中查找对应的键。

如果index包含一个函数的话，Lua就会调用那个函数，table和键会作为参数传递给函数。

> !!! 取值的时候，查看是否存在，如果有值则显示值 ，没有则调用index元方法，找元方法中的值 

``` lua
mytable = setmetatable({key1 = "value1"},
	{__index = function(mytable,key)
	if key == "key2" then 
		return "metatablevalue"
	else 
		return nil
	end 
end 
})
print(mytable.key1,mytable.key2)

--实际输出结果为：
--value1 metatablevalue
```


2. newindex元方法

> 赋值的时候，如果有值 ，则取值，没有值，则会触发newindex元方法，如果元方法是一个table，则会用此table替代原table

``` lua
mymetatable = {}
mytable = setmetatable({key1 = "value1"},{__newindex = mymetatable})
print(mytable.key1)
mytable.newkey = "新值2"
print(mytable.newkey,mymetatable.newkey)
mytable.key1 = "新值1"
print(mytable.key1,mymetatable.key1)
--以下实例执行输出结构为：

--value1
--nil    新值2
--新值1    nil
```


## 四、LUA GC
Lua是一门自动内存管理的语言，它使用的是经典的标记和清扫算法。

### 4.1 标记和清除模式
在标记阶段，从根集对象开始标记，把整个对象层级都标记完，这些被标记到的对象称为可到达的对象。
在清扫阶段，遍历上面提到的对象链表，如果对象被标记过则擦除标记并跳过，如果对象没被标记，说明它不可到达，那就把它释放掉。

> Lua 5.0之前，垃圾回收是一个stop the world的过程，即在执行GC的时候要一次性完成，它的好处是代码相对简单，5.0的GC代码不过几百行，如果你想了解GC算法本身，看一下5.0的lgc.h|c是非常好的。
这种stop the world的GC在轻量的应用中不是什么问题，如果遇到程序非常大，对象特别多的情况，效率就很成问题了。因此在5.1之后，Lua进化成一个步进的GC，原理还是标记和清扫，但是把一个GC周期分成很多步，一次只执行一步。这对GC的效率是一个很大的提升，代价就是GC代码变得很复杂，Lua 5.3已经有一千多行。
从代码上看，除了GC分步，还有upvalues，弱表，终结对象(有__gc元方法的对象)的处理，这些都加大了垃圾回收的复杂度。


#### 三色标记
一个GC对象分成三种颜色(三种状态):

白色：表示对象未被标记，在GC周期开始之前对象为白色，如果到清扫阶段还是白色，那就说明该对象不可到达，要被清除掉。
灰色：表示对象本身已标记，但它引用的对象未被标记，比如一个表已被标记，它的键值对象还未标记。这表示对象标记的一个中间状态。
黑色：表示对象和它引用的对象都已被标记，在清扫阶段黑色对象为可到达对象。

marked就是对象的标记状态，它的位含义如下：

第0位：第1种白
第1位：第2种白
第2位：黑
第3位：标记为终结对象
灰色为0, 1, 2位都清0的情况。

我们注意到白色有两个状态，这是为了解决分步GC的中间新建对象的问题。比如在标记阶段和清扫阶段的中间，有一个新建的对象，它默认为白色；清扫的时候会因为它是白色而把它给释放掉。引入两种白色之后这样处理：

>g->currentwhite表示当前白，它是两种白色中的任意一种，我们假定为白1，在清扫阶段之前，所有白对象都是白1。
>在标记阶段结束的时候，g->currentwhite切换为白2，现在之前那些白对象和g->currentwhite就是不同白了(因为它们是白1)。
>在标记结束之后，清扫开始之前，新建一个对象，默认标记当g->currentwhite，也就是白2。
>>在清扫的时候，只会清扫和g->currentwhite不同的白，即白1。这样那些新建的对象就不会在清扫阶段被释放。而在清扫结束之后，这些新建的对象也会变成白2。等待下一个周期。
要被终结对象就是那些有__gc元方法的对象。


#### 对象链表
global_State有好多和GC相关的字段，其中有一些重要链表。所有GC对象总是在下面的一个链表中：

allgc 所有未被标记为终结的对象
finobj 所有被标记为终结的对象
tobefnz 所有准备终结的对象(准备调用__gc的对象)
fixedgc 不会被回收的对象

> gfasttm(g,mt, TM_GC)函数: 如果给对象设置一个元表，且元表有__gc元方法，那么它会从allgc取出，加入到finobj去，并设置对象的FINALIZEDBIT标记位(就是上面说的第3个marked位)。 

在标记阶段，finobj中的白对象会移到tobefnz链表去，然后标记这些对象，这样当前周期不会释放这些对象；清扫完之后会进入GCScallfin阶段，在这里调用tobefnz对象的gc方法，同时把对象移回allgc链表；如果gc中使对象重新变成可到达，则对象复活过来；否则下个周期这个对象就会被正常清除。

fixedgc 是那些不会被回收的对象，在新建完对象后，必须马上调用luaC_fix把对象从allgc移到fixedgc去。GC的过程不会对fixedgc进行清扫。

对于灰对象还有好几个链表：

gray 普通的灰对象链表
grayagain 在GCSatomic阶段(是标记阶段的一个子阶段)中重新访问的灰对象，这些灰对象包括：
进行写屏蔽的黑对象
在传播阶段的弱表
所有线程对象

weak 待清理的弱值表
allweak 待清理的弱键值表
ephemeron 弱键表
可以看出这些灰对象链表是由分步和弱表引入的附加数据结构，这也是GC中较为复杂的部分。

#### 写屏障
从前文的描述知道，Lua的GC不断的遍历灰对象并把它们变黑，在遍历的过程中又有新的灰对象产生，一直重复这个过程到没有灰对象为止。此时黑对象就是可到达的对象，剩下的白对象就是不可到达的对象，要被清扫掉的。

在标记阶段中有一个重要的不变条件是：黑对象不能指向白对象。比如我们有一个普通的表是黑色的，那这个表必然已经被遍历过了，所以它里面的键值一定不是白色的。

但这个假设只是在一次性标记这个前提下成立。如果是增量式的，每次只标记一部分，那在标记的中间有一些修改，可能会打破这个不变式。比如t被标记为黑色，后面有一个赋值t.x = {}使得t指向了白色对象。