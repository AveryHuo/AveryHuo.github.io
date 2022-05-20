---
title: CSHARP的GC
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1608690535258.png
categories:
- Unity
---

## 一、GC概述
早在1958年，由鼎鼎大名的图林奖得主John McCarthy所实现的Lisp语言就已经提供了GC的功能，这是GC的第一次出现。Lisp的程序员认为内存管理太重要了，所以不能由程序员自己来管理。但后来的日子里Lisp却没有成气候，采用内存手动管理的语言占据了上风，以C为代表。出于同样的理由，不同的人却又不同的看法，C程序员认为内存管理太重要了，所以不能由系统来管理，并且讥笑Lisp程序慢如乌龟的运行速度。的确，在那个对每一个Byte都要精心计算的年代GC的速度和对系统资源的大量占用使很多人的无法接受。而后，1984年由Dave Ungar开发的Small talk语言第一次采用了Generational garbage collection的技术（这个技术在下文中会谈到），但是Small talk也没有得到十分广泛的应用。

直到20世纪90年代中期GC才以主角的身份登上了历史的舞台，这不得不归功于Java的进步，今日的GC已非吴下阿蒙。Java采用VM（Virtual Machine）机制，由VM来管理程序的运行当然也包括对GC管理。90年代末期.net出现了，.net采用了和Java类似的方法由CLR(Common Language Runtime)来管理。这两大阵营的出现将人们引入了以虚拟平台为基础的开发时代，GC也在这个时候越来越得到大众的关注。

为什么要使用GC呢？也可以说是为什么要使用内存自动管理？有下面的几个原因：
1、提高了软件开发的抽象度；
2、程序员可以将精力集中在实际的问题上而不用分心来管理内存的问题；
3、可以使模块的接口更加的清晰，减小模块间的偶合；
4、大大减少了内存人为管理不当所带来的Bug；
5、使内存管理更加高效。
总的说来就是GC可以使程序员可以从复杂的内存问题中摆脱出来，从而提高了软件开发的速度、质量和安全性。

比较常见的算法有Reference Counting，Mark Sweep，Copy Collection等等。目前主流的虚拟系统.net CLR，Java VM和Rotor都是采用的Mark Sweep算法。

## 二、更好的方式回收非托管内存

### 1. 析构函数
析构函数的类型需要两次GC才能被完全回收。这些类型会被放到一个专门的队列里，第一次GC执行析构函数回收非托管内存，第二次ＧＣ再回收他们自身。
采用析构函数来回收可以称为被动回收，因为你不知道它什么时候被回收。但由于它需要两次GC才能被完全回收，因此就会有一些性能影响。

### 2.IDisposable接口 + using
所以最好使用主动回收的方式，类型实现IDisposable接口后，非托管内存回收的逻辑就放在Dispose函数里。
using（Type A=new Type()）{A的具体使用逻辑}
A只能再using块里使用，使用完之后就立马调用A的Dispose函数，然后回收A。

## 三、Mark-Compact 标记压缩算法

简单把.NET的GC算法看作Mark-Compact算法
    阶段1: Mark-Sweep 标记清除阶段
    先假设heap中所有对象都可以回收，然后找出不能回收的对象，给这些对象打上标记，最后heap中没有打标记的对象都是可以被回收的
    阶段2: Compact 压缩阶段
    对象回收之后heap内存空间变得不连续，在heap中移动这些对象，使他们重新从heap基地址开始连续排列，类似于磁盘空间的碎片整理
	
* !! 主要处理步骤：将线程挂起=>确定roots=>创建reachable objectsgraph=>对象回收=>heap压缩=>指针修复


* roots: heap中对象的引用关系错综复杂（交叉引用、循环引用），形成复杂的graph，roots是CLR在heap之外可以找到的各种入口点。GC搜索roots的地方包括全局对象、静态变量、局部对象、函数调用参数、当前CPU寄存器中的对象指针（还有finalizationqueue）等。主要可以归为2种类型：已经初始化了的静态变量、线程仍在使用的对象（stack+CPU register）
* Reachable objects: 指根据对象引用关系，从roots出发可以到达的对象。例如当前执行函数的局部变量对象A是一个rootobject，他的成员变量引用了对象B，则B是一个reachable object。从roots出发可以创建reachable objectsgraph，剩余对象即为unreachable，可以被回收
* 指针修复：因为compact过程移动了heap对象，对象地址发生变化，需要修复所有引用指针，包括stack、CPUregister中的指针以及heap中其他对象的引用指针

> Debug和release执行模式之间稍有区别，release模式下后续代码没有引用的对象是unreachable的，而debug模式下需要等到当前函数执行完毕，这些对象才会成为unreachable，目的是为了调试时跟踪局部对象的内容

> Pinnedobjects指分配之后不能移动位置的对象，例如传递给非托管代码的对象（或者使用了fixed关键字），GC在指针修复时无法修改非托管代码中的引用指针，因此将这些对象移动将发生异常。pinnedobjects会导致heap出现碎片，但大部分情况来说传给非托管代码的对象应当在GC时能够被回收掉


## 四、Generational 分代算法

将对象按照生命周期分成新的、老的，根据统计分布规律所反映的结果，可以对新、老区域采用不同的回收策略和算法，加强对新区域的回收处理力度，争取在较短时间间隔、较小的内存区域内，以较低成本将执行路径上大量新近抛弃不再使用的局部对象及时回收掉


* 分代算法的假设前提条件：
1、大量新创建的对象生命周期都比较短，而较老的对象生命周期会更长
2、对部分内存进行回收比基于全部内存的回收操作要快
3、新创建的对象之间关联程度通常较强。heap分配的对象是连续的，关联度较强有利于提高CPU cache的命中率


Heap分为3个代龄区域，相应的GC有3种方式: # Gen 0 collections, # Gen 1 collections, #Gen 2 collections。如果**Gen 0 heap内存达到阀值**，则触发0代GC，0代GC后Gen 0中幸存的对象进入Gen1。如果**Gen 1的内存达到阀值**，则进行1代GC，1代GC将Gen 0 heap和Gen 1 heap一起进行回收，幸存的对象进入Gen2。==2代GC将Gen 0 heap、Gen 1 heap和Gen 2 heap一起回收 #F44336==
   Gen 0和Gen 1比较小，这两个代龄加起来总是保持在16M左右；Gen2的大小由应用程序确定，可能达到几G，因此0代和1代GC的成本非常低，2代GC称为fullGC，通常成本很高。粗略的计算0代和1代GC应当能在几毫秒到几十毫秒之间完成，Gen 2 heap比较大时fullGC可能需要花费几秒时间。大致上来讲.NET应用运行期间2代、1代和0代GC的频率应当大致为1:10:100。


## 五、Finalization Queue和Freachable Queue
这两个队列和.net对象所提供的Finalize方法有关。这两个队列并不用于存储真正的对象，而是存储一组指向对象的指针。当程序中使用了new操作符在Managed Heap上分配空间时，GC会对其进行分析，如果该对象含有Finalize方法则在Finalization Queue中添加一个指向该对象的指针。在GC被启动以后，经过Mark阶段分辨出哪些是垃圾。再在垃圾中搜索，如果发现垃圾中有被Finalization Queue中的指针所指向的对象，则将这个对象从垃圾中分离出来，并将指向它的指针移动到Freachable Queue中。这个过程被称为是对象的复生（Resurrection），本来死去的对象就这样被救活了。为什么要救活它呢？==因为这个对象的Finalize方法还没有被执行，所以不能让它死去 #F44336==。

Freachable Queue平时不做什么事，但是一旦里面被添加了指针之后，它就会去触发所指对象的Finalize方法执行，之后将这个指针从队列中剔除，这是对象就可以安静的死去了。

.net framework的System.GC类提供了控制Finalize的两个方法，ReRegisterForFinalize和SuppressFinalize。前者是请求系统完成对象的Finalize方法，后者是请求系统不要完成对象的Finalize方法。

* ReRegisterForFinalize方法其实就是将指向对象的指针重新添加到Finalization Queue中。这就出现了一个很有趣的现象，因为在Finalization Queue中的对象可以复生，如果在对象的Finalize方法中调用ReRegisterForFinalize方法，这样就形成了一个在堆上永远不会死去的对象，像凤凰涅槃一样每次死的时候都可以复生。


![流程](/img/1608690535258.png)

>非托管资源：
ApplicationContext,Brush,Component,ComponentDesigner,Container,Context,Cursor,FileStream,Font,Icon,Image,Matrix,Object,OdbcDataReader,OleDBDataReader,Pen,Regex,Socket,StreamWriter,Timer,Tooltip ,文件句柄,GDI资源,数据库连接等等资源。可能在使用的时候很多都没有注意到！

 

### .NET的GC机制有这样两个问题：
首先，GC并不是能释放所有的资源。它不能自动释放非托管资源。
第二，GC并不是实时性的，这将会造成系统性能上的瓶颈和不确定性。


### 使用SuppressFinalize函数

在使用~析构函数的同时又使用了IDisposable接口的时候，Dispose函数在执行完后应该调用 GC.SuppressFinalize以阻止 GC调用Finalize方法，因为Finalize方法的调用会牺牲部分性能。

### 强制GC回收

GC.Collect(Int32, GCCollectionMode) 	
强制对零代到指定代进行即时垃圾回收。强制回收的模式



GC注意事项：

1、只管理内存，非托管资源，如文件句柄，GDI资源，数据库连接等还需要用户去管理

2、循环引用，网状结构等的实现会变得简单。GC的标志也压缩算法能有效的检测这些关系，并将不再被引用的网状结构整体删除。

3、GC通过从程序的根对象开始遍历来检测一个对象是否可被其他对象访问，而不是用类似于COM中的引用计数方法。

4、GC在一个独立的线程中运行来删除不再被引用的内存

5、GC每次运行时会压缩托管堆

6、你必须对非托管资源的释放负责。可以通过在类型中定义Finalizer来保证资源得到释放。

7、对象的Finalizer被执行的时间是在对象不再被引用后的某个不确定的时间。注意并非和C++中一样在对象超出声明周期时立即执行析构函数

8、Finalizer的使用有性能上的代价。需要Finalization的对象不会立即被清除，而需要先执行Finalizer.Finalizer不是在GC执行的线程被调用。GC把每一个需要执行Finalizer的对象放到一个队列中去，然后启动另一个线程来执行所有这些Finalizer.而GC线程继续去删除其他待回收的对象。在下一个GC周期，这些执行完Finalizer的对象的内存才会被回收。

9、.NET GC使用"代"(generations)的概念来优化性能。代帮助GC更迅速的识别那些最可能成为垃圾的对象。在上次执行完垃圾回收后新创建的对象为第0代对象。经历了一次GC周期的对象为第1代对象。经历了两次或更多的GC周期的对象为第2代对象。代的作用是为了区分局部变量和需要在应用程序生存周期中一直存活的对象。大部分第0代对象是局部变量。==成员变量和全局变量很快变成第1代对象并最终成为第2代对象。 #F44336==

10、GC对不同代的对象执行不同的检查策略以优化性能。==每个GC周期都会检查第0代对象。大约1/10的GC周期检查第0代和第1代对象。大约1/100的GC周期检查所有的对象 #F44336==。重新思考Finalization的代价：需要Finalization的对象可能比不需要Finalization在内存中停留额外9个GC周期。如果此时它还没有被Finalize,就变成第2代对象，从而在内存中停留更长时间。