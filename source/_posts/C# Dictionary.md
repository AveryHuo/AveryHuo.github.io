---
title: C# Dictionary
categories:
- Unity
---

参考： https://www.cnblogs.com/InCerry/p/10325290.html

## 一、前言

Dictionary最大的优点就是它查找元素的时间复杂度接近O(1)，实际项目中常被用来做一些数据的本地缓存，提升整体效率。

那么是什么样的设计能使得Dictionary类能实现O(1)的时间复杂度呢？

## 二、理论知识

### 1.HASH算法
对于Dictionary的实现原理，其中有两个关键的算法，一个是Hash算法，一个是用于应对Hash碰撞冲突解决算法。

Hash算法是一种数字摘要算法，它能将不定长度的二进制数据集给映射到一个较短的二进制长度数据集，常见的MD5算法就是一种Hash算法，通过MD5算法可对任何数据生成数字摘要。而实现了Hash算法的函数我们叫她Hash函数。Hash函数有以下几点特征。

* 相同的数据进行Hash运算，得到的结果一定相同。HashFunc(key1) == HashFunc(key1)
* 不同的数据进行Hash运算，其结果也可能会相同，(Hash会产生碰撞)。key1 != key2 => HashFunc(key1) == HashFunc(key2).
* Hash运算时不可逆的，不能由key获取原始的数据。key1 => hashCode但是hashCode =\=> key1。

常见的构造Hash函数的算法有以下几种。
1. 直接寻址法：取keyword或keyword的某个线性函数值为散列地址。即H(key)=key或H(key) = a•key + b，当中a和b为常数（这样的散列函数叫做自身函数）
2. 数字分析法：分析一组数据，比方一组员工的出生年月日，这时我们发现出生年月日的前几位数字大体同样，这种话，出现冲突的几率就会非常大，可是我们发现年月日的后几位表示月份和详细日期的数字区别非常大，假设用后面的数字来构成散列地址，则冲突的几率会明显减少。因此数字分析法就是找出数字的规律，尽可能利用这些数据来构造冲突几率较低的散列地址。
3. 平方取中法：取keyword平方后的中间几位作为散列地址。
4. 折叠法：将keyword切割成位数同样的几部分，最后一部分位数能够不同，然后取这几部分的叠加和（去除进位）作为散列地址。
5. 随机数法：选择一随机函数，取keyword的随机值作为散列地址，通经常使用于keyword长度不同的场合。
6. 除留余数法：取keyword被某个不大于散列表表长m的数p除后所得的余数为散列地址。即 H(key) = key MOD p, p<=m。不仅能够对keyword直接取模，也可在折叠、平方取中等运算之后取模。对p的选择非常重要，一般取素数或m，若p选的不好，容易产生碰撞.


### 2、Hash桶算法
说到Hash算法大家就会想到Hash表，一个Key通过Hash函数运算后可快速的得到hashCode，通过hashCode的映射可直接Get到Value，但是hashCode一般取值都是非常大的，经常是2^32以上，不可能对每个hashCode都指定一个映射。

因为这样的一个问题，所以人们就将生成的HashCode以分段的形式来映射，把每一段称之为一个Bucket（桶），一般常见的Hash桶就是直接对结果取余。

假设将生成的hashCode可能取值有2^32个，然后将其切分成一段一段，使用8个桶来映射，那么就可以通过bucketIndex = HashFunc(key1) % 8这样一个算法来确定这个hashCode映射到具体的哪个桶中。

大家可以看出来，通过hash桶这种形式来进行映射，所以会加剧hash的冲突。

### 3、解决冲突算法
对于一个hash算法，不可避免的会产生冲突，那么产生冲突以后如何处理，是一个很关键的地方，目前常见的冲突解决算法有拉链法(Dictionary实现采用的)、开放定址法、再Hash法、公共溢出分区法，本文只介绍拉链法与再Hash法，对于其它算法感兴趣的同学可参考文章最后的参考文献。

1. 拉链法：这种方法的思路是将产生冲突的元素建立一个单链表，并将头指针地址存储至Hash表对应桶的位置。这样定位到Hash表桶的位置后可通过遍历单链表的形式来查找元素。

2. 再Hash法：顾名思义就是将key使用其它的Hash函数再次Hash，直到找到不冲突的位置为止。


![拉链法解决冲突](/img/1608693331816.png)

## 三、Dictionary实现

1. Entry结构体
首先我们引入Entry这样一个结构体，它的定义如下代码所示。这是Dictionary种存放数据的最小单位，调用Add(Key,Value)方法添加的元素都会被封装在这样的一个结构体中。

``` csharp
private struct Entry {
    public int hashCode;    // 除符号位以外的31位hashCode值, 如果该Entry没有被使用，那么为-1
    public int next;        // 下一个元素的下标索引，如果没有下一个就为-1
    public TKey key;        // 存放元素的键
    public TValue value;    // 存放元素的值
}
```

2. 其它关键私有变量
除了Entry结构体外，还有几个关键的私有变量，其定义和解释如下代码所示。

``` csharp
private int[] buckets;		// Hash桶
private Entry[] entries;	// Entry数组，存放元素
private int count;			// 当前entries的index位置
private int version;		// 当前版本，防止迭代过程中集合被更改
private int freeList;		// 被删除Entry在entries中的下标index，这个位置是空闲的
private int freeCount;		// 有多少个被删除的Entry，有多少个空闲的位置
private IEqualityComparer<TKey> comparer;	// 比较器
private KeyCollection keys;		// 存放Key的集合
private ValueCollection values;		// 存放Value的集合
```

上面代码中，需要注意的是buckets、entries这两个数组，这是实现Dictionary的关键。


3. Dictionary - Add操作

![初始状态](/img/1608693746908.png)
![添加一个元素后](/img/1608693760326.png)
![出现冲突hash](/img/1608693801943.png)
![解决后](/img/1608693812822.png)


4. Dictionary - Find操作

``` csharp
// 寻找Entry元素的位置
private int FindEntry(TKey key) {
    if( key == null) {
        ThrowHelper.ThrowArgumentNullException(ExceptionArgument.key);
    }

    if (buckets != null) {
        int hashCode = comparer.GetHashCode(key) & 0x7FFFFFFF; // 获取HashCode，忽略符号位
        // int i = buckets[hashCode % buckets.Length] 找到对应桶，然后获取entry在entries中位置
        // i >= 0; i = entries[i].next 遍历单链表
        for (int i = buckets[hashCode % buckets.Length]; i >= 0; i = entries[i].next) {
            // 找到就返回了
            if (entries[i].hashCode == hashCode && comparer.Equals(entries[i].key, key)) return i;
        }
    }
    return -1;
}
...
internal TValue GetValueOrDefault(TKey key) {
    int i = FindEntry(key);
    // 大于等于0代表找到了元素位置，直接返回value
    // 否则返回该类型的默认值
    if (i >= 0) {
        return entries[i].value;
    }
    return default(TValue);
}
```

5. Dictionary - Remove

``` csharp
public bool Remove(TKey key) {
    if(key == null) {
        ThrowHelper.ThrowArgumentNullException(ExceptionArgument.key);
    }

    if (buckets != null) {
        // 1. 通过key获取hashCode
        int hashCode = comparer.GetHashCode(key) & 0x7FFFFFFF;
        // 2. 取余获取bucket位置
        int bucket = hashCode % buckets.Length;
        // last用于确定是否当前bucket的单链表中最后一个元素
        int last = -1;
        // 3. 遍历bucket对应的单链表
        for (int i = buckets[bucket]; i >= 0; last = i, i = entries[i].next) {
            if (entries[i].hashCode == hashCode && comparer.Equals(entries[i].key, key)) {
                // 4. 找到元素后，如果last< 0，代表当前是bucket中最后一个元素，那么直接让bucket内下标赋值为 entries[i].next即可
                if (last < 0) {
                    buckets[bucket] = entries[i].next;
                }
                else {
                    // 4.1 last不小于0，代表当前元素处于bucket单链表中间位置，需要将该元素的头结点和尾节点相连起来,防止链表中断
                    entries[last].next = entries[i].next;
                }
                // 5. 将Entry结构体内数据初始化
                entries[i].hashCode = -1;
                // 5.1 建立freeList单链表
                entries[i].next = freeList;
                entries[i].key = default(TKey);
                entries[i].value = default(TValue);
                // *6. 关键的代码，freeList等于当前的entry位置，下一次Add元素会优先Add到该位置
                freeList = i;
                freeCount++;
                // 7. 版本号+1
                version++;
                return true;
            }
        }
    }
    return false;
}
```

6.Dictionary Resize

* 第一种情况自然就是数组已经满了，没有办法继续存放新的元素。
  
* 第二种，Dictionary中发生的碰撞次数太多，会严重影响性能，也会触发扩容操作。
目前.Net Framwork 4.7中设置的碰撞次数阈值为100.

``` csharp
public const int HashCollisionThreshold = 100;
```

``` csharp
private void Resize(int newSize, bool forceNewHashCodes) {
    Contract.Assert(newSize >= entries.Length);
    // 1. 申请新的Buckets和entries
    int[] newBuckets = new int[newSize];
    for (int i = 0; i < newBuckets.Length; i++) newBuckets[i] = -1;
    Entry[] newEntries = new Entry[newSize];
    // 2. 将entries内元素拷贝到新的entries总
    Array.Copy(entries, 0, newEntries, 0, count);
    // 3. 如果是Hash碰撞扩容，使用新HashCode函数重新计算Hash值
    if(forceNewHashCodes) {
        for (int i = 0; i < count; i++) {
            if(newEntries[i].hashCode != -1) {
                newEntries[i].hashCode = (comparer.GetHashCode(newEntries[i].key) & 0x7FFFFFFF);
            }
        }
    }
    // 4. 确定新的bucket位置
    // 5. 重建Hahs单链表
    for (int i = 0; i < count; i++) {
        if (newEntries[i].hashCode >= 0) {
            int bucket = newEntries[i].hashCode % newSize;
            newEntries[i].next = newBuckets[bucket];
            newBuckets[bucket] = i;
        }
    }
    buckets = newBuckets;
    entries = newEntries;
}
```

7. Dictionary - 再谈Add操作
在我们之前的Add操作步骤中，提到了这样一段话，这里提到会有一种其它的情况，那就是有元素被删除的情况。

避开一种其它情况不谈，接下来它会将hashCode、key、value等信息存入entries[count]中，因为count位置是空闲的；继续count++指向下一个空闲位置。上图中第一个位置，index=0就是空闲的，所以就存放在entries[0]的位置。
因为count是通过自增的方式来指向entries[]下一个空闲的entry，如果有元素被删除了，那么在count之前的位置就会出现一个空闲的entry；如果不处理，会有很多空间被浪费。

这就是为什么Remove操作会记录freeList、freeCount，就是为了将删除的空间利用起来。实际上Add操作会优先使用freeList的空闲entry位置，摘录代码如下。

``` csharp
private void Insert(TKey key, TValue value, bool add){
    
    if( key == null ) {
        ThrowHelper.ThrowArgumentNullException(ExceptionArgument.key);
    }

    if (buckets == null) Initialize(0);
    // 通过key获取hashCode
    int hashCode = comparer.GetHashCode(key) & 0x7FFFFFFF;
    // 计算出目标bucket下标
    int targetBucket = hashCode % buckets.Length;
	// 碰撞次数
    int collisionCount = 0;
    for (int i = buckets[targetBucket]; i >= 0; i = entries[i].next) {
        if (entries[i].hashCode == hashCode && comparer.Equals(entries[i].key, key)) {
            // 如果是增加操作，遍历到了相同的元素，那么抛出异常
            if (add) {      
				ThrowHelper.ThrowArgumentException(ExceptionResource.Argument_AddingDuplicate);
            }
            // 如果不是增加操作，那可能是索引赋值操作 dictionary["foo"] = "foo"
            // 那么赋值后版本++，退出
            entries[i].value = value;
            version++;
            return;
        }
        // 每遍历一个元素，都是一次碰撞
        collisionCount++;
    }
    int index;
    // 如果有被删除的元素，那么将元素放到被删除元素的空闲位置
    if (freeCount > 0) {
        index = freeList;
        freeList = entries[index].next;
        freeCount--;
    }
    else {
        // 如果当前entries已满，那么触发扩容
        if (count == entries.Length)
        {
            Resize();
            targetBucket = hashCode % buckets.Length;
        }
        index = count;
        count++;
    }

    // 给entry赋值
    entries[index].hashCode = hashCode;
    entries[index].next = buckets[targetBucket];
    entries[index].key = key;
    entries[index].value = value;
    buckets[targetBucket] = index;
    // 版本号++
    version++;

    // 如果碰撞次数大于设置的最大碰撞次数，那么触发Hash碰撞扩容
    if(collisionCount > HashHelpers.HashCollisionThreshold && HashHelpers.IsWellKnownEqualityComparer(comparer)) 
    {
        comparer = (IEqualityComparer<TKey>) HashHelpers.GetRandomizedEqualityComparer(comparer);
        Resize(entries.Length, true);
    }
}
```

8. Collection版本控制
![示例](/img/1608694671258.png)

![代码](/img/1608694646427.png)