---
title: C++ 复习3
cover: false
date: 2023-02-20 10:03:22
updated: 2023-02-24 10:03:22
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