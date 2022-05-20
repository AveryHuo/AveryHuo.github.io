---
title: 动态规划
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- 算法
---

#### DP-Dynamic Programing 
* 试用场景：
大部分用于求最小值，最大值，最优，计数等的问题

* 一般步骤：递归+记忆化
* 1.寻找递归式：由大化小
* 2.先写递归式，记忆重复项以优化算法复杂度。解决子问题重叠求解。
* 3.优化为非递归： 由小到大，由大到小（记忆）。

#### 面试常见类型：
* 1.矩阵坐标型 30%
* 2.序列型：单序列，双序列  50%
> 单序列：LIS：longest increasing sequence 最长上升序列
> 双序列：LCS: longest common sequence 最长公共序列
* 3.Knapsack变种 20%
> subset sum. 硬币类题
* 4.区间型  <10%
> 矩阵相乘，optimised BST.