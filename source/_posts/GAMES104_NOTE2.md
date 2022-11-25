---
title: GAMES104-NOTE2
cover: /img/image-20221123153956216.png
date: 2022-11-24 16:56:21
updated: 2022-11-25 17:18:58
top_img: false
categories:
- 引擎
tags: 
- Engine
---

# 1.粒子系统

## 1.1 基础概念
* Emitter
发射器
* Particle System
把众多的Emitter结合到一起
> 游戏中的粒子系统的编辑核心就是如何组合Emitter

* Spawn Position
发射生成点
* Spawn Mode
生成的方式的种类，比如到达一定时机才进行Spawn发射
* Simulate
粒子在空间的行为
使用最简单的显式积分
旋转
重力和大小
一些物理特性，如落地的与地面相遇时反弹

* Billboard Particle
最古老，每个粒子都是sprite, 面向相机
如果尺寸大，建议用Animated texture，texture表面不断变化

* Mesh Particle
每个粒子都是Model， 碎片来自于爆炸

* Ribbon Particle
Particle拖出一条光带，如刀剑的拖尾的效果。
在飞行过程中会不断拉出一个个的控制点
使用Catmull-Rom 曲线，把曲线拉得更光滑

## 1.2 Rendering

* Particle Sort
Mode
1. Global的方式
对于整个System进行排序，性能消耗大
2. 通过层级
对于Per System -> Per Emitter -> Within emitter
规则：
1. 通过相机的远近来
2. 通过各自System的Bouning Box来

* Low-Resolution Particles
对于全Resolution的粒子，会导致严重的性能消耗。因此会把Resolution进行减半处理。
降低采样率

## 1.3 GPU粒子

* Processing Particle on GPU
  粒子系统的Simulate过程对于CPU的性能占用过大，放到GPU中处理。

![GPU实现粒子](/img/image-20221123153956216.png)

* 实现概述
首先做一个池子，如下
![初始状态](/img/image-20221123154056932.png)
生成粒子，终究从dead list的尾巴取数据
![生成](/img/image-20221123154215247.png)
模拟过程
![Simulate](/img/image-20221123154251635.png)
使用compute shader的原子性特征
进一步的，实现粒子的view culling的list支持，与dead与active列表区别开
![Swap](/img/image-20221123154602844.png)
* 排序
使用归并排序的思想
![GPU上的实现排序](/img/image-20221123155107096.png)
* 碰撞
![image-20221123155238906](/img/image-20221123155238906.png)

## 1.4 粒子应用
* 人群模拟
1. 把人物做成一个Mesh，使用Animated Particle Mesh，支持skeleton动画
2. 把人物的原始动画制作成 Particle Animation Texture，再在particle system实现一个简易的ASM。
3. 人物移动时的Navigation Texture，使用SDF（有正负号的DF），随着值越来越接近零，就知道是否靠近障碍物。 有了SDF算出Direction Field(Texture)，对于一个点就有了一个指引性。再结合ASM里的随机量，实现状态切换模拟真实的情况。

* 实现动作-骨骼- 破坏等变换。 Unreal例子
* 与环境感知

## 1.5 粒子设计工具链
* Preset Stack-Style Modules
如unreal的Cascade PS 
传统的有界面有参数，通过叠加module的形式制作粒子。
缺点是固定的方法和流程，添加新的需要引擎中支持，固定的粒子数据不灵活

* Graph-Based Design
参数化与可共享化的graph的设计，类似于蓝图系统的搭建

* Hybrid Design
  如Unreal的Niagara System Design(引擎中近100万行代码实现)

![Niagara System](/img/image-20221123165313926.png)

# 2.Sound System

## 2.1 音量单位
音量来自于单位面积受到的音量压强
![名词](/img/image-20221123174146135.png)

## 2.2 分贝
能感知的最小声音：一个蚊子离三米发出的声音，以此为基数，每十倍为一个台阶
![分贝](/img/image-20221123174235750.png)

## 2.3 音色
频率差不多，但多个不同的基波叠加

## 2.4 降噪
以两种波长互相抵消的方式



![人耳的识别](/img/image-20221123180030888.png)

> 能识别20-50HZ，但实际高过50HZ时，也会产生绕动音色，实际在电影行业制作时是要高于50HZ的

## 2.5 Digital Sound
把声音从无线连续的信号变成离散信号（Digital化）
* PCM 脉冲代码调试器
1. 对于波动的信号采样
2. 进行Quantizing 变成可以存储的数据
3. 进行Encoding编码

采样：
人能听见的声波的范围（20-5千HZ）。
香浓定理：对于任何频率的信号，只需要采样密度是频率的两倍，就可以表示无损。

Quantizing:
big-depth: bit depth is the number of bits of information in each sample.

Encoding:
WAV: 无损，质量好
FLAC：lossless，存储
MP3: 只支持立体声，不能支持5.1声音源（环绕音），但重要的是有专利保护。
OGG: 对比MP3，拥有多通道且没有专利保护 

![声音类型种类](/img/image-20221125164141470.png)

## 2.6 3D 声音渲染
游戏引擎中的声音难点在于如何创建一个3维的声音场。

* 3D Sound Sources
声音源

* Listener
虚拟的电话，位置，速度，方向
如TPS游戏，人物与相机的距离一般在相机和人物主角之间的某处

* Spatialization
声音的空间感
如何区分声音的远近，除了声音的大小，还有到达我左右耳的时间差距，同样的声音到达左右耳的音色变化

* Panning
当speaker有许多通道时，通过调整各个通道之间的参数（大小，音色，Latency）创建出空间感

Linear Panning
音强从左往右移动
人对声音的感知是音强的平方，当声源移到离最近的时候听起来会变小
![Linear Panning1](/img/image-20221125165154700.png)

![Linear Panning2](/img/image-20221125165317049.png)



![image-20221125165359913](/img/image-20221125165359913.png)

在游戏引擎中，更多的是处理好Steroing 两个耳朵的声音感

* Attenuation
同样的音源，对于距离不同位置时，高频与低频的衰弱会发生变化。
真实世界中，有些高频的声音离得远点就听不清，但低频声音能听得更远。
各样各样的Attenuation的声音Shape：
Sphere
Capsule- 如小溪
Box - 如房间
Cone - 如喇叭

* Obstruction and Occlusion

![Obstruction and Occlusion](/img/image-20221125170304765.png)

1. 对于重要的声源，进行声源的Ray-casting的采样。
2. 根据材质的碰撞表面的属性去决定有多少声源能量损耗或被阻挡

* Reverb 混响
与空间与材质影响特别大
1. Direct(dry) 真实的声音
2. Early reflections(echo) 回音
3. Late reverberations(tail) 尾音
不同材质对于不同波段的吸收是不一样的。无论什么时候，混音的加入是提升感受的重要因素

* The Doppler Effect
因为介质在运动过程，声波不断发生扩散，最终感受到的音就一样
应用于游戏中对于速度感和打击感的感知来源

## 2.7 Common Middlewares
fmod 维护的不太好， wwise的使用者也越来越多



