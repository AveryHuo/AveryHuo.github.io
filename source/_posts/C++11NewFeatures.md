---
title: C++ 11新特性
cover: false
date: 2023-02-20 10:03:22
updated: 2023-02-25 15:07:26
top_img: false
categories:
- CPlusPlus
tags: 
- C++
---

# 1. 支持Long long类型
一般来说编译器支持int 为4个字节，double占用8个字节（2个字）， 在C++11中加入了更高精度的long long类型，long double类型，以3、4个字表示（16个字节）

# 2. 列表初始化或赋值
说是列表初始化，其实本质上就是一种由花括号（类似于列表）的方式来初始变量。
```c++
int test_a = {1};
test_a = {2}; //赋值
int test_b{2};
vector<int> test_c = {1,3,4} //同样适用于vector
//int test_d = {1.2} //错误，类型转换无法发生在列表初始化
//test_d = {1.3} //错误，类型转换无法发生在列表赋值
map<string, string> authors = {{"1", "a"},{"2", "b"},{"3", "c"}};//关联容器的列表初始化
pair<string, string> author = {"1", "a"};
```
但是这种也有限制，不可以将高精度用于低精度初始化，如下初始化会失败，由于编译对于数值的保护：
```c++
long double ld = 3.1415926536;
int a{ld}, b = {ld}; //错误
int a(ld), b = ld; //正确，但会丢失精度
vector<int> *test_d = new vector<int>{1,2,3,4,5};
```

# 3. nullptr常量
C++11之前，常在需要设置为空指针时用如下两种写法：
```c++
int *p = 0;
int *p = NULL; //NULL 实质上是一个预处理变量，表示0
```
C++11提出nullptr常量，并且推荐开发者都使用这种方式设置空指针。
> 这样设计也有原因，比如0常常与数值0混淆，而且对于为0的数值变量是无法与指针赋值的，当然这也很奇怪。

# 4.constexpr 
1. 变量
对于一些复杂系统，不易分辨是不是常量表达式，也的确可以在变量定义时做：
```c++
const int THREADHOLD = 3;
const int THREADHOLD_ADD_ONE = THREADHOLD + 1;
```
C++11中加入constexpr 支持常量表达式：
```c++
constexpr int THREADHOLD = 3;
constexpr int THREADHOLD_ADD_ONE = THREADHOLD + 1;
```
特别的constexpr不可以为让一个非constexpr的函数赋值！ 除非也定义那个函数为constexpr
2. 函数
对于constexpr函数与普通函数类似，但是其要求返回类型必须是算术类型，指针，引用这三种，且不能有多个return语句。 在运行时将被替换成结果，同时也将隐式的使用inline:
```c++
constexpr int new_sz(){return 42;}
```

# 5.类型别名声明
一般方法是使用typedef的方式：
```c++
typedef double MyDouble;
```
现在支持一种using语法，接=后为所想指的原类型：
```c++
using MyDouble = double;
```

# 6. auto类型指示符
可以为一些难以确定的类型使用auto来替代类型名，常用于迭代器的类型，也可以为一些确定的表达式类型声明使用auto.
```c++
int a, b =5
auto c = a + b;//c将自动为int类型
int ia[3][4];
int (*ip)[4] = ia; //ip为指向带四个元素的数组
//int *ip[4]; // 这个表示一个数组带四个指针
for(auto p = ia; p != ia + 3; ++p){
	for(auto q = *p; q != *p + 4; ++q)
		cout << *q << ' ';
	cout << endl;
}
auto p = new auto(a); // p为 int *， 注意不可使用在列表初始化上。

```

# 7.decltype类型指示符
可以取一个表达式或者变量名的类型
```c++
const int i, &j = i;
decltype(i) a = 5; //与int a = 5等价
decltype(j) b = a;//与int &b = a等价
```
注意的两点：
1. decltype其中再加多一层括号时，必须返回的是左值，即引用的结果：
```c++
int i = 5;
decltype((i)) a = i; //与int &a = i;等价
```
2. 当decltype应用于解引用指针时，返回的是一个左值引用的结果，与例1类似，所以必须得初始化

# 8. 类内初始化
可以为类的成员直接写上初始值。简化了构造函数的工作
```c++
class A
{
 
public:
.....
 
  int a = 1;
  int b{ 2 };
};

//旧的指定初始值需要这样写
A(int i, int j) :a(1),b(2) {};
//现在在类已有初始化值时，可以用简化的写法就行
A(int i, int j){};
```
# 9. range base iterator
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
# 10.vector对象的vector
旧的标准中 右尖括号必须隔开以防与>>右移运算符冲突
```c++
vector<vector<int> >
```
C++11后，可以不用这个空格限制。

# 11.容器的cbegin和cend函数
为了能得到一个const修饰的迭代器某项的值，使用cbegin和cend替代begin和end
```c++
vector<int> v;
const vector<int> cv;
auto it1 = v.begin();//auto代表提vector<int>::iterator
auto it2 = cv.begin();//auto代表提vector<int>::const_iterator
auto it3 = v.cbegin(); //auto代表提vector<int>::const_iterator
```

# 12. begin与end函数
直接取得一个数组的头和尾：
```c++
int test_arry[] = {1,2,3,90, 5,6};
int *test_arry_begin_ptr = begin(test_arry);
int *test_arry_end_ptr = end(test_arry);
while((test_arry_begin_ptr != test_arry_end_ptr) && (*test_arry_begin_ptr < 6)){
	test_arry_begin_ptr ++;
}
cout << "Find weird num:" << *test_arry_begin_ptr <<endl;

//对应11点的容器来说可以这样写：
vector<int>::const_iterator test_arry_begin_ptr = begin(test_v_a);
auto test_arry_end_ptr = end(test_v_a); //这里的auto是vector<int>::iterator
```

# 13.除法的舍入规则
1. C++11所有的商都一律向0取整
2. 除法运算，直接切除小数部分，而是由具体情况而定，(-m)/n 等于 m/(-n) 等于 -(m/n) 
3. 取余运算来说，只匹配m的符号，分子n的值一律按正的值处理： m % (-n) 等于m%n , (-m) % n 等于 -(m % n), -m % -n 等于-(m % n)
```c++
21 / 8  2  
-21 % 8  -5  ==> -(21 % 8)
21 % -8  5  ==> 21 % 8
-21 % -8  -5 ==> -(21 % 8)
```

# 14.sizeof用在类成员
sizeof输出常量表达式，所以可以自然放到右值使用。
sizeof有两种用法：传入typename或object
```c++
class TestClass{
public:
	int m;
}
TestClass tc;
sizeof(TestClass) //取这个类型的所占空间
sizeof  tc;//放表达式后面，取其所占空间大小，与上面一样效果
```
> 但对vector或string使用时，只返回该类型固定部分大小，即与括号返回的结果一样，而非包含元素大小。

# 15.标准库initializer_list类
与vector用法类似，本质的实现上也采用模板参数的方法，这样适配了各种类型。
几个规则：
1. 初始化时，采用复制的方式把初始值拷贝出来
2. 拷贝或赋值运算时，取的引用，与副本共享元素
3. 同样内置了迭代器
```c++
 int il_i1 = 1;
 int il_i2 = 2;
 int il_i3 = 3;
 initializer_list<int> il_a {il_i1, il_i2, il_i3};
 initializer_list<int> il_b (il_a);
 for(auto il_iter = il_a.begin(); il_iter != il_a.end(); ++il_iter){
 cout << *il_iter << endl;
 }
```

# 16.列表初始化返回
与列表初始化相对应的，用花括号放数同类型数据可以初始化一个对象或者列表，也可以当作函数返回值使用!
```c++
int Test4(){
	return {1};
}
vector<int> Test5(){
	return {1,3,4,2};
}
```

# 17.尾置返回类型
返回类型写成auto，使用箭头符告诉具体的返回类型：
```c++
auto Test5() -> vector<int>{
	return {1,3,4,2};
}
```

# 18.=default生成默认构造函数
在C++11中加入=default可以在函数内部使用Inline的方式，外部非inline方式指定此构造函数使用默认的构造。
```c++
struct Sales_data{
	Sales_data() = default;
}
```

# 19. 委托构造函数

定义一个构造函数，其他构造函数可以委托其执行一些逻辑，注意这个执行是优先的，然后才自己的构造函数体内的部分
```c++
class Sales_data{
private:
    string booksNo;
    unsigned units_sold;
    double revenue;
public:
	Sales_data(string s, unsigned cnt, double price):booksNo(s), 	units_sold(cnt), revenue(price){//1
		cout << "RUN: Sales_data(string s, unsigned cnt, double 	price):booksNo(s), units_sold(cnt), revenue(price)" << endl;
	}
	Sales_data(): Sales_data("xxx", 1, 0.1){//2
		cout << "RUN: Sales_data(): Sales_data(\"xxx\", 1, 0.1)" << endl;
	}
    Sales_data(string s): Sales_data(s, 1, 0.1){//3
    	cout << "RUN: Sales_data(string s): Sales_data(s, 1, 0.1)" << endl;
	}
};

void Test6(){
Sales_data sd1;// 执行1，再执行2
Sales_data sd2("book1"); //执行1，再执行3
Sales_data sd3("book1", 1,3);//只执行1
}
```

# 20.constexpr的构造函数
为构造函数添加constexpr关键字，可以让其生成constexpr的对象，可以定义为default，也可以在满足构造函数和constexpr的前提下定义如下规则的函数：
*  必须初始化所有的数据成员，使用初始值的方式或者constexpr构造或constexpr表达式
```c++
class Debug{
private:
	bool hw;
	bool io;
	bool other;
public:
	constexpr Debug(bool b= true):hw(true), io(b), other(false){}
	constexpr Debug(bool h, bool i, bool o):hw(h), io(i), other(o){}
}
```

# 21.string对象处理文件名
文件流对象在旧的标准中，必须使用C风格字符串，现在也能支持直接传string了：
```c++
std::string ifile = "test.txt";
ifstream in(ifile);
```

# 22. array和forward_list容器
foward_list是单向链表的容器，插入删除性能很快，但不支持size函数。array是固定数组大小的容器，快速随机访问，但不能增删元素。
例：
```c++
//创建部分元素有值，其他为0的array对象
std::array<double, 10> values {0.5,1.0,1.5,,2.0};

//拷贝普通数组，创建forward_list容器
int a[] = { 1,2,3,4,5 };
std::forward_list<int> values(a, a+5);
//拷贝其它类型的容器，创建forward_list容器
std::array<int, 5>arr{ 11,12,13,14,15 };
std::forward_list<int>values(arr.begin()+2, arr.end());//拷贝arr容器中的{13,14,15}

#include <iostream>
#include <forward_list>
using namespace std;
int main()
{
    std::forward_list<int> values{1,2,3};
    values.emplace_front(4);//{4,1,2,3}
    values.emplace_after(values.before_begin(), 5); //{5,4,1,2,3}
    values.reverse();//{3,2,1,4,5}
    for (auto it = values.begin(); it != values.end(); ++it) {
        cout << *it << " ";
    }
    return 0;
}
```
# 23. swap函数
swap对元素不进行拷贝，删除，插入操作，因此只有常数时间的算法复杂度。
旧的标准使用的拷贝构造函数：
```c++
namespace std {
    template<typename T>
    void swap(T &a,T &b) {
        T temp(a);
        a = b;
        b = temp;
    }
}
```
c++11后有了移动构造函数和移动运算符，优化后的版本，同时支持为非成员函数：
```c++
template<typename T>
void swap(T& a,T&b) {
    T temp(std::move(a));
    a = std::move(b);
    b = std::move(temp);
}
```



# 24. 容器insert成员的返回类型
C++11中容器insert将返回第一个新加入元素的迭代器
```c++
list<string> lst;
auto iter = lst.begin();
while(cin >> word)
	iter = lst.insert(iter, word);
```

# 25. emplace, emplace_front, emplace_back
新增的三个成员。 emplace对应insert，emplace_front对应push_front, emplace_back对应push_back
区别就是emplace可以直接给参数并且调用构造生成对象，而insert必须传对象才行。
```c++
c.emplace_back("a", 1, 2);//这里的c是一个指定对象X的容器
c.push_back(X("a", 1, 2)); //与上行等价
```

# 26. 容器shrink_to_fit()
对于容器vector, string, deque。由于是会根据大小进行动态分配大小，当分配大小不足时，会再次分配一块内存，使用shrink_to_fit()可以让多分配出的内存退回。 
> 但不能保证都能正常退回？有些环境下shrink_to_fit()可能无效？
```c++
 vector<int> ivec;
 cout << ivec.size() << "," << ivec.capacity() << endl; //0,0
 for(size_t ix = 0; ix < 24; ix ++)
	 ivec.push_back(1);
 cout << ivec.size() << "," << ivec.capacity() << endl; //24,32
 ivec.shrink_to_fit(); 
 cout << ivec.size() << "," << ivec.capacity() << endl;// 24,24
 ivec.reserve(60);
 cout << ivec.size() << "," << ivec.capacity() << endl;// 24,60
 for(size_t ix = 0; ix < 50; ix ++)
 ivec.push_back(1);
 cout << ivec.size() << "," << ivec.capacity() << endl; //74, 120
 ivec.shrink_to_fit();
 cout << ivec.size() << "," << ivec.capacity() << endl; //74,74
```

# 27. string与数值相互转换
新加入数值与string相互转换的方法
```c++
int pi = 42;
string str1 = to_string(pi);
string str = "3.24";
double dv = stod(str);
cout << pi << dv << endl;
```

# 28. lambda表达式
使用如下格式可以定义一个lambda表达式，本质上是一个inline的未命名函数，表示一块可以执行的代码块。
[capture list] (params list) mutable exception-> return type { function body }
* capture list: 表示捕获在此lambda之前声明的变量，用,隔开，可以使用= 表示对值进行捕获，用&表示对引用进行捕获。
* mutable： 表示用来说用是否可以修改捕获的变量， 只对值数据有效，类似于对值变量前加一个引用符
* -> : 使用尾置返回类型，指明此Lambda的返回类型

```c++
int sz = 3;
ostream &os = cout;
vector<string> str_list = {"c", "abc", "abcdefg","eedfg"};
auto iter = find_if(str_list.begin(), str_list.end(), [&, sz](string &s){ os << s << endl; return s.size() >= sz;});// find_if 找出第一个匹配的迭代器
cout << *iter << endl;
```

# 29. 标准库 bind
给定函数，除了使用直接调用的方式，也可以使用bind得到一个函数绑定器，用这个绑定器来调用。
1. 有这个绑定器，结合标准库placeholders空间提供的占位符，以重新更改需要传入的参数顺序。
2. 对于传递的变量是引用类型，，要使用ref()函数包裹一下，如果是const 引用，则用cref()函数包裹。注意这只是在传递变量的情况，如果使用Placeholders，则不需要加这个函数包裹
```c++
 ostream &os = cout;
 int sz = 3;
 auto compare_func = [sz](ostream &os, string &s, int hack, bool is_bigger){
 	 os << s << ", with " << hack << endl;
     if(is_bigger)
        return s.size() >= sz;
     else
        return s.size() < sz;
 };
 auto compare_big_func = std::bind(compare_func, ref(os), placeholders::_1, 0, true);
 auto compare_small_func = std::bind(compare_func, ref(os), placeholders::_1, 0, false);
 vector<string> str_list = {"c", "abc", "abcdefg","eedfg"};
 auto iter = find_if(str_list.begin(), str_list.end(), compare_big_func);
 cout << *iter << endl;
 auto iter2 = find_if(str_list.begin(), str_list.end(), compare_small_func);
 cout << *iter2 << endl;
```

# 30. 无序容器
unordered_map， unordered_set，同时支持重复关键字的版本是 unordered_multimap, unordered_multiset
```c++
//创建一个空的unordered_multiset容器
std::unordered_multiset<std::string> umset;
//给 uset 容器添加数据
umset.emplace("http://c.biancheng.net/java/");
umset.emplace("http://c.biancheng.net/c/");
umset.emplace("http://c.biancheng.net/python/");
umset.emplace("http://c.biancheng.net/c/");
//查看当前 umset 容器存储元素的个数
cout << "umset size = " << umset.size() << endl;
//遍历输出 umset 容器存储的所有元素
for (auto iter = umset.begin(); iter != umset.end(); ++iter) {
cout << *iter << endl;
}
```
# 31. 可变参数模板
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

# 32. 智能指针

1. shared_ptr 
允许多个shared_ptr指向同个对象，当所有的shared_ptr都被销毁时，将调用所反指向的对象析构，进行销毁。 
原则：只要shared_ptr指向指定堆内存的引用计数不为0，则这块内存还存在，还可以被shared_ptr找到。
```c++
std::shared_ptr<int> p3(new int(10));
std::shared_ptr<int> p3 = std::make_shared<int>(10);//等价与上行

//调用拷贝构造函数
std::shared_ptr<int> p4(p3);//或者 std::shared_ptr<int> p4 = p3;
//调用移动构造函数
std::shared_ptr<int> p5(std::move(p4)); //或者 std::shared_ptr<int> p5 = std::move(p4); //这里的p4将变成空的智能指针，p5将指向


//自定义释放规则
void deleteInt(int*p) {
    delete []p;
}
//初始化智能指针，并自定义释放规则
std::shared_ptr<int> p7(new int[10], deleteInt);

//构建智能指针
shared_ptr<int> p1(new int(10));
shared_ptr<int> p2(p1);
shared_ptr<int> p3(p1);

//输出 p2 指向的数据
cout << *p2 << endl;
//修改这块内存的值
*p1 = 25;
//重定向到另一块堆内存
p1.reset(new int(80));
//引用计数减 1,p1为空指针
p1.reset();
if (p1)
cout << "p1 不为空:" << *p1 <<endl;
else
cout << "p1 为空" << endl;

//以上操作，并不会影响 p2
cout << *p2 << endl;
//判断当前和 p2 同指向的智能指针有多少个
cout << p2.use_count() << endl;
```

2. unique_ptr
与shared_ptr相比较，只指向给定的堆内存，且不支持左值拷贝和构造
```c++
unique_ptr<int> P1(new int(5));
cout << *P1 << endl;
//unique_ptr<int> P2(P1); //报错
unique_ptr<int> P2(move(P1));

auto printPtr = [](string name, unique_ptr<int> &p){
	if(p)
		cout << "*" << name << ":" << *p << endl;
	else
		cout << "*" << name << " is NULL" << endl;
};
auto printPtr1 = bind(printPtr, "P1", placeholders::_1);
auto printPtr2 = bind(printPtr, "P2", placeholders::_1);
auto printPtr3 = bind(printPtr, "P3", placeholders::_1);

unique_ptr<int> P1(new int(5));
printPtr1(P1);
//        unique_ptr<int> P2(P1); //报错
unique_ptr<int> P2(move(P1));
printPtr1(P1);
printPtr2(P2);
unique_ptr<int> P3(P2.release());
printPtr1(P1);
printPtr2(P2);
printPtr3(P3);
P1.reset(P3.release());
printPtr1(P1);
printPtr2(P2);
printPtr3(P3);
//以上例子把P1传到P2再传到P3.最后再回P1，这里只改变了指针指向，指向的内存块没有变动。
```
3. weak_ptr
在shared_ptr的基础上，不对引用计数发生变动，因此计数为0的释放时，其他的weak_ptr指针是不被理会的，突出一个“弱”指针。
也因此弱指针不能直接访问，需要调用lock返回shared_int才可以访问：
```c++
if(shared_ptr<int> wp = p2.lock()){
	cout << *wp << endl;
}
```


# 33. 动态分配
1. 可以使用new 在不指定默认值的情况下，申请一块空间：
```c++
int *a = new int;
```
2. 动态数组与普通数组的区别是，动态数组得到的是一指向数组元素类型的指针。由于是指针指向数组元素类型，而不是数组，所以不能使用begin和end。也不能使用auto.
```c++
int *p = new int[42];
int p2[] = {1,2,3};//这得到的是一个数组
int *p2_begin = begin(p2);
int *p2_end = end(p2);
```
3. 使用列表初始化结合动态数组：
```c++
int *pia = new int[10]{0,1,2,3};//由于初始化值不足，剩余值将使用默认值初始化0。
```
4. 动态分配一个空数组是合法的：
```c++
char arr[0];//错误的，数组不能定义为空
char *cp = new char[0];//动态数组可以为空，因为返回的是一个合法的非空指针，但这个指针不为解引用，因为这并不指向任何元素。
```

# 34. allocator
标准库的allocator实际上是每个标准库容器类的模板的第二个默认参数。
每个容器实例中都有一个Allocator实例。它向分配器请求存储来存储元素。

* T*allocate(size_t n);分配足够的存储空间来存储T的n个实例，并返回指向它的指针
* void deallocate(T* p, size_t n) 释放分配的内存
* void construct(T* p, Args ... args);使用p指向的args参数构造一个对象,该接口在C++20中已被移除。本质上就是对传入的类型，原地调用构造和new运算符
* void destroy(T* p);调用p指向的对象的析构函数，该接口在C++20中已被移除。本质上是对对象原地调用析构。

```c++
allocator<string> alloc; // 可以分配string的allocator对象
int n{ 5 };
string * p = alloc.allocate(n); // 分配n个未初始化的string

auto q = p;
alloc.construct(q++, "first");
alloc.construct(q++, 10, 'c');
alloc.construct(q, "hi"); // *q为hi

cout << *p << endl;
cout << *q << endl;
cout << p[0] << endl;
cout << p[1] << endl;
cout << p[2] << endl;

while (q != p) {
alloc.destroy(--q); // 释放我们真正构造的string
}

alloc.deallocate(p, n);
```

# 35. =default/ = delete
= default标识无成员参数的构造函数，意为要求编译器显式生成一个合成的版本。 =delete则用于阻止对象的拷贝构造操作。
```c++
class X
{ 
public: 
    X() = default; //该函数比用户自己定义的默认构造函数获得更高的代码效率
    //X(int, int) = default; // 错误
    X& operator=(const X &) = delete; // 声明拷贝赋值操作符为 deleted 函数
    X(int i)
    { 
        a = i; 
    }

private: 
    int a; 
}; 
```

# 36.右值引用
按照C++的左值长久，右值短暂的特点，右值往往表示的一个值的特征，而左值表示对象的句柄。使用&&符号可以指定一个对象为右值：
```c++
int a = 24;//a是左值
int &&r = a; //错，左值不能往右值赋
int &&r = 43;//正确
int &&r = 43 + a;//正确，右边的结果是一个右值
```
* 区别于左值引用，左值引用只能绑左值
```c++
int a = 20;
int &r = a;//正确
int &r = a+ 32; //错误，右值绑不了左值
```

# 37. std::move
move的作用，就是把一个左值将成右值来用，但这有个后果就是左值被move执行后，将不能再使用了，只能赋值或销毁。
```c++
int &&r = 10;
int &&rr = r;//错误 r是右值引用生成的左值，不能被赋值到右值引用上
int &&rr = std::move(r);//正确，r被转成右值
```

# 38. 移动构造与移动赋值
与拷贝构造的定义类似，区别就是移动构造或赋值并不会对内存进行拷贝，就像是“移动”的文字本意，把原参数对象的指向进行转移，因此做为参数的对象需要使用&&标识，且被置Nullptr时需要安全的。一般也会结合noexcept标识。
```c++
// Move constructor.
MemoryBlock(MemoryBlock&& other) noexcept
   : _data(nullptr)
   , _length(0)
{
   std::cout << "In MemoryBlock(MemoryBlock&&). length = "
             << other._length << ". Moving resource." << std::endl;

   // Copy the data pointer and its length from the
   // source object.
   _data = other._data;
   _length = other._length;

   // Release the data pointer from the source object so that
   // the destructor does not free the memory multiple times.
   other._data = nullptr;
   other._length = 0;
}

// Move assignment operator.
MemoryBlock& operator=(MemoryBlock&& other) noexcept
{
   std::cout << "In operator=(MemoryBlock&&). length = "
             << other._length << "." << std::endl;

   if (this != &other)
   {
      // Free the existing resource.
      delete[] _data;

      // Copy the data pointer and its length from the
      // source object.
      _data = other._data;
      _length = other._length;

      // Release the data pointer from the source object so that
      // the destructor does not free the memory multiple times.
      other._data = nullptr;
      other._length = 0;
   }
   return *this;
}
```
# 39. 移动迭代器
使用标准库的make_move_iterator将普通迭代器转为移动迭代器。这样解引用将生成一个右值引用。
容器在使用make_move_iterator时，std::copy后会将其中的内容清空，变成uninitialize状态，但容器的大小还存在，所以需要调用一下clear来清理掉size不正常的情况。
```c++
std::list<std::string> s{ "one", "two", "three" };

std::vector<std::string> v1(s.begin(), s.end()); // copy

std::vector<std::string> v2(std::make_move_iterator(s.begin()),
std::make_move_iterator(s.end())); // move

std::cout << "v1 now holds: ";
for (auto str : v1)
std::cout << "\"" << str << "\" ";
std::cout << "\nv2 now holds: ";
for (auto str : v2)
std::cout << "\"" << str << "\" ";
std::cout << "\noriginal list now holds: ";
for (auto str : s)
std::cout << "\"" << str << "\" ";
std::cout << '\n';

//结果是s被清空了

vector<unique_ptr<int>> vec;
unique_ptr<int> s1(new int(1));
unique_ptr<int> s2(new int(2));
unique_ptr<int> s3(new int(3));
unique_ptr<int> s4(new int(4));
vec.push_back(std::move(s1));
vec.push_back(std::move(s2));
vec.push_back(std::move(s3));
vec.push_back(std::move(s4));


unique_ptr<int> s5(new int(5));
vector<unique_ptr<int>> des_vec;
des_vec.push_back(std::move(s5));
des_vec.insert(des_vec.end(), std::make_move_iterator(vec.begin()), std::make_move_iterator(vec.end()));
display_vector(des_vec);
cout << "now, des_vec size: " << des_vec.size() << endl;
cout << "now, vec size: " << vec.size() << endl;

//display_vector(vec);
cout << "now, vec size: " << vec.size() << endl;
for (int i=0; i<vec.size(); i++)
{
	cout << *vec[i] << " ";//报错了，无法操作解引用uninitialize的地址
}
vec.clear();
```
