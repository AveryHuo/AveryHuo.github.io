---
title: C++ 复习3
cover: false
date: 2023-02-25 15:09:05
updated: 2023-03-06 18:28:34
top_img: false
categories:
- CPlusPlus
tags: 
- C++
---

# 函数模板的隐式或显式转换
对于类型不明确的情况，需要使用显式转换告诉编译器类型，隐式转换存在于编译器明确知道是什么类型的情况 。
```c++
template <typename T>
const T& max(const T& a, const T& b){
	return a > b?a:b;
}

void Test1(){
    cout << max(1,2);//隐式
    cout << max<double>(1,19.2);//显式
}
```
> 无法为函数模板指定缺省的模板实参，但类模板可以

模板参数： 这里的typename T就是模板参数，而a，b则是调用参数。通过隐式转换，可以得到一些更简化的用法：
```c++
 template <typename RT, typename T1, typename T2>
 RT max(const T1& a, const T2& b){
	cout << "run two" ;
	return (RT)a > b?a:b;
 }
 cout << max<double>(1,2.5); //为RT设置类型double,另外的两个通过隐式转换得到
```
# 对于const的顶层底层再理解
区分const修饰时，以指针符星号为界，往左侧进行修饰。const修饰类型时，则为底层const，表示指针指向一个常量类型对象，如果是顶层const，表示修饰的是指针为常量，一般在指针的右侧。
例如： const char*与char const* 是一样的，这里的const都是修饰类型，而char * const则是顶层const，表示修饰的是指针为常量指针。

# 重载函数模板
* 对于参数类型不同，参数的个数不同的情况都可以算重载。 
* 在调用时，如果出现非模板与模板函数都能匹配的情况，隐式情况下默认选择非模板，但可以使用空的<>来强制要求使用模板。
* 对于传值或传引用的调用要区分，否则会出现意外的错误，如下：
```c++
const char* max(const char * a, const char* b){
    cout << "run max char const*" <<endl;
    return strcmp(a,b) < 0 ? b: a;
}

template <typename T>
const T& max(const T& a, const T& b, const T&c){
    cout << "run max three"  <<endl;
    return max(max(a,b), c);// 报错，Returning reference to local temporary object 。 原因在于会调用上述的模板函数生成一个值类型的指针指向const char类型，这个传回来一个无效的引用，无法使用。
}
```

* 一定要让函数重载的版本声明位于被调用之前，否则会出现找不到的错误。同理类的模板定义也一样，比如在main.cpp中的调用，需要类定义之后。

# 指向指针的引用
通过*&实现指向指针的引用，符号是往左修饰的，必须让引用在指针右侧
```c++
  void ptrswap2(int *&v1,int *&v2)//指向指针的引用是某一指针的别名，同变量的引用一样，可以实现对传递给形参的实参数值的交换
    {
        int *temp=v2;//指针别名，当然以指针的形式来应用
        v2=v1;
        v1=temp;
    }

    void ptrswap1(int *v1,int *v2)//利用指针进行数值交换，改变的只是形参的指向，实参的值保持不变；
    {
        int *temp=v2;
        v2=v1;
        v1=temp;
    }
```
# 类模板或函数模板使用普通值
可以为一个类模板定义普通值，也可以指定默认值
```c++
template <typename T, int MAXSIZE, bool isNormal=true>
class Stack{
...
}

template<typename T, int VAL>
T addValue(const T&t){
	return t + VAL;
}
```
但注意不同的普通值生成的模板对象类型不相同！

限制: 不可以为double或内部链接对象
```c++
template <char const * name>
class MyClass{
...
}
extern char const a[] = "hello";
char const * b = "hello2";
MyClass<b>;//错误，指向内部
MyClass<"Test">; //错误，字符串文字不被允许
MyClass<a>;//正确
```

# 关于DLL的知识
DLL是Dynamic Link Library的缩写，意为动态链接库。在Windows中，许多应用程序并不是一个完整的可执行文件，它们被分割成一些相对独立的动态链接库，即DLL文件，放置于系统中。当我们执行某一个程序时，相应的DLL文件就会被调用。一个应用程序可有多个DLL文件，一个DLL文件也可能被几个应用程序所共用，这样的DLL文件被称为共享DLL文件。

如何链接：
1. 隐式链接（Load-Time Dynamic Linking）： 大部分系统的DLL通过这种方式， 是指在应用程序中不指明DLL文件的实际存储路径。建立 DLL时链接程序会自动生成一个与之对应的LIB导入文件。 这个文件中包含着一些类似于头文件的定义，这个文件是会被exe开始就加载进去的。  待需要加载真正的DLL时，windows根据其中的信息进行加载。
2. 显式链接（Run-time Dynamic Linking）： 直接使用Win32提供的LoadLibrary()函数去装载，指定DLL的路径为参数，加载成功后，使用GetProcAddress()去获取DLL的函数地址。当然如果不指定路径，就会变为隐式链接的方式了。

DLL中包含了一个导出函数表。这些导出函数由它们的符号名和称为标识号的整数与外界联系起来。函数表中还包含了DLL中函数的地址。当应用程序加载DLL模块时时，它并不知道调用函数的实际地址，但它知道函数的符号名和标识号。

好处：
1. 逻辑更加分离，当程序需要调用函数时需要先载入DLL，然后取得函数的地址，最后进行调用。使用DLL文件的好处是程序不需要在运行之初加载所有代码，只有在程序需要某个函数的时候才从DLL中取出。
2. 节省内存。子程序被分出到各个dll按需加载，这样程序运行时的占用自然就会小，而不必完全装载到主程序里。
3. 程序之间的合作更加方便，同时也能降低各模块的耦合度，各自完成自己所属的dll即可。

# 模板参数的使用
可以使用{}括号代替普通括号使用构造函数变量初始化，同时也可以为其指定默认值。
```c++
template <typename T>
class Test10Class{
public:
    T t{}; // 1. 使用默认初始化
    //        Test10Class() = default;
    //        Test10Class(T t=T()):t() { // 2. C++11之前的写法，为模板默认参数化
    //            cout << "Construct Test10 class " << endl;
    //        }
    Test10Class(T ct=T()):t{ct} { // 2. 为模板默认参数化 3. 参数默认值的写法
    	cout << "Construct Test10 class " << endl;
    }
};

void Test10(){
	Test10Class<int> myObj{25};
	cout << "my val is:" << myObj.t << endl;
}
```

# 成员模板
在函数内对成员函数定义单独的模板，注意不支持偏特化，必须全特化
```c++
class BoolString{
public:
    template<typename T = std::string>
        T get() const { // get value (converted to T)
        return value;
    }
    
     template<>
     bool get<bool>() const { 
        return value;
    }
}
```

# .template
在调用模板参数时，需要与小于号进行区别，这时可以使用.template
```c++
template<unsigned long N>
    void printBitset (std::bitset<N> const& bs) {
        std::cout << bs.template to_string<char, std::char_traits<char>,std::allocator<char>>() << endl;
    }

    void Test10(){
        Test10Class<int> myObj{25};
        cout << "my val is:" << myObj.t << endl;
        unsigned long a = 12;
        std::bitset<12> m = {};
        printBitset(m);
    }
```

# 字符串作为模板参数
当使用字符串直接做为模板参数时，会转为数组，这时就要求数组长度一致才可以。当然如果用指针就可以解决：
```c++
template<typename T>
const T & max2(const T& t1, const T& t2){
    return t1 > t2? t1: t2;
}
const char* max(const char * a, const char* b){
	cout << "run max char const*" <<endl;
    return strcmp(a,b) < 0 ? b: a;
}

string s;
cout << "max2:" << max2("abc", "bcd") << endl;
cout << "max:" << max("abc", "bcdm") << endl;//用不了max2，会提示数组长度不同
cout << "max2:" << max2("abcd", "bcdm") << endl;
```

# 变量模板[C++14]
允许为变量创建模板
1. 不能出现在函数或块作用域内

```c++
template<typename T>
constexpr T pi{3.14145454};

cout << "PI: "<< pi<double> << endl;
```

2. 也可以有默认参数，但必须带有<>符号
```c++
template<typename T = long double>
constexpr T pi{3.14145454};

cout << "PI: "<< pi<> << endl;
```
3. 可以接收非类型参数
```c++
template<int N>
std::array<int,N> arr{};

//double只在C++20后支持
//    template<double n> 
//    constexpr double pi2{n};

template<auto N>
constexpr decltype(N) dval = N;

cout << dval<'c'> << endl;
```
4. 可以使用在表示某个类的数据成员，当然以下的情况是类的成员是静态的。
```c++
template<typename T>
int myMax = MyClass<T>::max;

auto i = myMax<std::string>;
```
> C++17之后加的一种_v的特征后缀为所有产生bool值的标准库值支持快捷方式
```c++
std::is_const_v<T>  // std::is_const<T>::value
```

# 适配移动语义
对于一般的模板函数参数，T& 这种只能处理左值的情况，而对于移动语义的参数，就需要使用C++11提供的转发参数，std::forward
```c++
class X{}
void g(X x){}
void g(X& x){}
void g(X&& x){}
//以下就能完美转发所有的g函数了
template <template T>
void f(T&& t){
	g(std::forward<T>(t));
}

X v; // create variable
X const c; // create constant

f(v); // f() for variable calls f(X&) => calls g(X&)
f(c); // f() for constant calls f(X const&) => calls g(X const&)
f(X()); // f() for temporary calls f(X&&) => calls g(X&&)
f(std::move(v)); // f() for move-enabled variable calls f(X&&) => calls g(X&&)
```

* 2. 适配构造函数时会出现混乱，因为成员模板的匹配优先级更高。
```c++
#include <utility>
#include <string>
#include <iostream>

class Person
{
private:
std::string name;
public:
// generic constructor for passed initial name:
template<typename STR>
explicit Person(STR&& n) : name(std::forward<STR>(n)) {
std::cout << "TMPL-CONSTR for '" << name << "'\n";
 }
// copy and move constructor:
Person (Person const& p) : name(p.name) {
std::cout << "COPY-CONSTR Person '" << name << "'\n";
}
Person (Person&& p) : name(std::move(p.name)) {
std::cout << "MOVE-CONSTR Person '" << name << "'\n";
}
};

std::string s = "sname";
Person p1(s); // init with string object => calls TMPL-CONSTR
Person p2("tmp"); // init with string literal => calls TMPL-CONSTR
Person p3(p1); // ERROR
Person p4(std::move(p1));
Person const p2c("ctmp")
Person p3c(p2c);
```

# std::enable_if
C++11后提供了一种（删除代码）禁用模板的方法，可以在尖括号中用括号写入表达式，以结果为决定是否能用这个模板， C++ 14后添加一个enable_if_t的方法支持成功后返回第二个参数
```c++
template <typename T>
typename std::enable_if_t<(sizeof(T) > 4), T> foo(T t){
    cout << "Foo" << endl;
    return t;
};
cout << foo<double>(23.6) << endl;
//Foo
//23.6
```
1. 使用在类中适配移动语义
```c++
template<typename T>
using EnableIfString = std::enable_if_t<
std::is_convertible_v<T,std::string>>; //c++14 , c++11需要的补上::type;


// generic constructor for passed initial name:
template<typename STR, typename = EnableIfString<STR>>
explicit Person(STR&& n)
: name(std::forward<STR>(n)) {
std::cout << "TMPL-CONSTR for ’" << name << "’\n";
}

std::string s = "sname";
Person p1(s); // init with string object => calls TMPL-CONSTR
Person p3(p1); // OK => calls COPY-CONSTR
```

2. 限制构造函数， 由于在定义成员函数模板时，会与默认的构造函数发生冲突，这时编译器会优先调用默认的构造函数，为了防止调用默认的构造函数，使用const volatile 获取到后用delete删除掉默认的
```c++
   template<typename T>
    class C
    {
    public:
        C() = default;
        // user-define the predefined copy constructor as deleted
        // (with conversion to volatile to enable better matches)
        C(C const volatile&) = delete;
        // if T is no integral type, provide copy constructor template with better match
        template<typename U,
                typename = std::enable_if_t<!std::is_integral<U>::value>>
                        C (C<U> const&) {
                            cout << "Good" << endl;
                        }
    };

C<int> c;
C<int> c2{c};//编译不通过！必须非Int类型，但不加这句 C(C const volatile&) = delete; ，编译成功，
```

3. 使用C++20的 concepts
```c++
    template<typename U>
    concept NotIntergerType = !std::is_integral<U>::value;
    class C{
    ...
      template<typename U>
   requires NotIntergerType<U>
   C (C<U> const&) {
   cout << "Good" << endl;
   }
    
    }
    
    C<int> c; 
    C<int> c2{c}; //使用concepts语法将直接提示错误。
 
```