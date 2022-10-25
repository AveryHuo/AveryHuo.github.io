---
title: C++ 复习1
cover: false
date: 2022-05-19 21:28:29
updated: 2022-10-25 18:20:12
top_img: false
categories:
- CPlusPlus
tags: 
- C++
---

#### 关于无符号与有符号数
* 无符号不能为负数
* 循环如果使用无符号计数，以>=为条件将导致死循环

#### C++ 11的初始化方法
```c++
int a{0};
```

#### extern的使用
* 对于希望分离成多个文件独立编译的变量，使用extern公开出去
* 声明一个变量并extern出去，但注意不要声明+定义一起，否则失去了extern作用了
* extern变更的声明可以在多个文件，但定义只能在一个文件

#### 复合类型：引用与指针
* 引用类型一旦初始化就与初始对象绑定在一起，不可以更换绑定。且必须在定义时赋值。
* 引用类型不可以与值绑定
* 指针可以不在声明时初始化，指针是一个对象
* 指针赋值之间类型必须相同
* C++ 11的标准提供了nullptr为指针初始化为空。 引用cstdlib标准库中，还可以用NULL为指针初始化
* 任何非0的指针都为true.
* void＊指针，可用于存放任意对象的地址，但不能直接操作指针所指的对象，可理解为操作内存空间

#### 理解复合类型
* 对于一个变量，要理解其类型，最简单的办法从右向左阅读变量的定义，离变量名最近的对变量有最直接的影响。
```c++
int i = 42;
int *p;
int *&r = p; //r是对指针p的一个引用类型变量

r = &i; //给r赋值，就是给p的地址赋值，因此此时 p的值指向了i的地址
*r = 0;//i的值也为0
```

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

#### 常量表达式 constexpr
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

#### 类型别名
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

#### Auto类型说明符 (C++11)

不需要强制为某个变量指定类型的声明方式
* 注意： auto一般会忽略掉顶层的const，当auto引用时！才会保留const
* auto多变量声明类型必须一样
```c++
int i = 0;
const int ci = i;
//以下错误，因为n和p的类型不同，n是整型指针，ci是整型常量指针。
auto &n = i, *p = &ci;
```

#### decltype类型说明符（C++11）

使用decltype可取出表达式或变量的类型，以此类型再声明变量。

* 注意：与auto不同的是decltype的值与其内的变量或表达式密切相关，同时也可使用到顶层const和引用。
* 注意：带括号的表达式或变量，使用decltype时，将必定！返回对应结果的引用类型。而且普通无多个括号时，只有表达式或变量是引用类型才为引用。
```c++
decltype((i)) d; // 错误，d的类型最终为int &, 引用类型必须初始化才行
```

#### 关于结构体
C++11新标准规定可以为结构体内的变量设置初始值

#### 关于using的用法
 ```c++
 using std:cin;
 using namespace std;
 ```
 
 * 注意一般不要在头文件中使用using


#### string
* string相加的注意
```c++
string s1 = "H"+"s"; //错误，无法确定为string类型
```
* string的size()返回的size_type，不确定具体类型，但一定是无符号的，所以比对时一定注意。

#### for ： （C++ 11）
类似于foreach，for 与： 结合取出对象。

#### vector
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


#### 迭代器的使用

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



#### 数组的使用

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

#### C风格字符串
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

#### 与旧代码兼容
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

#### 多维数组
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

#### 运算符组合使用
注意++ 运算符优先级高于解引用优先级
```c++
	int b[3][4] = {1,2,3,4,5,6,7,8,9,10,11,12};
	auto p = begin(b[0]);
	cout << *p++ << endl; //1
	cout << *p << endl; //2
	cout << *++p << endl; //3
//*p++;//p为迭代器时，返回迭代器的值，同时地址往前移一位
```

#### 位运算符
```c++
<< //左移运算符，将一个数的二进制向左移一定位数
>> //右移运算符，将一个数的二进制向右移一定位数
| //逻辑或，二进制相同位上的值，有一个为1则为1
& //逻辑与，二进制相同位上的值，都为1则为1
^ //逻辑异或，二进制相同位上的值，相同则为0，不同则为1
```
*　优先级： 算术运算符 >　移位运算符　＞条件运算符

#### 函数

* 函数的形参会自动忽略顶层const。
* 尽量将不改动的对象形参设为常量形参。以阻止调用时出错。

#### 内联函数

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

#### 类成员
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

#### 析构函数
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