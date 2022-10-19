---
title: GAMES104-NOTE1
cover: false
date: 2022-10-19 11:07:16
updated: 2022-10-19 17:07:16
top_img: false
categories:
- 引擎,图形学
tags: 
- Game,Engine,图形学,CG
---

# 1.游戏引擎导论

* 什么是游戏引擎
1. 底层框架
2. 生产力工具
3. 复杂性的系统艺术集合

* 核心难点：
1. 游戏引擎最重要的难点是Realtime，必须在33毫秒之内将结果计算出来，是所有系统的计算结果计算出来，这就是现代游戏引擎设计的核心难点。
2. 游戏引擎不仅仅是一系列的算法，更是生产力的工具，需要成熟的工具链

* 学习的方式：
以framework为基准，自上往下再细致学习研究

# 2. 分层

* Tool Layer 工具层
* Function Layer 基本功能层
* Resource Layer 资源层，包括数据等
* Core Layer 核心层，内存管理，容器分配，数学运算模块，脚本运行时环境
* Platform Layer 平台层，操作系统，平台文件系统，Graphics API, Platform SDK

## 2.1 Resource Layer:
以特定引擎的格式统一化导入
从Resource到Asset，通过Importer转换到引擎下
通过一个reference文件数据记录关联
GUID  做为唯一识别号

* Runtime 资源管理器， 虚拟的文件系统加载和卸载Asset
* 管理所有资源的生命周期

## 2.2 Function Layer:
Tick 模拟，利用现代计算机的性能，在一帧时间做一定事件

Logic(Camera,Motor,Controller,Animation,Physics) -> Render (Render Camera, culling, rendering, postprocess, present)

这一层经常与具体的游戏混合在一起

## 2.3 Core Layer:
数学库
SIMD： 指令池，整合多个运算到一个

内存管理：
表现优化：
* 内存池
* 减少cache miss
* 内存对齐

核心：
* Put data together 数据堆放在一起
* Access Data in order 按顺序访问
* Allocate and de-allocate as a block 一次一批的申请和释放
做一套引擎的数据结构，把内存管理起来
> 关于CPU，不仅仅看其主频，缓存大小也决定了跑分，同时缓存硬件成本也更高

> 什么是图灵机？
> 图灵机是一个虚拟的机器，由数学家阿兰·图灵1936年提出来的，尽管这个机器很简单，但它可以模拟计算机的任何算法，无论这个算法有多复杂。
> 现代电子计算机的计算模型其实就是这样一种通用图灵机，它能接受一段描述其他图灵机的程序，并运行程序实现该程序所描述的算法。

## 2.4 Platform Layer
对于不同的API，不同的操作系统的适配性问题

## 2.5 Tool Layer
以开发效率优先，而不是以性能优先。 这一层代码量往往比引擎代码还要多，可以选择Python，wpf等各种语言实现。
Digital Content Creation: 引擎与各个工具软件之间的数据互通转换- Asset Conditioning Pipeline

## 总结：
分层的核心思想：
* 越往上越灵活，越往下越稳定。
* 一定是上往下调用，不能反向
> C++ 17使用了原EA寒霜引擎的定制的STL高效
> 一个引擎首先是从【CORE层】、【功能层】开始搭建

# 3. 如何构建游戏世界

## 3.1 游戏对象-GO
分类：
* 动态物
* 静态物
* 环境（天空，植被，地形系统）
* 其他的对象（空气墙）

## 3.2 组件化GO 
组件化游戏对象，将各个部件做为一个组件自由拼装
弊端：需要频繁地访问组件时的效率问题

## 3.3 LOOP
TICK能力，现在引擎逐渐转到各个系统的tick

## 3.4 通信
* 互相通信的能力，替代最原始的HARD-CODE方式，使用事件的方式

## 3.5 场景管理器
Scene management
管理着场景内的GO
* 空间上的数据管理是场景管理的核心
* 一般引擎需要支持两到三种空间的划分法

## 3.6 时序性
期望游戏中的确定性，利用一个中间层去控制管理。 或者如GO Binding之间的顺序性
