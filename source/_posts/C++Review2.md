---
title: C++ 复习2
cover: false
date: 2023-02-01 18:17:56
updated: 2023-02-01 18:17:56
top_img: false
categories:
- CPlusPlus
tags: 
- C++
---
## 一、概述
C++ 起源于1983年，1.0正式版于1998年发布又叫C++98。 2.0版本为C++11（即2011年推出的大版本）。
C++ 简单来说由 语言+标准库组成

C语言的缺点：数据-> 函数的处理方式，导致数据一定是全局才能给各个函数处理。这时C++的面向对象思想就解决了这一问题
c++ 用 class 将member data和member function包在一起来创建object
延展文件名（extension file name）不一定是.h或.cpp，可能是.hpp甚至没有。

## 二、文件头与类

### 2.1 Header（头文件）中的防卫式声明（guard）
为了防止多次include复制执行，保证只被一次include，使用防卫式声明。
```c++
#ifndef __COMPLEX__
#define __COMPLEX__
内容
#endif
```
> 建议所有头文件都有这个声明

### 2.2 头文件内容布局
前置声明
```c++
class complex; 
```

+ 类声明
```c++
class complex{....}
```
+类定义
```c++
complex::function ...
```
### 2.3 模板类的初探
根据使用者需要的类型来决定：
```c++
template<typename T> //模板
class complex
{
public：
    complex(T r = 0, T i = 0)
        : re(r),im(i)   //initialization list（初值列，初始列）
    {}
    complex& operator += (const complex&);
    T real() const {return re;} //函数若在class body内定义，便会自动定义完成，变自动成为inline候选人
    T imag() const {return im;}
private：
    T re,im;
    
    friend complex& __doapl(complex*, const complex&);
};

complex<double> c1(1.2,2.1);
complex<int> c1(1,2);
```
### 2.4 inline
相较于没有inline标识，会更快，通常于class内定义的函数会成为inline的候选人。对外部的需要自己加inline来设置。
> 只是给编译器的建议，是否能变成inline取决于编译器是否能够。
```c++
inline double imag(const complex& x){
    return x.imag();
}
```

### 2.5 构造函数

```c++
complex c1(2，1);
complex c2;
complex* p = new complex(4);
```
> 构造函数还可以给默认值

```c++
complex(T r = 0, T i = 0) : re(r),im(i)   //initialization list（初值列，初始列）{}
```
初值列与初始列的写法与写到函数内实质上是一样的。但区别的是，变量的赋值分为初始化和赋值化阶段，初值列就是分出来初始化的阶段。

> 不带指针的类，多半不用写析构函数

### 2.6 函数重载
常出现在构造函数上。对于有默认参数的情况下，重载可能会错误

### 2.7 Private域的构造函数
一般情况下，构造函数不放在private，因此放在private就不允许创建了。
但是对于单例模式下就可以使用private构造函数。
```c++
class A{
public:
    static A& getInstance();
    setup(){...}
private:
    A();
    A(const A& rhs);
    ...
};
A& A::getInstance()
{
    static A a;
    return a;
}
```
### 2.8 const
对于不改变数据的函数的，在花括号前加const。但const也需要保证统一性，如果在类对象为const时，则不可以调用非const函数了。如
```c++
const complex c1(2,1);
cout << c1.real(); //如果real()没加const标识，这里就会报错
cout << c1.imag(); //如果 imag()没加const标识，这里就会报错
```
### 2.9 pass by value/refrence
1. value 
整个压到函数栈里
```c++
complex(T r = 0, T i = 0) 
```
2. reference
推荐：尽量传引用
底层就是指针的形式，传引用就是传指针
```c++
//如果函数体内修改，则会报错。注意如果不加const，则会对原地址内内容影响
complex& operator += (const complex&);
```
### 2.10 return by value/refrence
1. value
2. reference
传递者无需知道接收者是以reference形式传递。
推荐使用
```c++
complex& operator += (const complex&);
```

### 2.11 friend
friend函数内可以直接拿对象中的Private数据
```c++
friend complex& __doapl(complex*, const complex&);
...
inline complex&
__doapl (complex* ths,const complex& r){
    ths->re += r.re;
    ths->im += r.im;
    return *ths;
}
```

class内对于其他同类对象来说，是互为友元的！
```c++
T func(complex &param){
	return param.re + param.im;//不报错，可以直接拿到re, im私有变量
}

//以下调用是成功的
complex<double> a(1.3,4.5);
complex<double> b;
std::cout << b.func(a) << std::endl;
```
### 2.12 传递方式的选择
对于函数体内新建对象的返回，不能传引用，因为此对象为局部的，离开函数即被销毁。
```c++
inline complex& __doapl(complex* ths, const complex& r){
    ths->re += r.re;    //第一参数将会被改动
    ths->im += r.im;    //第二参数不会被改动
    return *ths;
}

inline complex& complex::operator += (const complex& r){
    return __doapl(this,r);
}
inline T imag(const complex& x){
    return x.imag();
}
inline T real(const complex& x){
    return x.real();
}
```

### 2.13 操作符重载
在C++中，操作符运算也可以是一种函数
成员函数(带有this指针的情况)：
```c++
// c2 += c1 成员函数内的第一个参数实际应为this，但被默认隐藏了，这个this就是c2
inline complex& 
complex::operator += (const complex& r){
    return __doapl(this, r);
}
//一个有趣的事情是，可以把返回值改为void，这样也能支持c2+=c1，但无法支持c3+=c2+=c1这种连串的表达式。
```

非成员函数，没有this的pointer，全域的函数：
```c++
template<typename T>
inline T imag(const complex<T>& x){
    return x.imag();
}
template<typename T>
inline T real(const complex<T>& x){
    return x.real();
}

template<typename T>
inline complex<T>
operator + (const complex<T>& x, const complex<T>& y){
    return complex<T>(real(x) + real(y),
                   imag(x) + imag(y));
}

template<typename T>
inline complex<T>
operator + (const complex<T>& x, const T& y){//这里需要对y参数加const，不然就无法使用实际的右值做为参数，加了const可以做为右值使用
    return complex<T>(real(x) + y, imag(x));
}

template<typename T>
inline complex<T>
operator + (const T& x,const complex<T>& y){
    return complex<T>(x + real(y), imag(y));
}

//此函数是可以改成return by reference
template<typename T>
inline complex<T>
operator + (const complex<T>& x){
    return x;
}
template<typename T>
inline const complex<T>&
operator + (const complex<T>& x){
    return x;
}/

template<typename T>
inline complex<T>
operator - (const complex<T>& x){
    return complex<T>(-real(x), -imag(x));
}

complex<double> a(1.3,4.5);
complex<double> b(1.3,4.5);
complex<double> c;
c = a + b;
std::cout << c.real() << std::endl;
c = b + 5.1;
std::cout << c.real() << std::endl;
c = 5.1 + a;
std::cout << c.real() << std::endl;
c = + a; // 1.3
std::cout << c.real() << std::endl;
c = - a; // -1.3
std::cout << c.real() << std::endl;
```

共轭复数：
```c++
//共轭复数：实部相同，虚部相反
template<typename T>
inline complex<T> conj(const complex<T>& x){
    return complex<T>(real(x), -imag(x));
}
```

### 2.14 临时对象
直接在类型后用（）生成临时对象，代码离开后就被销毁。标准库中大量使用
```c++
complex<double>(1.4,4.5);
```

### 2.15 << 符号
output operator 输出运算符：此类运算符，只能为非成员函数，全局。因此相当于值入ostream对象中，无法用在成员函数

<< ： 右侧往左侧作用。
```c++
template<typename T>
inline std::ostream&
operator << (std::ostream& os, const complex<T> &x){
    return os << '(' << x.real() << ',' << x.imag() << ')' << std::endl;
}
std::cout << c;
```

### 2.16 class 关注点总结
1. 构造函数的初始值定义
2. 函数的const定义
3. 参数传递尽量用reference
4. return 的reference的考虑
5. 数据需要在private，函数多数是public
