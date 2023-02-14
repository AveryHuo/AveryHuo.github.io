---
title: C++ 复习2
cover: /img/image-20230202174221474.png
date: 2023-02-01 22:43:40
updated: 2023-02-09 17:33:42
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

## 三、设计类-BIG Three

### 3.1 BIG Three 1 - 拷贝构造
当构造函数，接收的是与自己相同类型的引用时，这个称为拷贝构造

### 3.2 BIG Three 2 - 拷贝赋值
流程：自我检测（指针相同？） + 清空自己内容 + 拷贝源 + 目标赋值操作
对比拷贝构造，当变量不是已构造的方式位于左值时，以赋值的方式时就为拷贝赋值
```c++
//以下两行完全等价,因为s2都是新创建出来的对象
String s2(s1);
String s2 = s1; 
```

### 3.3 BIG Three 3 - 析构
销毁时调用

> string的设计，方案1是在char前加一个长度符，如pascal使用的方式的，另一种方案，就是把在结尾添加一个\0的结尾符，如C/C++的实现方案

### 3.4 带指针成员的类一定要有BIG Three
因此编译器默认生成的拷贝函数，是浅拷贝，导致内存泄漏

### 3.5 BIG Three的实现：
```c++
class String{
public:
    String(const char *ctr = nullptr);
    String(const String&);// copy constructor
    String& operator=(const String&); // copy assignment
    ~String();
    const char* get_cstr() const {return m_data;};
private:
    char * m_data;
};

//必须为非成员函数，原理实际上是cout的运算符重载实现！
inline std::ostream&
operator << (std::ostream& os, const String &x){
    return os << '(' << x.get_cstr() << ')' << std::endl;
}

inline
String::String(const char *ctr) {

    if(ctr){
        m_data = new char[strlen(ctr)+1];
        strcpy(m_data, ctr);
        std::cout<< "Normal constructor- has value" << *this << std::endl;
    }else{
        m_data = new char [1];
        *m_data = '\0';
        std::cout<< "Normal constructor- no value" << *this << std::endl;
    }
}

inline
String::String(const String &src) {
    m_data = new char [strlen(src.get_cstr()) + 1];
    strcpy(m_data, src.get_cstr());
    std::cout<< "Copy constructor" << *this << std::endl;
}

inline
String &String::operator=(const String &src) {
    if(this == &src){
        std::cout<< "Self copy=  skip" << *this << std::endl;
        return *this;
    }
    delete[] m_data;
    m_data = new char [strlen(src.get_cstr()) + 1];
    strcpy(m_data, src.get_cstr());
    std::cout<< "copy=" << *this << std::endl;
    return *this;
}

inline
String::~String() {
    std::cout<< "deconstruct" << *this << std::endl;
    delete[] m_data;
}
String s1("Hello"); 
String s2("Hello2");
String d1(s1); 
String d2 = s1; //注意这个还是拷贝构造函数，因为是创建
d2 = s2;
```

## 四、栈，堆与内存管理
32位机器中，一个指针是个四个字节
### 4.1 栈stack
存在于某个作用域内的内存空间。如调用函数时，函数本身即生成一个stack用于存放接收的参数。在函数体内声明的任何变量，都在这个stack内。

### 4.2 堆heap
system heap，由操作系统提供一块全局的内存空间，这块空间需要动态去取得。

实例：
```c++
complex c1(1,2); // 栈上
complex * p= new complex(3); // 堆上
static complex c1(1,2); //静态变量，虽然在栈上，但不会销毁，直到程序结束
```

### 4.3 作用域内存泄漏
作用域内的定义的指针会在离开时结束生命，所以在所指的内容不销毁的情况下，会造成指针无法获取销毁

### 4.4 new的原理
C++的new的过程：
以 下以这个为例：

```
Complex * pc = new Complex(1,2)
```


```c++
Complex *pc;

void * mem = operator new(sizeof(Complex));
pc = static_cast<Complex *>(mem);
pc->Complex::Complex(1,2);
```

### 4.5 delete的过程
以下为例：
```
String * ps = new String("Hello");
delete ps;
```

```c++
Complex::~Complex(ps);//析构
operator delete(ps);//释放内存

```

### 4.6 内存管理
操作系统默认是16的倍数分配，且头尾的cookie即为分配的大小的16进制，最后一位表示放出去则为1，回收回来即为0
![image-20230202174221474](/img/image-20230202174221474.png)

对于数组的情况
![image-20230202181136848](/img/image-20230202181136848.png)

> 对于数组new完没有用delete[]而只用delete的情况，实际上delete也会释放整块的空间，但是必须连上括号才会让编译器知道需要调用几次析构，所以实际上对于没有指针的类是可以支持delete没有array，但从规范上还是要求搭配使用

![image-20230202181416205](/img/image-20230202181416205.png)

> 引用符号出现在typename后面，表示引用，出现在变量前面，表示取地址


## 五、类扩展

### 5.1 static
对于非成员函数，会有一个隐藏的this指针来管理此类函数，因为函数需要处理多个实例数据，这时当前对象的地址就被会传入进去。

* 在变量或函数前加static让其变为静态，静态函数只能处理静态数据。
* 静态函数可以通过classname或object来调用。
初步优化的单例简单写法：
```c++
class A{
public:
    static A& getInstance();

};

A& A::getInstance() {
    static A a;
    return a;
}
```

### 5.2 cout
cout 是标准库中继承自ostream的类，其中实现了各种类型的<<运算符

### 5.3 类模板
使用 template class T 的方式实现类模板

### 5.4 namespace
与C#的类似，把代码块包装起来：
```c++
namespace std
{
....
}

//使用1
using namespace std;
//使用2
using std::cout;
//使用3 直接使用
std::cout 
```

## 六、类关系-Composition
### 6.1 复合关系，拥有。has-a, 实心菱形为起点，指向包含的对象
```c++
template<class T>
class queue{
protected:
dequeue<T> c;

}
```

### 6.2 Adaptor模式
适配器，理解为封装的思想，进行适配改造。

### 6.3 构造与析构
构造： 先构造内部的Component，再构造自己。 默认行为下，编译器会先调用Component的默认构造函数，如果需要指定构造函数，需要在当前类构造下做出指定。
析构：先析构自己，再析构各个component。 在函数内也需要先释放自己的资源，再释放components

## 七、类关系-Delegation
Composition by reference. 空心菱形指向目标对象。 
如下则是String与StringRep委托关系，此种实现叫pImpl, pointer to implementation，或者Handle and Body。 String就是Handle，StringRep就是Body。
```c++
class String{
private:
StringRep * rep;
}
```
> Copy on write, 对于共享环境下的写入操作，产生一个副本来做做为对象，以不影响其他引用。

## 八、类关系-Inheritance
is-a 继承， 子类指向父类，终点使用空心三角形。 
### 8.1 子类对象包着父类的东西，父类以一个PART形式存在于子类。
public继承

以下继承主要为了继承父类的数据
```c++
template<typename _Tp>
struct _List_node: public _List_node_base{
	_Tp _M_data;
}
```

### 8.2 构造与析构
构造，由内而外（父就是内）：先父类的default构造，再子类自己的
析构，由外而内： 先执行自己，再执行父类的

基类的析构必须是virtual ，否则 会出现Undefined behavior
> 当子类有组合关系存在时，构造仍然是以父类最先的方式再子类Component最后再是子类自己

### 8.3 virtual
基类的函数默认为非虚函数 ， impure virtual 为添加virtual的函数，希望子类去重定义。
pure virtual纯虚函数，同时添加const = 0在后面，表示一定要子类重定义。


## 九、常见的设计模式

### 9.1 Template Method
这是一种设计模式：设计一个函数为虚函数，且在父类流程（框架中）是固定会执行的，留下此函数让未来的子类来实现。

### 9.1 观察者模式
使用委托+继承
![image-20230207142409951](/img/image-20230207142409951.png)

### 9.2 Composite

![image-20230207143817602](/img/image-20230207143817602.png)

### 9.3 Prototype
一种解法：子类必须有一个静态自己，必须有一个私有构造并在其中调用父类的addprototype，让父类调用到clone生成自己
![image-20230207150459069](/img/image-20230207150459069.png)


实现细节：父类
![image-20230207151629369](/img/image-20230207151629369.png)

实现细节：子类

![image-20230207153822048](/img/image-20230207153822048.png)



```c++
#ifndef LEARN01_IMAGE_H
#define LEARN01_IMAGE_H
#include "ImageType.h"
class Image{
public:
    virtual void Draw() = 0;
    static Image* FindAndClone(ImageType);
    static Image* GetPrototype(ImageType);
    static void AddPrototype(Image* p){
        Prototypes[NextSlot++] = p;
    }
protected:
    virtual ImageType getImageType() const = 0;
    virtual Image* clone() const = 0;
    static Image* Prototypes[10];
    static int NextSlot;
};

Image* Image::Prototypes[];
int Image::NextSlot;

Image* Image::FindAndClone(ImageType t) {
    for(int i = 0; i < NextSlot; i++){
        if(Prototypes[i]->getImageType() == t)
            return Prototypes[i]->clone();
    }
}

Image* Image::GetPrototype(ImageType t) {
    for(int i = 0; i < NextSlot; i++){
        if(Prototypes[i]->getImageType() == t)
            return Prototypes[i];
    }
}

#endif //LEARN01_IMAGE_H

#ifndef LEARN01_LANDANDSATIMAGE_H
#define LEARN01_LANDANDSATIMAGE_H
#include <iostream>
#include "Image.h"

class LandAndSatImage:public Image{
public:
    LandAndSatImage(int dummy){
        _id = count++;
        std::cout<< "Construct LandAndSatImage:" << _id << std::endl;
    }
    void Draw() override{
        std::cout<<_id<<":Draw LandAndSatImage"<< std::endl;
    }
    Image* clone() const override{
        return new LandAndSatImage(1);
    }
    ImageType getImageType() const override{
        return LSAT;
    }
    ~LandAndSatImage(){
        std::cout<< "Deconstruct LandAndSatImage:" << _id << std::endl;
    }
private:
    int _id;
    static LandAndSatImage _LandAndSatImage;
    static int count;
    LandAndSatImage(){
        std::cout << "add LandAndSatImage prototype" << std::endl;
        AddPrototype(this);
    }
};

LandAndSatImage LandAndSatImage::_LandAndSatImage;
int LandAndSatImage::count = 1;


#endif //LEARN01_LANDANDSATIMAGE_H

#ifndef LEARN01_SPOTIMAGE_H
#define LEARN01_SPOTIMAGE_H
#include <iostream>
#include "Image.h"

class SpotImage:public Image{
public:
    SpotImage(int dummy){
        _id = count++;
        std::cout<< "Construct SpotImage:" << _id << std::endl;
    }
    void Draw() override{
        std::cout<<_id<<":Draw SpotImage"<< std::endl;
    }
    Image* clone() const override{
        return new SpotImage(1);
    }
    ImageType getImageType() const override{
        return SPOT;
    }
    ~SpotImage(){
        std::cout<< "Deconstruct SpotImage:" << _id << std::endl;
    }
private:
    int _id;
    static SpotImage _SpotImage;
    static int count;
    SpotImage(){
        std::cout << "add SpotImage prototype" << std::endl;
        AddPrototype(this);
    }
};

SpotImage SpotImage::_SpotImage;
int SpotImage::count = 1;

#endif //LEARN01_SPOTIMAGE_H

//main
cout << "------------------------------------- Prototype ----------------------------" << endl;
LandAndSatImage * lsatInstance1 = static_cast<LandAndSatImage*>(Image::GetPrototype(LSAT));
lsatInstance1->Draw();
//    delete lsatInstance1; //删除原型就没了，后面就无法使用了

LandAndSatImage * lsatInstance2 = static_cast<LandAndSatImage*>(Image::FindAndClone(LSAT));
lsatInstance2->Draw();
delete lsatInstance2;

LandAndSatImage * lsatInstance3 = static_cast<LandAndSatImage*>(Image::FindAndClone(LSAT));
lsatInstance3->Draw();
delete lsatInstance3;

SpotImage * spotInstance = static_cast<SpotImage*>(Image::FindAndClone(SPOT));
spotInstance->Draw();
delete spotInstance;

//OUTPUT
add LandAndSatImage prototype
add SpotImage prototype
------------------------------------- Prototype ----------------------------
0:Draw LandAndSatImage
Construct LandAndSatImage:1
1:Draw LandAndSatImage
Deconstruct LandAndSatImage:1
Construct LandAndSatImage:2
2:Draw LandAndSatImage
Deconstruct LandAndSatImage:2
Construct SpotImage:1
1:Draw SpotImage
Deconstruct SpotImage:1
    
Deconstruct SpotImage:0
Deconstruct LandAndSatImage:0
```

## 10、Conversion Function 转换函数
操作符重载的语法基础上，把返回值省略掉，函数名以类型名，不允许有参数。 这种形式定义一个转换函数。 一般情况下转换函数是const的
```c++
class Fraction{
public:
    Fraction(int num, int den=1):m_num(num), m_den(den){};
    operator double() const{
        double n = (double)m_num / m_den;
        return n;
    }
private:
    int m_num;
    int m_den;
};
Fraction f(3,5);
double m = 54.0 + f ;
cout << m << endl; //54.6
```

## 11. Non-explicit-one-argument ctor
三个部分： 
1. Non-explicit 非强制指定，即显式
2. one-argument 表示有一个实参，这里带默认值的参数可以不算进来
3. ctor 构造函数

如下代码实现Non-explicit-one-argument ctor
```c++
class Fraction2{
public:
    Fraction2(double num, int den=1):m_num(num), m_den(den){
        cout << "Fraction2 construct:" << num << endl;
    };
    operator double() const{
        cout << "Fraction2 conversition double:" << m_num << endl;
        double n = (double)m_num / m_den;
        return n;
    }
    Fraction2& operator+(const Fraction2& other){//const带上下面使用会报错，不带则不会
        cout << "Fraction2 add:" << m_num << ", " << other.m_num<< endl;
        this->m_num += other.m_num;
        this->m_den += other.m_den;
        return *this;
    }
    int getNum()const {return m_num;}
    int getDen()const {return m_den;}
private:
    int m_num;
    int m_den;
};
inline
ostream & operator<< (ostream& os, const Fraction2 & frac){
    return os << '(' << frac.getNum() << ',' << frac.getDen() <<')' << std::endl;
}

Fraction2 f2(3,5);
Fraction2 fr2 = f2 + 54;
cout << fr2 << endl;
//输出
Fraction2 construct:3
Fraction2 conversition double:3
Fraction2 construct:54.6
(54,1)
```
> 这个例子里，课程侯老师说会出现两条路，导致Error【ambiguous】冲突，一条是fr2 由两个Fraction2对象转换而来，一条是fr2则double的数直接调用conversion再构造而来。 如果+操作符不加const，则编译器会使用conversion转换，即使用第二条路，如果带了const,则可以选择两条路，则会出现ambiguous冲突。 说白了就是没有const，编译器就知道了怎么选择了，不纠结了，所以运算符重载还是加个const

如下代码实现 explicit-one_argument ctor
```c++
class Fraction3{
public:
    explicit Fraction3(int num, int den=1):m_num(num), m_den(den){};
    operator double() const{
        double n = (double)m_num / m_den;
        return n;
    }
    Fraction3& operator+(Fraction3& other){
        this->m_num += other.m_num;
        this->m_den += other.m_den;
        return *this;
    }
private:
    int m_num;
    int m_den;
};
//这样调用编译器会报错，提示无法把54隐式转换成Fraction
//    Fraction3 f3(3,5);
//    Fraction3 fr3 = 54 + f3 ;
//    cout << fr3 << endl;
```

## 12. pointer-like classes
智能指针
实例如下：注意实参要传引用，否则将是个拷贝地址，导致输出错误
```c++
template <class T>
class SmartPtr{
private:
    T * t;
public:
    SmartPtr(T *target):t(target){
    }
    SmartPtr(T& target):t(&target){
    }
    T& operator*(){
        return *t;
    }

    T* operator->(){
        return t;
    }
};
Fraction2 fTest(30,5);
SmartPtr<Fraction2> sptr(fTest);
cout << sptr->getNum() << endl;
//输出
Fraction2 construct:30
30
```
应用在迭代器中：
```c++
reference operator*() const{return (*node).data;}
pointer operator->() const {return &(operator*());}
```
对于ite->method()这样的调用， 想当于：

```c++
Foo::method();
(*ite).method();
(&(*ite))->method();
```

![image-20230208161927997](/img/image-20230208161927997.png)


## 13. function-like classes
把类或struct做为一个函数来调用，注意调用时需要两个括号，第一个用于生成临时对象实例第二个调用操作运算符
如下实例中，通过一个父类继承为子类的类型生成别名，此父类的大小为0（实际输出为1）。
```c++
template<class Arg, class Result>
struct MyUnaryFunc{
    typedef Arg first_type;
    typedef Result second_type;
};

template<class T1, class T2>
        struct MyPair: public MyUnaryFunc<T1, T2>{
    T1 first;
    T2 second;
    MyPair(): first(T1()), second(T2()){};
    MyPair(const T1& a, const T2& b): first(a), second(b){};
};

template<class T>
        struct identity: public MyUnaryFunc<T, T>{
    const T&
    operator()(const T& t){return t;}
};

template<class P>
        struct select1st: public MyUnaryFunc<P, typename P::first_type>{
    const typename P::first_type&
    operator()(const P& t){return t.first;}
};

template<class P>
        struct select2nd: public MyUnaryFunc<P, typename P::second_type>{
    const typename P::second_type&
    operator()(const P& t){return t.second;}
};
MyPair<int,int> p(1,2);
typename MyPair<int, int>::first_type select_pair1 = select1st<MyPair<int, int>>()(p);
cout << select_pair1 << endl;
//输出 1
```
## 14. namespaces
习惯上建议在开始写C++文件时，都加上namespaces。方便日后扩展时不会千万类名冲突，如上例中的pair就容易与标准库中重名冲突。

## 15. 类模板与函数模板
类模板使用如2.13的complex的写法，而函数模板，则如13。注意只有在模板内的typename和class是共通的，由于历史原因，class更早期就有，后面就有了typename。
使用模板的默认参数，类似于函数默认值的方式，为缺少参数自动添加缺省值！

## 16. 成员模板
在类的成员中，也有需要定义模板的地方，标准库中多数用在构造函数上。
```c++
template<class T1, class T2>
        struct MyPair: public MyUnaryFunc<T1, T2>{
    T1 first;
    T2 second;
    MyPair(): first(T1()), second(T2()){};
    MyPair(const T1& a, const T2& b): first(a), second(b){};
    template<class U1, class U2>
    MyPair(const MyPair<U1, U2> &p):first(p.first), second(p.second){};
};

MyPair<SubClass, SubClass> classPair1;
MyPair<BaseClass, BaseClass> classPair2;

MyPair<BaseClass, BaseClass> TestPair1(classPair1);
MyPair<SubClass, SubClass> TestPair2(classPair2);//报错，无法从把父类转子类
```

## 17. 特化与偏特化
可以理解为与模板的泛化相反，指定类型，偏特化则是对部分参数进行特化
```c++
template<>
struct MyPair<int, std::string>: public MyUnaryFunc<int, std::string>{
    int first;
    std::string second;
    MyPair(): first(0), second("d"){
        std::cout << "dsa" << std::endl;
    }
    MyPair(const int& a, const std::string& b): first(a), second(b){
        std::cout << "aaa" << std::endl;
    }
    template<class U1, class U2>
            MyPair(const MyPair<U1, U2> &p):first(p.first), second(p.second){};
};

//偏特化
template<typename T>
struct MyPair<std::string , T>: public MyUnaryFunc<int, T>{
    int first;
    std::string second;
    MyPair(): first(0), second(T()){
        std::cout << "KKK" << std::endl;
    }
    MyPair(const int& a, const T& b): first(a), second(b){
        std::cout << "KKKK" << std::endl;
    }
    template<class U1, class U2>
            MyPair(const MyPair<U1, U2> &p):first(p.first), second(p.second){};
};
```
## 18.template template parameter
对于模板中再放入模板的情况。 
```c++
template<typename T, template<typename T> class Container>
class XCls{
public:
    Container<T> c;
    XCls(){
        std::cout << "ttp: container"<< std::endl;
    }
};

template<typename T, template<class T> class SmartPtr>
class XCls2{
public:
    SmartPtr<T> c;
    XCls2():c(new T){
        std::cout << "ttp: ptr"<< std::endl;
    }
};

template<typename T, class Squence=std::deque<T>>
class XCls3{
public:
    Squence c;
    XCls3(){
        std::cout << "this is not ttp"<< std::endl;
    }
};
XCls<int, Lst> xcl_obj;
XCls2<int, shared_ptr> xcl2_sp;
//    XCls2<int, unique_ptr> xcl2_up;//报错 由于unique_ptr有多个template，需要强制指明
//    XCls2<string, weak_ptr> xcl2_wp; //报错 由于weak_ptr未实现构造
XCls2<int, auto_ptr> xcl2_ap;
XCls3<int, list<int>> xcl3_obj;
```
> 对于模板的默认值的情况，这种不属于模板模板参数，因为还是必须指明模板参数。如上例XCls3
> 这里注意选中MSVC的编译器，使用CLANG会阻止定义模板模板参数，只能改为如下的方式：但无法按原样使用
> [关于clang的提示错误](https://stackoverflow.com/questions/20875033/clang-vs-vcerror-declaration-of-t-shadows-template-parameter)
```c++
template<typename T> class Container;
template<typename T, Container<T>>
class XCls{
...
};
```

## 19.关于__cplusplus
返回当前C++标准的值，msvc环境下需要添加编译选项，否则永远输出199711。

[MSVC官方解释](https://learn.microsoft.com/en-us/cpp/build/reference/zc-cplusplus?view=msvc-170)

```c++
if (MSVC)
    add_compile_options(/Zc:__cplusplus)
endif()
```

## 20.三个c++11的主题
### 20.1 可变参数模板
语法上支持...，可以直接解包
```c++
//写法一
void print(){

}

template<typename T, typename... Args>
void
print(const T& t, const Args&... args){
    cout << t << endl; //cout << sizeof...(args) << t << endl;
    print(args...);
}
//print(5, bitset<15>(370), "abc");

//写法2
template<typename T>
using Lst = list<T, allocator<T>>;

template<typename T>
ostream &
print(ostream& os, const T& t){
    os << t << endl;
    return os;
}

template<typename T, typename... Args>
ostream &
print(ostream& os, const T& t, const Args&... args){
    os << t << endl;
    return print(os, args...);
}
//print(cout, 5, bitset<15>(370), "abc");
```
### 20.2 auto
类似于c#的var，可以自动获取类型，常用于迭代器

### 20.3 range base iterator
使用冒号解开容器，可以使用引用符来接收参数，这样就可以实现改值操作。
```c++
list<int> m = {1,32,4,5,4,6};
for(auto& i : m){
cout << i++ << endl;
}
for(auto i : m){
cout << i << endl;
}
```


