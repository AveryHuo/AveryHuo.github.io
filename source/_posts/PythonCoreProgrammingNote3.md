---
title: Python Core Programming Note 3
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Core Programming
- Note
---

## Multi-thread 

### Python 的 threading 模块
Python 提供了多个模块来支持多线程编程，包括 thread、 threading 和 Queue 模块等。程
序是可以使用 thread 和 threading 模块来创建与管理线程。 thread 模块提供了基本的线程和锁
定支持；而 threading 模块提供了更高级别、功能更全面的线程管理。使用 Queue 模块，用户
可以创建一个队列数据结构，用于在多线程之间进行共享。

> **核心提示：避免使用 thread 模块**
推荐使用更高级别的 threading 模块，而不使用 thread 模块有很多原因。 threading 模
块更加先进，有更好的线程支持，并且 thread 模块中的一些属性会和 threading 模块有冲突。
另一个原因是低级别的 thread 模块拥有的同步原语很少（实际上只有一个），而 threading
模块则有很多。
不过，出于对 Python 和线程学习的兴趣，我们将给出使用 thread 模块的一些代码。
给出这些代码只是出于学习目的，希望它能够让你更好地领悟为什么应该避免使用
thread 模块。我们还将展示如何使用更加合适的工具，如 threading 和 Queue 模块中的那
些方法。
避免使用 thread 模块的另一个原因是它对于进程何时退出没有控制。当主线程结束
时，所有其他线程也都强制结束，不会发出警告或者进行适当的清理。如前所述，至少
threading 模块能确保重要的子线程在进程退出前结束。
我们只建议那些想访问线程的更底层级别的专家使用 thread 模块。为了强调这一点，
在 Python3 中该模块被重命名为_thread。你创建的任何多线程应用都应该使用 threading 模
块或其他更高级别的模块。

> **核心提示：守护线程**
避免使用 thread 模块的另一个原因是该模块不支持守护线程这个概念。当主线程退出
时，所有子线程都将终止，不管它们是否仍在工作。如果你不希望发生这种行为，就要引
入守护线程的概念了。
threading 模块支持守护线程，其工作方式是：守护线程一般是一个等待客户端请
求服务的服务器。如果没有客户端请求，守护线程就是空闲的。如果把一个线程设置
为守护线程，就表示这个线程是不重要的，进程退出时不需要等待这个线程执行完成。
如同在第 2 章中看到的那样，服务器线程远行在一个无限循环里，并且在正常情况下
不会退出。
如果主线程准备退出时，不需要等待某些子线程完成，就可以为这些子线程设置守护
线程标记。该标记值为真时，表示该线程是不重要的，或者说该线程只是用来等待客户端
请求而不做任何其他事情。
要将一个线程设置为守护线程，需要在启动线程之前执行如下赋值语句：
thread.daemon = True（调用 thread.setDaemon(True)的旧方法已经弃用了）。同样，要检
查线程的守护状态，也只需要检查这个值即可（对比过去调用 thread.isDaemon()的方
法）。一个新的子线程会继承父线程的守护标记。整个 Python 程序（可以解读为：主线
程）将在所有非守护线程退出之后才退出，换句话说，就是没有剩下存活的非守护线
程时。

>当所有线程都分配完成之后，通过调用每个线程的 start()方法让它们开始执行，而不是
在这之前就会执行。相比于管理一组锁（分配、获取、释放、检查锁状态等）而言，这里只
需要为每个线程调用 join()方法即可。 join()方法将等待线程结束，或者在提供了超时时间的
情况下，达到超时时间。使用 join()方法要比等待锁释放的无限循环更加清晰（这也是这种锁
又称为自旋锁的原因）。136 第 1 部分 通用应用主题
对于 join()方法而言，其另一个重要方面是其实它根本不需要调用。一旦线程启动，它们
就会一直执行，直到给定的函数完成后退出。如果主线程还有其他事情要去做，而不是等待
这些线程完成（例如其他处理或者等待新的客户端请求），就可以不调用 join()。 join()方法只
有在你需要等待线程完成的时候才是有用的。


>使用 Thread 类，可以有很多方法来创建线程。我们将介绍其中比较相似的三种方法。选
择你觉得最舒服的，或者是最适合你的应用和未来扩展的方法（我们更倾向于最后一种方案）。
• 创建 Thread 的实例，传给它一个函数。
• 创建 Thread 的实例，传给它一个可调用的类实例。
• 派生 Thread 的子类，并创建子类的实例。
你会发现你将选择第一个或第三个方案。当你需要一个更加符合面向对象的接口时，
会选择后者；否则会选择前者。老实说，你会发现第二种方案显得有些尴尬并且稍微难以
阅读，以下示例详细介绍：

> 函数形式创建

```python
import threading as thread
from time import sleep, ctime

loops = [3,2]
def loop(nloop, nsec):
    print("thread start! :",nloop , ctime())
    sleep(nsec)
    print("thread end! :",nloop , ctime())


def main():
    print(f"starting at :{ctime()}")
    threads = []
    for i in range(len(loops)):
        t = thread.Thread(target=loop, args=(i, loops[i]))
        t.daemon = True
        threads.append(t)

    for i in range(len(loops)):
        threads[i].start()

    for i in range(len(loops)):
        threads[i].join()
    
    print("all done")

main()
```

> 类形式创建

```python
import threading as thread
from time import sleep, ctime

loops = [3,2]

class MyThread():
    def __init__(self, func, args, name=''):
        self.func = func
        self.args = args
        self.name = name
    def __call__(self):
        self.func(*self.args)
        

def loop(nloop, nsec):
    print("thread start! :",nloop , ctime())
    sleep(nsec)
    print("thread end! :",nloop , ctime())


def main():
    print(f"starting at :{ctime()}")
    threads = []
    for i in range(len(loops)):
        t = thread.Thread(target=MyThread(loop,(i,loops[i]),loop.__name__))
        t.daemon = True
        threads.append(t)

    for i in range(len(loops)):
        threads[i].start()

    for i in range(len(loops)):
        threads[i].join()
    
    print("all done")

main()
```


> 子类形式创建

```python
import threading as thread
from time import sleep, ctime

loops = [3,2]

class MyThread(thread.Thread):
    def __init__(self, func, args, name=''):
        thread.Thread.__init__(self) #Changed: need to inherit and call parent's init
        self.func = func
        self.args = args
        self.name = name

    def get_result(self):
        return self.res

    def run(self):
        print('starting', self.name, 'at: ', ctime())
        self.res = self.func(*self.args)
        print('finished', self.name, 'at: ', ctime())
        

def loop(nloop, nsec):
    sleep(nsec)


def main():
    threads = []
    for i in range(len(loops)):
        t = MyThread(loop, (i, loops[i]), loop.__name__+str(i)) #Changed:no need to use threading.Thread() method
        t.daemon = True
        threads.append(t)

    for i in range(len(loops)):
        threads[i].start()

    for i in range(len(loops)):
        threads[i].join()
    
    print("all done")

main()

```

> 实例：

```python
#my_thread.py
import threading as thread
from time import ctime

class MyThread(thread.Thread):
    def __init__(self, func, args, name=''):
        thread.Thread.__init__(self)  # Changed: need to inherit and call parent's init
        self.func = func
        self.args = args
        self.name = name

    def get_result(self):
        return self.res

    def run(self):
        print('starting', self.name, 'at: ', ctime())
        self.res = self.func(*self.args)
        print('finished', self.name, 'at: ', ctime())

```


 ```python
 #main.py
 from my_thread import MyThread
from time import ctime, sleep


def fib(x):
    sleep(0.002)
    if x < 2: return 1
    return fib(x-2) + fib(x-1)


def fac(x):
    sleep(0.1)
    if x < 2: return 1
    return x * fac(x-1)


def sum(x):
    sleep(0.2)
    if x < 2: return 1
    return x + sum(x-1)


funcs = [fib, fac, sum]
n = 12

def main():
    print("****** Single THREAD ********")
    for i in range(len(funcs)):
        print("start function %s" % funcs[i].__name__)
        print(funcs[i](n))
        print("end function %s" % funcs[i].__name__)

    threads = []
    print("****** Multi THREAD ********")
    for i in range(len(funcs)):
        t = MyThread(funcs[i], (n,), funcs[i].__name__)
        threads.append(t)

    for i in range(len(funcs)):
        threads[i].start()

    for i in range(len(funcs)):
        threads[i].join()
        print(threads[i].get_result())

    print("all done")
main()

 ```


