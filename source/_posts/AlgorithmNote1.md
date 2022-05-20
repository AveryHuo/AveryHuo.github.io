---
title: Coursera算法课笔记1
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1598259821964.png
categories:
- 算法
---

## UnionFind

### 描述
Dynamic Connectivity 动态连通性问题
 1.给定任意N数据集
 2.判断p到q是否连通

> 假定的前提： p连q，则q也连p。 

### 算法1： Quick Find -快速查找

* 数据结构
数组，将每个元素存储一个id[]下

* 算法思路
将相连通的所有元素存储为一个相同的ID
![存储结果](/img/1598259821964.png)

* 分析
 ![分析](/img/1598260733232.png)
 
 ### 算法2： Quick Union -快速交集
 
 * 数据结构
   与Quick Find一样，采取 数组
   
 * 算法思路
   1.每位数仅记录其根结点
   2.Union函数调用时，设第一个数为p，第二数为q。 将p的root赋值为q的root，即q的root为p的root的新root

  * 分析：
   ![分析](/img/1598273584691.png)
   
   ### 算法优化一： 使用权重
   
   * 永远只将小树往大树挂。这样不会产生过深的树层次！
   
   ![示例结果](/img/1598273763851.png)
  
  * 实现：额外定义一个数组，存储树的权重，在添加时判定，只将权重小的往权重大的加

### 算法优化二： 压缩

 * Union函数调用时，对于多于一层的树，全部将真正的root改为当前的上级

![示例结果](/img/1598273932723.png)



### C++实例、例子：

```c++

////////////////// Quick Find /////////////
QuickFind_UF::QuickFind_UF(int N) {
	
	this->length = N;
	this->id = new int[N];
	for (int i = 0; i < N; i++)
	{
		this->id[i] = i;
	}
}

QuickFind_UF::~QuickFind_UF() {
	this->length = 0;
	delete[] this->id;
}

void QuickFind_UF::Union(int p, int q) {
	int pid = this->id[p];
	int qid = this->id[q];//以此为准

	for (int i = 0; i < this->length; i++)
	{
		if (this->id[i] == pid)
			this->id[i] = qid;
	}
	Print();
}

bool QuickFind_UF::Connected(int p, int q) {
	return this->id[p] == this->id[q];
}

////////////////// Quick Union & Weight & Compression /////////////

QuickUnion_UF::QuickUnion_UF(int N) {

	this->length = N;
	this->id = new int[N];
	this->sz = new int[N];
	for (int i = 0; i < N; i++)
	{
		this->sz[i] = 1;
		this->id[i] = i;
	}	
}

QuickUnion_UF::~QuickUnion_UF() {
	delete[] this->id;
}

void QuickUnion_UF::SetUseWeight(bool use) {
	this->useWeight = use;
}

void QuickUnion_UF::SetUseCompression(bool use) {
	this->useCompression = use;
}

int QuickUnion_UF::Root(int i) {

	while (this->id[i] != i) {
		if (this->useCompression) {
			this->id[i] = this->id[this->id[i]];
		}
		i = this->id[i];
	}
	return i;
}

void QuickUnion_UF::Union(int p, int q) {
	int pid = this->Root(p);
	int qid = this->Root(q);
	if (this->useWeight) {
		if (pid == qid)
			return;
		if (this->sz[pid] < this->sz[qid]) {
			this->id[pid] = qid;
			this->sz[qid] += this->sz[pid];
		}
		else {
			this->id[qid] = pid;
			this->sz[pid] += this->sz[qid];
		}
	}
	else {
		this->id[pid] = this->id[qid];
	}
	
}

bool QuickUnion_UF::Connected(int p, int q) {
	return this->Root(p) == this->Root(q);
}

```
> 测试：数组为0-9，输入union:  (4,3),(3,8),(6,5),(9,4),(2,1),(8,9),(5,0),(7,2), (6,1)

> Quick Find 结果：
![QuickFind](/img/1598274190104.png)

> 多一个测试union: ,(7,3). Quick Union 结果：
![QuickUnion](/img/1598274216079.png)

> 多一个测试union: ,(7,3). Quick Union+ Weight结果：
![QuickUnion+Weight](/img/1598274276096.png)


## C++ 玫举与玫举类：

* 普通玫举是以（int）值进行比较，而玫举类可以根据不同名字来避免相同：
  
 ```c++
  enum Color { red, green, blue };                    // plain enum 
enum Card { red_card, green_card, yellow_card };    // another plain enum 
enum class Animal { dog, deer, cat, bird, human };  // enum class
enum class Mammal { kangaroo, deer, human };        // another enum class

void fun() {

    // examples of bad use of plain enums:
    Color color = Color::red;
    Card card = Card::green_card;

    int num = color;    // no problem

    if (color == Card::red_card) // no problem (bad)
        cout << "bad" << endl;

    if (card == Color::green)   // no problem (bad)
        cout << "bad" << endl;

    // examples of good use of enum classes (safe)
    Animal a = Animal::deer;
    Mammal m = Mammal::deer;

    int num2 = a;   // error
    if (m == a)         // error (good)
        cout << "bad" << endl;

    if (a == Mammal::deer) // error (good)
        cout << "bad" << endl;

}
 ```
 
 ## 希尔排序
  
  * 选用Knuth的一增量序列 3X+1
 
   * 先排大段，再排小段，一直到1段：

![分级排序](/img/1598514940240.png)

![优势](/img/1598516074235.png)

```c++
/// <summary>
/// 希尔排序 
/// </summary>
/// <param name="a"></param>
/// <param name="len"></param>
void ShellSort(int *a, int len){

	int isSorted = true;
	//优化一：提前做一个相邻位置排序
	for (int i = len-1; i > 0; i--)
	{
		if (a[i] < a[i - 1]) {
			SortHelper::Exch(a, i, i - 1);
			isSorted = false;
		}
	}
	if (isSorted) return;

	int h = 1;
	//得到一个最高的分级值
	while (h <= len / 3)
		h = 3 * h + 1;

	while (h >= 1) {
		//插入排序
		for (int i = h; i < len; i++)
		{
			for (int j = i; (j >= h) && (a[j] < a[j - h]); j -= h)
			{
				SortHelper::Exch(a, j, j - h);
			}
		}
		h = h / 3;
	}
}
```

## 堆排序

![java示例](/img/1598929159605.png)
