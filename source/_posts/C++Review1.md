---
title: C++ 复习1
cover: false
date: 2022-05-19 21:28:29
updated: 2023-02-01 15:38:50
top_img: false
categories:
- CPlusPlus
tags: 
- C++
---

### 一、 关于无符号与有符号数
* 无符号不能为负数
* 循环如果使用无符号计数，以>=为条件将导致死循环

### 二、 C++ 11的初始化方法
```c++
int a{0};
```

### 三、 extern的使用
* 对于希望分离成多个文件独立编译的变量，使用extern公开出去
* 声明一个变量并extern出去，但注意不要声明+定义一起，否则失去了extern作用了
* extern变更的声明可以在多个文件，但定义只能在一个文件

### 四、复合类型：引用与指针
* 引用类型一旦初始化就与初始对象绑定在一起，不可以更换绑定。且必须在定义时赋值。
* 引用类型不可以与值绑定
* 指针可以不在声明时初始化，指针是一个对象
* 指针赋值之间类型必须相同
* C++ 11的标准提供了nullptr为指针初始化为空。 引用cstdlib标准库中，还可以用NULL为指针初始化
* 任何非0的指针都为true.
* void＊指针，可用于存放任意对象的地址，但不能直接操作指针所指的对象，可理解为操作内存空间

### 五、理解复合类型
* 对于一个变量，要理解其类型，最简单的办法从右向左阅读变量的定义，离变量名最近的对变量有最直接的影响。
```c++
int i = 42;
int *p;
int *&r = p; //r是对指针p的一个引用类型变量

r = &i; //给r赋值，就是给p的地址赋值，因此此时 p的值指向了i的地址
*r = 0;//i的值也为0
```
### 六、const
* const 限定符， 声明了const后就不能改变其值，但可以使用非常量来初始化const值
* const 在多文件中的使用：在一个文件中用extern声明同时定义，其他文件中仅extern声明即可。
* const声明的任何类型都不可以改值！
* const指针， 即指针指向的地址是不能改变的
```c++
int *errNumb = 0;
int *const curErr = &errNumb;//curErr指针的指向的地址不能改变
const double pi = 3.14;
const double *const pip = &pi;// pip指向常量pi的常量指针
```
* 顶层const与底层const:　从变量名的左侧开始算，底层到高层。最右侧的为顶层const, 指针符左侧为底层const.
* 拷贝的操作必须两对象都具有相同的底层const
* 一般来说非常量可转换为常量。

### 七、常量表达式 constexpr
具有以下两个条件的可称为常量表达式：
1. 表达式左侧的变量需定义为常量
2. 表达式右侧的值是不用到运行时就能确定的。

C++ 11的标准规定，可以使用constexpr 让编译器验证是否为常量表达式，也可定义函数为constexpr 这样就可以在常量表达式中使用。
```c++
constexpr int mf =20;
constexpr int limit = mf+1;
constexpr int sz = size(); //size()一定要用constexpr声明。
```

* constexpr 定义指针，表达此指针为常量指针，因此根据常量指针的特点，必须进行初始化。
* 注意constexpr定义后的指针就为常量指针，即此const为指针对象的顶层const
```c++
const int *p = nullptr;
constexpr int *q = nullptr;
//p与q是非常不同的，p是一个指针，指向常量。 q是一个常量指针，其地址不能改。
```

### 八、类型别名
使用typedef 为类型起一个别名：
```c++
typedef int ss;
```

* C++ 11 新标准可使用using语法替换typedef
```c++
using ss = int;
```
* 特别注意当有const在最左侧声明时，带指针的类型别名解释不能直接替换后来翻译，如：
```c++
typedef char *pstring; //类型别名为指向char的指针
const pstring a;//a是指向char的常量指针
//const char* a;//a是指向const char的指针，与const pstring a表示不同！

```

### 九、Auto类型说明符 (C++11)

不需要强制为某个变量指定类型的声明方式
* 注意： auto一般会忽略掉顶层的const，当auto引用时！才会保留const
* auto多变量声明类型必须一样
```c++
int i = 0;
const int ci = i;
//以下错误，因为n和p的类型不同，n是整型指针，ci是整型常量指针。
auto &n = i, *p = &ci;
```

### 十、decltype类型说明符（C++11）

使用decltype可取出表达式或变量的类型，以此类型再声明变量。

* 注意：与auto不同的是decltype的值与其内的变量或表达式密切相关，同时也可使用到顶层const和引用。
* 注意：带括号的表达式或变量，使用decltype时，将必定！返回对应结果的引用类型。而且普通无多个括号时，只有表达式或变量是引用类型才为引用。
```c++
decltype((i)) d; // 错误，d的类型最终为int &, 引用类型必须初始化才行
```

### 十一、关于结构体
C++11新标准规定可以为结构体内的变量设置初始值

### 十二、关于using的用法
```c++
using std:cin;
using namespace std;
```

* 注意一般不要在头文件中使用using


### 十三、string
* string相加的注意
```c++
string s1 = "H"+"s"; //错误，无法确定为string类型
```
* string的size()返回的size_type，不确定具体类型，但一定是无符号的，所以比对时一定注意。

### 十四、 for ： （C++ 11）
类似于foreach，for 与： 结合取出对象。

### 十五、 vector
* 定义的方式：
```c++
vector<int> ivec;
vector<int> ivec2(ivec);
vector<int> ivec3 = ivec;
//C++ 11
vector<int> ivec4 = {5,6,7}

//10个int类型的元素，且全部为-1
vector<int> vec(10,-1);
//10个int类型的元素，且全部为默认初始值
vector<int> vec2(10);
```
* 区别初始化vector时，花号与普通括号内的值的意义。
* curly braces还可以智能识别，如果其内的第一位与vector不符，且为数字，则此第一位可以表示为初始化的长度。第二位必须与类型相符。

* 添加元素： push_back. 注意不可用下标添加元素
```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
	// your code goes here
	vector<string> myVec;
	myVec.push_back("a");
	myVec.push_back("b");
	cout<< myVec[1] << endl;
	auto &v = myVec[1];
	v = "c";
	cout<< myVec[1]<<endl;
	return 0;
}
```


### 十六、 迭代器的使用

string与vector都有迭代器。但返回的类型是未知的。因此经常使用auto来接收。

```c++
	// your code goes here
	vector<vector<string>> myVec;
	vector<string> iVec;
	iVec.push_back("a");
	myVec.push_back(iVec);
	
	if(myVec.begin() != myVec.end()){
		cout<< "非空vector"<<endl;
		auto firstVec = myVec.begin();
		auto &v = (*firstVec)[0];
		cout<< "第一个值："<< v;
		v = "b";
		cout<< "改：第一个值："<< (*firstVec)[0];
	}
```

* C++中推荐尽量使用迭代器加!= 来做遍历。因为标准库的容器都定义了== !=。大部分没有定义<比较。
```c++
	// your code goes here
	vector<int> myVec = {5,9,7,5,8,2};
	cout << myVec[1]<<endl;
	for(auto it = myVec.begin(); it != myVec.end() ; ++it){
		cout<< *it << endl; 
	}
```
* 迭代器的表示：
除了用auto外，还可以使用：：iterator，或：：const_iterator表示常量vector或string。

```c++
vector<int> a;
a.push_back(6);
vector<int>::iterator it = a.begin();
cout<< *it << endl;
```
> c++ 11 中引入 cbegin和cend用于表示vector的常量迭代器，返回永远是const_iterator.

* 访问迭代器
使用C++的箭头， 将解引用与.运算符合在一起了。
```c++
// (*it).mem //访问 解it引用后的成员mem
//it ->mem //与上面一样
```
> 特别注意，迭代器的循环不能添加元素，否则将破坏迭代器。

* 迭代器之间的运算：
+、- 一个数，表示移位置
+=、-=也适用
相减得到之间的距离：得到的类型为difference_type。为有符号类型。
大小比较根据位置而定



### 十七、 数组的使用

* 与vector区别，数组是定长的
* 不存在存引用的数组
```c++
int arr[10];//定义含10个元素的数组
int * parr[10];//含有10个整形指针的数组
```
* 显示初始化：
```c++
int a2[] = {0,2,1};// 自动设置维度为3
```

* 特殊情况的初始化：字符数组初始化必须加一个’\0‘结尾字符
```c++
char a3[] = "c++";//维度其实是4，因为会自动加一个结尾字符
```
* 重要：存对象的数组不需要由另一个数组拷贝，也不需要赋值！
* 可以定义引用或指针数组来指向一个普通的数组：
```c++
	int a[] = {1,5,3,6,8};
	int (*b)[5] = &a;
	int (&c)[5] = a;
	cout << a[0]<< endl;
	cout << *b[0]<<endl;
	cout << c[0]<<endl;
```
* 数组的size跟vector一样也是size_type

* 指针与数组：
```c++
string nums = {"a","b","c"};
string *p2 = nums;
//string p2 = nums[0];//与上面等价
```
* 对数组使用decltype关键字返回的是数组还不是指针。使用auto返回的是指针！
```c++
	int a[] = {1,5,3,6,8};
	auto b(a);//这是一个指针
	decltype(a) c = {5,9,8,7};//这是一个数组
```
* 指针其实也是一个迭代器，拥有之前迭代器的操作。
如用指针做迭代器输出：
```c++
	for(int *i = a; i != &a[5]; i++){
		cout << *i << endl;
	}
```
* C++ 11引入 begin和end函数用于取出数组的头尾指针位置。
```c++
	for(int *i = begin(a); i != end(a); i++){
		cout << *i << endl;
	}
```
> begin与end相减返回的类型为ptrdiff_t。与迭代器之差不同。但类型类似是符号数

* 指针当成数组用：数组下标与vector和string不同，不是无符号类型！。可为负数。
```
int *p = &ia[2];
int j = p[1];//与*(p+1)等价
int k = p[-2];//返回ia[0]的元素
```

### 十八、  C风格字符串
* C风格的字符串，操作的都是指针，而没有string对象的操作。
* C++中的cstring就是string.h的C++版本。
* 使用C风格字符串，必须保证字符数组以'\0'结尾，否则就会发生严重错误！
* 常用函数
```c
strlen(p)
strcmp()//比较相等，相等返回0，大于为正值
strcat(p1,p2)//连接，p2加到p1,返回p1。必须保证p1能装得下p2
strcpy(p1,p2)//p2拷贝到p1，返回p1
```
> 使用C的字符串在估算数组长度时会充满风险，建议使用标准库string.

### 十九、 与旧代码兼容
以下 C字符串意为： 以空字符结尾的字符数组 
* 1. 允许使用C字符串初始化 string，或为其赋值
* 2. string的加法运算，允许有一个C字符串
* 3. string的复合赋值，右侧可以为一个C字符串
此三个专为string标准库设计，反之如果是C字符则不行。但可以使用string.cstr()返回一个C字符串。如：
```c++
string s("Hello");
char * str = s;//错误，string不能给str赋值
const char *str = s.cstr();//正确，但如果一直要用此值，最好重新拷贝
```

*  以数组初始化vector
```c++
int a[] = {1,5,3,6,8};
vector<int> ivec(begin(a),end(a));
cout << ivec[0] << endl;
```

### 二十、 多维数组
本身C++是没有多维数组的，可以用一个指针嵌套的思想理解。从左往右的理解一个多维数组。
如3,4的数组表示数组有三个元素，每个元素又是一个有四个元素的数组
* 定义，二维数组可理解为行和列，平铺式的定义是以一行一行的定义来：
```c++
	int a[3][4] = {
		{1,2,3,4},
		{5,6,7,8},
		{9,10,11,12}
	};
	int b[3][4] = {1,2,3,4,5,6,7,8,9,10,11,12};//与a等价
```
* 遍历查值，除了用下标查找外，可以使用C++ 11的for
```c++
int b[3][4] = {1,2,3,4,5,6,7,8,9,10,11,12};
	for(auto &row:b){//注意必须使用引用，因为否则auto将自动转成指针，无法进行下一步
		for(auto &i:row){
			cout << i <<endl;
		}
	}
```

* 注意括号的使用：
```c++
int *p[4];//一个有四个整型指针的数组
int (*p)[4];//定义一个数组指针，指向四元素的数组
```

* 使用auto遍历：
```c++
	for(auto p = b;p != b+3;p++){
		for(auto q = *p; q != (*p)+4; q++){
			cout << *q <<endl;
		}
	}
	//当然可以使用begin和end函数
```
* 使用类型别名来定义多维数组里的内部：
```c++
using int_array = int[4];//c++11标准
```

### 二十一、 运算符组合使用
注意++ 运算符优先级高于解引用优先级
```c++
	int b[3][4] = {1,2,3,4,5,6,7,8,9,10,11,12};
	auto p = begin(b[0]);
	cout << *p++ << endl; //1
	cout << *p << endl; //2
	cout << *++p << endl; //3
//*p++;//p为迭代器时，返回迭代器的值，同时地址往前移一位
```

### 二十二、 位运算符
```c++
<< //左移运算符，将一个数的二进制向左移一定位数
>> //右移运算符，将一个数的二进制向右移一定位数
| //逻辑或，二进制相同位上的值，有一个为1则为1
& //逻辑与，二进制相同位上的值，都为1则为1
^ //逻辑异或，二进制相同位上的值，相同则为0，不同则为1
```
*　优先级： 算术运算符 >　移位运算符　＞条件运算符

### 二十三、 函数

* 函数的形参会自动忽略顶层const。
* 尽量将不改动的对象形参设为常量形参。以阻止调用时出错。

### 二十四、 内联函数inline

* 使用Inline定义内联函数
* 当函数被声明为内联函数之后, 编译器会将其内联展开, 而不是按通常的函数调用机制进行调用.
> 在使用内联函数时要留神：
1.在内联函数内不允许使用循环语句和开关语句；
2.内联函数的定义必须出现在内联函数第一次调用之前；
3.类结构中所在的类说明内部定义的函数是内联函数。
Tip： 只有当函数只有 10 行甚至更少时才将其定义为内联函数.
优点: 当函数体比较小的时候, 内联该函数可以令目标代码更加高效. 对于存取函数以及其它函数体比较短, 性能关键的函数, 鼓励使用内联.
缺点: 滥用内联将导致程序变慢. 内联可能使目标代码量或增或减, 这取决于内联函数的大小. 内联非常短小的存取函数通常会减少代码大小, 但内联一个相当大的函数将戏剧性的增加代码大小. 现代处理器由于更好的利用了指令缓存, 小巧的代码往往执行更快。
结论: 一个较为合理的经验准则是, 不要内联超过 10 行的函数. 谨慎对待析构函数, 析构函数往往比其表面看起来要更长, 因为有隐含的成员和基类析构函数被调用!

### 二十五、类成员
* C++11 标准中，将默认值声明成一个类内初始值：
```c++
//类里定义
std::vector<Screen> screens{Screen(24, 80, '')};
```

* 返回值类型为引用与普通的区别
```c++
//如下如果改为返回Screen对象而非引用，将导致访问到的只是拷贝
Screen &Screen::set(pos r)
{
	contents[r] = 10;
	return *this;
}
```
* 如果一个const成员函数以引用形式返回 * this, 则其返回类型是常量引用。因此如下代码无法执行
```c++
//假定display为返回const
myScreen.display(cout).set('s');
```

### 二十六、 析构函数
参考文章：https://blog.csdn.net/yangkunqiankun/article/details/74885784

对于非指针类型的对象，离开作用域会主动调用析构
另外由于vector的扩容机制问题，也会导致对象的复制拷贝过程，从而对于对象会导致其析构

```c++
void initShaders() {
    ShaderInclude::ShaderSource vecShaderSource = ShaderInclude::load(shaderDir + "vec.glsl");
    ShaderInclude::ShaderSource fragShaderSource = ShaderInclude::load(shaderDir + "frag.glsl");

    auto vertShader = Shader(vecShaderSource, GL_VERTEX_SHADER);
    auto fragShader = Shader(fragShaderSource, GL_FRAGMENT_SHADER);
    auto fragShader2 = Shader(ShaderInclude::load(shaderDir + "frag2.glsl"), GL_FRAGMENT_SHADER);
    std::vector<Shader> shaders1{ vertShader, fragShader };
    std::vector<Shader> shaders2{ vertShader, fragShader2 };

    printf("Dummy 1\n");
    shaderProgram = new ShaderProgram(shaders1);
    shaderProgram2 = new ShaderProgram(shaders2);
}

//以上函数Shader的析构会调用多少次？
// Shader delete!: 2
// Shader delete!: 1
// Shader delete!: 3
// Shader delete!: 1
// Dummy 1
// Shader delete!: 1
// Shader delete!: 2
// Shader delete!: 1
// Shader delete!: 3
// Shader delete!: 1
// Shader delete!: 3
// Shader delete!: 1
// Shader delete!: 2
// Shader delete!: 3
// Shader delete!: 2
// Shader delete!: 1
```
### 二十七、 C++ noexcept

* 表明此函数没有异常
* C++11后的新特性
* 使用后，本来的throw将不再抛到上层，会直接调用 terminate终止
```cpp
double &Vector::operator[](int i) noexcept{
    if(i < 0 || i > size()){
        throw std::out_of_range{"Vector out of range"};
    }
    return elem[i];
}


Vector user(int sz){
    Vector v(sz);
//    iota(&v[98], &v[100], 0);
    try{
        v[102] = 38;
        cout<< v[102] <<endl;
    }catch(out_of_range &err) {
        cerr<<err.what()<<endl;
    }
}

//输出：
//libc++abi: terminating with uncaught exception of type std::out_of_range: Vector out of range
//23,90
//look at me!
```
> 在删除noexcept时，将正常捕获异常

### 二十八、 类的不变式invariant
* 假设某事为真的声明为类不变式
* 类的不变式是构造函数的任务
```cpp
Vector v(23);
Vector::Vector(int s){
	if(s < 0){
		throw length_error("negative size");
	}
	elem = new double[s];
	sz = s;
}
```
### 二十九、 使用assert, static_assert 或 合约
* C* assert断言机制，如果内容发生异常，则会直接terminate
* static_assert 使用常量定义的检测

### 三十、 C++ 拷贝控制
#### 30.1 分类
在类通过定义五类特殊的成员函数：
拷贝构造函数
拷贝赋值运算符
移动构造函数
移动赋值运算符
析构函数

#### 30.2 拷贝构造函数
一个构造函数的第一个参数是自身引用，但任何额外参数都有默认值，由此为拷贝构造函数

Foo（const Foo&）

这两种都会走拷贝构造函数
string s = "abc";
string s("abc"); 

不仅出现在定义变量时，也出现在以下几种情况：
1. 实参传到非引用的参数
2. 返回值为非引用
3. 以花号初始化数组或一个聚合类成员

> 如果类中未定义，则默认编译器会生成一个
> 如果定义了explicit，则不能使用拷贝函数的行为

#### 30.3 拷贝赋值

Foo& operator=(const Foo&)

通常这种走拷贝赋值函数
f2 = f;
直接初始化时，编译器会主动找匹配的函数
Foo f2(200); 

Foo f3 = f2; //这样走的是赋值构造函数

> 如果类中未定义，则默认编译器会生成一个合成拷贝赋值运算符

#### 30.4 析构函数
不可被重载，且有唯一性，释放对象非static数据成员。
析构的部分是隐式的

> * 需要理解析构并不是执行销毁的过程，而只是成员销毁步骤的另一个部分
> * 由于内置类型没析构函数，所以销毁内置类型时什么也不会做，比如隐式销毁一个内置指针类型成员，不会销毁其指向的对象
> * 一个引用，或者指针离开作用域并不会调用其析构函数,所以需要手动去释放 
```cpp
{ //作用域
    Foo *f = new Foo();
    auto p = make_shared<Foo>();
    delete f;
}
//离开作用域，智能指针p会减引用计数到0，然后调用析构， f由于主动调用，也会调用析构
```

#### 30.5 三五原则 
* 三法则： 如果一个类需要自定义析构函数，那基本肯定的是也需要有自己的拷贝构造和拷贝赋值函数
* 如果有拷贝赋值，必然要有拷贝构造， 相反也成立。但不一定要有析构
> 扩展， 五法则，增加两种特殊函数，移动构造函数，移动赋值函数

#### 30.6 =default
当希望编译器用合成构造或合成赋值函数时，在后面接上=default即可。
> 在定义里使用=default表示使用内联的方式，要想使用非内联，可以在类定义外的地方使用=default
```cpp
Foo& Foo::operator=(Foo &) = default;
```
> =default只能对编译器带有合成功能的函数使用

#### 30.7 阻断合成 =delete
当不希望编译器为我们合成拷贝构造函数，赋值运算符函数时，必须在定义时使用=delete阻断

> =delete可对任意函数使用
> 析构函数一般不能被定义为=delete，否则将无法删除对象

> 如果一个类的某个成员，不具有拷贝, 复制，删除的功能，则对应到类的合成拷贝，赋值，删除函数将被默认=delete掉。 这个规则同样适用于有引用成员的类。

#### 30.8 使用private来阻断
使用private阻止了一般用户的访问，但友元函数和成员函数均可以访问，如果未定义，则会报链接错误。因此不推荐此种方法。

#### 30.9 类值的行为类
每一个拷贝后的东西都是自己独立的个体，而不会影响到原对象。
设计示例：
```cpp
//
// Created by Avery Huo on 2021/8/22.
//

#include "ValueAssignmentTemple.h"

ValueAssignmentTemple& ValueAssignmentTemple::operator=(ValueAssignmentTemple &s) {
    auto ns = new string(*s.ps);
    delete this->ps;
    this->ps = ns;
    this->i = s.i;
    return *this;
}

ValueAssignmentTemple& ValueAssignmentTemple::operator=(string &s) {
    *this->ps = s;
    return *this;
}

ValueAssignmentTemple::~ValueAssignmentTemple(){
    delete this->ps;
}

string &ValueAssignmentTemple::operator*() {
    return *this->ps;
}

//main.cpp
    ValueAssignmentTemple vat("God1");
    cout << *vat << endl;
    ValueAssignmentTemple vat2(vat);
    cout << *vat << "," << *vat2 <<endl;
    cout << vat.ps << "," << vat2.ps << endl;

//输出:
God1
get copyed
God1,God1
0x7fddf5c05a90,0x7fddf5c05ab0
```

> 赋值运算符函数的注意：
> 1. 要保证参数是自身的，即自己赋值给自己的情况
> 2. 先拷贝再删除自己对象的中的成员的指针。

#### 30.10 类指针的行为类
与类值的行为类对比，就是把一个成员的本身传过去，而不是拷贝。因此，为了不影响原对象，需要在析构进行判断，这里就需要加入一个引数计数的实现方法：
引用计数的意义： 当自己生成时，表示计数占一，当自己换成其他时，自己的计数要减一 
例：

```cpp
class PtrAssignmentTemple {
public:
    string *ps;
    int i;
    int *use;
    PtrAssignmentTemple(const PtrAssignmentTemple& s):ps(s.ps), i(s.i), use(s.use){
        ++*use;
    };
    PtrAssignmentTemple(const string &s = string()):ps(new string(s)),i(0), use(new int(1)){};
    PtrAssignmentTemple& operator=(PtrAssignmentTemple &);
    PtrAssignmentTemple& operator=(const string &);
    string& operator*();
    ~PtrAssignmentTemple();
};



PtrAssignmentTemple& PtrAssignmentTemple::operator=(PtrAssignmentTemple &s) {
    ++*s.use;
    if(--*this->use == 0)
    {
        delete this->ps;
        delete this->use;
    }
    this->ps = s.ps;
    this->use = s.use;
    return *this;
}

PtrAssignmentTemple& PtrAssignmentTemple::operator=(const string &s) {
    *this->ps = s;
    return *this;
}

PtrAssignmentTemple::~PtrAssignmentTemple(){
    if(--*this->use == 0)
    {
        delete this->ps;
        delete this->use;
    }
}

string &PtrAssignmentTemple::operator*() {
    return *this->ps;
}

// main.cpp
    PtrAssignmentTemple vat("God1");
    cout << *vat << endl;
    PtrAssignmentTemple vat2(vat);
    cout << *vat << "," << *vat2 <<endl;
    cout << vat.ps << "," << vat2.ps << endl;

//输出：
//God1
//God1,God1
//0x7fe33dc05a90,0x7fe33dc05a90
```
#### 30.11 对象移动
右值引用： 使用&& 表示， 只能绑定到将要销毁的对象上。表达式等。短暂。
左值引用：常规引用，持久
> 特别的，可以 将一个带const的引用绑定到右值引用上
> ```cpp
> int i = 2;
> const int &r3 = i * 42;
> ```

* 使用move，可以将一个左值显式转换为对应的右值引用
```cpp
int &&r1 = 42;
int &&r2 = std::move(r1);
```

#### 30.12 移动构造函数和移动赋值运算符

```cpp
class StrVec{
public:
	StrVec(StrVec&&) noexcept; // 移动构造函数
	StrVec &StrVec::operator=(StrVec &&rhs) noexcept; //移动赋值运算符
}
```

场景： 如果不想用拷贝，而只是想支持移动操作
注意： 任何额外的参数都必须有默认实参。 原因是移后源对象会被销毁，如果不在给定对象中未删除，新对象中的指针就会失效。所以应该要这样在移动构造函数中写：
```cpp
s.elements = s.first_free = s.cap = nullptr;
```

* 1. 移动构造函数
> 告诉标准库 noexcept的重要性，在移动操作过程中的发生的异常是不可处理的，标准库会为拷贝操作做异常处理，为了让标准库不做拷贝操作，这里需要指明noexcept

* 2. 移动赋值运算符
>  首先检测自身是否与参数的结果相同，如果一样，则按移动的处理是先free()自己，再将参数的引用传过来，最后再将参数置none使其进入析构。

#### 30.13 合成移动构造函数，移动赋值运算符

* 生成条件
条件1： 如果没有定义拷贝构造函数和拷贝赋值运算符和析构函数，编译器才会为其生成移动构造函数和移动赋值运算符。反之，如果定义了任一个，就不会生成，会默认使用拷贝操作。
条件2： 如果成员是类类型，则需要保证此类也有对应的移动操作才行

只有条件1和条件2都存在时，才会可能生成合成移动的函数和运算符。

* 与拷贝操作不同，移动操作永远不会被隐式定义为删除的函数，但如果强制用=default指定时，有可能被定义为删除的函数，条件如下：
1. 有成员不能合成移动构造函数或未定义时
2. 有类成员的移动构造函数被定义为删除时
3. 类的析构被定义为不可访问时
4. 类成员是const或引用时
> 定义了移动构造函数和移动运算符的类，也必须定义拷贝构造函数等，不然拷贝的相关函数会被定义为删除的

#### 30.14 同时都有的情况
移动右值，拷贝左值
```cpp
StrVec v1, v2;
v1 = v2;//拷贝
StrVec getVec(istream &);
v2 = getVec(cin);    //移动
```

> 如果没有定义移动或移动是删除的情况下，即使用了move函数，也会使用拷贝操作代替移动

#### 30.15 移动迭代器
改变迭代器解引用运算符行为来适配移动，生成移动迭代器。
此解引用运算符生成的将是一个右值引用，意味着构造函数将是一个移动构造函数。

#### 30.16 引用限定符
使用引用限定符，强制返回变为一个左值或右值，使用&表示 返回是一左值，&& 是右值
```cpp
Foo anotherMem() const &;
```

支持重载：
```cpp
Foo Foo::sorted() &&; //右值，可以直接使用，原地处理
Foo Foo::sorted() const &; //左值，需要拷贝
```
> 如果用了const标识，在加了引用限定符，在重载时必须指明引用限定符

### 三十一、C++ 重载运算与类型转换
#### 30.1 概念

* 通过参数个数分为：一元运算符，二元运算符。 除operator()外，其他不能有默认实参。
* 运算符函数是成员函数时，第一个左侧运算对象绑定到隐式的this指针上
* 不能重载已有的内置运算符
* （+、-、*、&*） 既是一元运算符，又是二元运算符。
* 运算符重载后优先级不变
* 作用域运算符不可重载
* 显示调用： data1.operator+=(data2)   等价于   data1 +=data2
* 一般不重载点运算符和取引用运算符
* 除了对称性的运算符，双与，算术，相等性，关系，一般都是成员函数
* 成员函数时，左侧运算对象表示为第一个所属类。
```cpp
struct node{
	int a;
	string name;
	operator +(node &b){
		a += b.a;
		name += b.name;
	}
};
```

#### 30.2 输入和输出运算符

“\>\>” 输入运算符, “\<\<” 输出运算符
* 重载输出运算符： 需要第一个参数为非常量的引用类型ostream， 因为需要改变其状态 ，且不能复制，所以用引用。
```cpp
ostream &operator<<(ostream &os, const Sales_data &item)
{
	os<<item.isbn() << " " << item.units_sold;
	return os;
}
```
> 必须是非成员函数，因为返回不能是this指针，而必须是osstream或isstream.
* 重载输入运算符：第一个参数为非常量的引用类型，第二参数必须为非常量，因为需要改变其状态
```cpp
istream &operator>>(isstream &is, Sales_data &item)
{
	double price;
	is >> item.book_name >> item.units_sold >> price;
	if (is) //检测是否正确
		item.revenue = item.units_sold * price;
	else
		item = Sales_Data();
	return is;
}
```
> 对于输入运算符重载，需要设定标识符，如failbit读取失败符, eofbit表示文件结束符

#### 30.3 算术和关系运算符
一般为非成员函数以允许左侧与右侧的运算对象进行互换。但一般需要实现复合赋值运算符！ 如下例中需要先定义+=运算符。在都定义的情况下，通常情况下应该使用复合赋值来实现算术运算符。
```cpp
Sales_data &operator+(const Sales_data &lhs,const Sales_data &rhs)
{
	Sales_data sum = lhs;
	sum += rhs;
	return sum;
}
```
* 相等与不相等运算符，一般都是成对出现在非成员函数中。
#### 30.4 下标运算符
* 必须是成员函数 
* 返回的是元素的引用
* 可以用常量标识返回的结果是否可以改变
```cpp
class StrVec{
public:
	std::string &operator[](std::size_t n)
	{ return elementes[n];}
	const std::string &operator[](std::size_t n) const
	{ return elementes[n];}
private:
	std::string *elements;
}
```
#### 30.5 递增递减运算符
* 建议为成员函数，不强制
* 需要定义前置和后置的两个版本，但由于同时存在时重载会有问题，所以会添加一个无用的int实参
```cpp
class StrBlobPtr{
public:
	//前置
	StrBlobPtr &operator++();
	StrBlobPtr &operator--();
	//后置
	StrBlobPtr operator++(int);
	StrBlobPtr operator--(int);
private:
	std::string *elements;
}

StrBlobPtr &StrBlobPtr::operator++()
{
	check(curr, 'increment past end!');
	curr++;
	return *this;
}

StrBlobPtr &StrBlobPtr::operator++()
{
	curr--;
	check(curr, 'increment past begin!');
	return *this;
}

StrBlobPtr StrBlobPtr::operator++(int)
{
	StrBlobPtr ret = *this;
	++*this;
	return ret;
}

StrBlobPtr StrBlobPtr::operator++()
{
	StrBlobPtr ret = *this;
	--*this;
	return ret;
}

//显式调用：
StrBlobPtr p(a1);
p.operator++(0); //后置
p.operator++(); //前置
```
#### 30.6 成员访问运算符
解引用运算符，箭头运算符
```cpp
class StrBlobPtr{
public:
	std::string &operator*() const
	{
		auto p = check(curr, "past end");
		return (*p)[curr];
	}

	std::string *operator->() const
	{
		return &this->operator*();//使用解引用运算符的实现
	}
}
```
> 箭头运算符不能改变其获取成员的事实

#### 30.7 函数调用运算符
如果一个类定义函数调用运算符，则该类的对象称作 函数对象
```cpp
struct absInt{
	int operator()(int val) const{
		return val < 0? -val; val;
	}
}
```
含状态的函数对象
```cpp
class PrintString{
public:
	PrintString(ostream &o = cout, char c = ' '): os(o), sep(c){}
	void operator()(const string &s) const {os << s << sep;}
private:
	ostream &os;
	char sep;
};

PrintString printer;
printer(s);
PrintString errors(cerr, '\n');
errors(s);
```
* 函数对象常作为泛型算法的实参，如for\_each
```cpp
for_each(vs.begin(), vs.end(), PrintString(cerr, '\n'));
```
* lambda是函数对象
```cpp
stable_sort(words.begin(), words.end(), [](const string &a, const string &b){return a.size() < b.size();})

其类似于：
class ShorterString{
public:
	bool operator()(const string &s1, const string &s2){
		return s1.size() < s2.size();
	}
}

stable_sort(words.begin(), words.end(), ShorterString());
```
*  标准库定义的函数对象
如加法plus， 二元的%取模 modulus, equal\_to等执行==。 如例：
```cpp
plus<int> intAdd;
negate<int> intNegate; //取反
int sum = intAdd(10, 20);
sum = intNegate(intAdd(10, 20));
```
作用：对于算法中的调用传递
```cpp
sort(svec.bein(), svec.end(), great<string>());
```
特别的，标准库的函数对象对于指针同样适用。
```cpp
sort(nameTable.begin(), nameTable.end(), less<string *>());
```
* 可调用对象
	函数，函数指针，lambda表达式，bind创建的对象等
	不同的可调用对象也有各自的类型，如：
```cpp
//函数指针
int add(int i, int j){return i+j;}
//lambda返回一个函数对象类
auto mod = [](int i, int j){return i % j}

//使用map进行存储
map<string, int(*)(int ,int)> binops;

binops.insert({"+", add});
```
* 标准库function类型
	使用function解决可调用对象的问题，其本质是一个模板。
```cpp
function<int(int, int)> f1 = add;
function<int(int, int)> f2 = divide();
function<int(int, int)> f3 = [](int i, int j){return i * j;};

map<string, function<int(int, int)>> binops = {
	{"+", add},
	{"-", std::minus<int>()},
	{"/", divide()},
	{"*", [](int i, int j){return i * j;}},
	{"mod", mod}
};
```
#### 30.8 类型转换运算符
特殊的成员函数，负责将一个类类型的值转换为其他类型，如：
```cpp
operator type() const;
```
* 必须为成员函数，不能有返回类型，形参列表必须为空，const
```cpp
class SmallInt{
public:
	SmallInt(int i = 0): val(i)
	{
		if (i < 0 || i > 255)
			throw std::out_of_range("Bad small int value");
	}
	operator int() const {return val;}
private:
	std::size_t val;
}

SmallInt si = 3.14; //float转int,int 再转SmallInt
si + 3.14;//转int再转double
```
* 显式的类型转换运算符
C++引入
```cpp
explicit operator int() const{return val;}

SmallInt si = 3;
si +3;//错
static_cast<int>(si) + 3; //显示调用，正确
```
> 特别的，显式的类型转换会被隐式调用，在if、while、for、条件运算符
```cpp
operator const int(); //必须接受一个const int类型
operator int() const; //返回int类型，表明不会改动参数值
```
* 避免二义性
	使用显式的调用来解决
	在成员函数中避免定义多个以内置算术类型为结果的运算符