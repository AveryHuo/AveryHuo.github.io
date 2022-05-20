---
title: 线性代数-笔记1
categories:
- 数学
---


#### 第一章、线性代数中的线性方程组

##### 
1.线性方程组等价⇔解集相同⇔增广矩阵行等价
2.线性方程组的解：null/one/infinite
3.线性方程组相容：有解（one/infinite）
4.行初等变换：
倍加：加上另一行的倍数
对换：两行互换
倍乘：一行各元素乘一个标量
5.行初等变换是可逆的
6.（行）阶梯形矩阵（缩写为REF）
每一非零行在每一零行之上
下方的行的先导元素在右方
> 推论：先导元素（一行的最左非零元素）所在列的下面全是零

7.简化（行）阶梯形（缩写为RREF）
先导元素都是1
先导元素是所在列唯一的非零元素
简化阶梯形是唯一的

8. 主元位置：阶梯形中先导元素的位置；主元列*：含主元位置的列
主元列对应基本变量，非主元列对应自由变量
9.线性方程组相容⇔增广矩阵最右列不是主元列（没有0=b情况出现，其中b为非零常数）
10.**向量方程**： 以向量的方式代表一个单列矩阵，如：（3，-1）对应2x1列矩阵
11.证明某个向量c在其他两个向量a,b组成的面上，只需要证明存在r1,r2为实数让c = r1a + r2b成立。
12.向量方程与矩阵方程：
向量方程以向量加未知数的形式组成部成方程。矩阵方程将方程组写成矩阵 乘 向量组成的方程。

