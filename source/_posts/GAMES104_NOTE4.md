---
title: GAMES104-NOTE4
cover: /img/image-20230106174810993.png
date: 2023-01-01 22:36:20
updated: 2023-02-01 22:36:20
top_img: false
categories:
- 引擎
tags: 
- Engine
---

# 1. 引擎中的GamePlay玩法
GamePlay is Everything

## 1.1 总览
• Event Mechanism
• Script System
• Visual Script
• Character, Control and Camera

GamePlay的挑战
1. 各个子系统之间的协作
2. 对于一些游戏中，可能存在各种类型玩法
3. 如何针对市场情况，做出快速迭代

## 1.2 Event Mechanism

1. Publish-subscribe Pattern
* 发送者 -> 事件注册到Dispatcher
* Dispatcher送到各个GO中
* GO返回Callback
因此需要三个组件：
组件1： Event Definition
* 这里的问题是，游戏的玩法多样性导致无法从程序层面预先定义好类型。UE的解决方案下是允许自定义类，生成可编辑的界面。
* 但另一个问题是，这样还是会需要重编译代码，对于UE来说，允许一种C++代码编译出的DLL的注入机制。

组件2：Callback Registration
预先注册一个callback函数句柄，由某个时刻被Invoke。
* 问题，生命周期的问题，callback安全性问题，在invoke原指针地址已经被回收，wild point
* 强引用的做法：callback注册在对象不可能销毁！ 这样内存可能会越来越大。。
* 弱引用的做法：对象可以被销毁，但Invoke时，进行判定！

组件3：Event Dispatching
* 立即模式，父类的函数会一直等到callback后才能继续执行
问题，多同步的情况难以处理，对于游戏环境的添加特效，如果加载的事件放成立即，则会花费大量的事件在发送事件
* 消息队列， 先放到队列中，在未来某个时间点按顺序（或优先级）执行
1. 需要解决Event序列化和反序列化的问题，利用反射的机制，将Event与内存块之间进行相互转换。
2. 进一步的优化Event的内存，用Ring Buffer的方法，通过移动指针来管理内存池。
![image-20230106174810993](/img/image-20230106174810993.png)

3. 消息队列进行分类， 对于复杂的Event来说，做出多个Dispatcher，多个Queue。如Net Event Queue, Combat Event Queue等，加强处理效率，也更易维护。
4. 问题1， 队列无法保存顺序问题
5. 问题2， 时效性问题，需要至少等一帧，无法立即处理。 如对于ACT游戏来说，实时性要求较高的情况。

> Event不建议添加优先级机制，这会导致耦合度的增加，同时也不符合dispatcher的优势，更难以处理并行化的设计。设置了优先级就会包含了大量的假设，也加大了与dispatcher的耦合度。

## 1.3 Game Logic的语言

* 编译型语言构建游戏逻辑
问题1： 更新迭代困难，每次修改都要重编
问题2： 使用门槛高，设计（非开发）人员几乎无法参加
* 脚本语言，解释型语言
在一个虚拟机的环境中运行
![image-20230109104104021](/img/image-20230109104104021.png)

* 脚本管理系统
方案一： Native语言控制游戏主世界，拥有更高的性能。
方案二： 使用脚本语言控制
实际情况下，在重度脚本依赖的游戏中，GO的创建管理多数在于脚本中，因为游戏逻辑中GO的使用控制是相对更多的，而脚本主控的也是游戏逻辑部分，编译型语言则是提供基础功能的接口。

> 脚本语言的缺点是慢，但借助JIT（just-in-time），一边运行一边编译，以此种方式优化整个性能，甚至可以超过编译语言。
> 魔兽世界- 使用LUA

## 1.4 Visual Scripting
可视化编程语言
> 引擎的本质是生产力工具

* 将整个脚本语言转为可视化的过程
* 难点：主要还是团队协作的问题，这里有规范性的问题，debugger机制，手动整理过程低效耗时
* 本质上，就是可视化的脚本，需要能与脚本之间互相转换，但与脚本并不是一个替代关系。而更好的是一个互补的情况

## 1.5 3C系统
Character, Control & Camera
形成了游戏的体验的核心
* Character: 首先就是Movement，对于3A游戏来说，移动会有很多的细节。 其次是与环境的互动。一般来说由 状态机来实现。
* Control: 针对不同的设备的Input做出不同的对应响应，同时也需要反馈机制，另外对于一些ACT游戏，还需要设计不同的按键组合，这里有Chords，同时按下某些键，触发一个独特的行为，有Key Sequences，保留一段玩家的操作记录，以触发一个游戏行为。
> 多数的FPS游戏都配有一个吸咐系统，如果不做吸咐的话，由于操作的延迟可能会有100MS+，导致难以操作。

* Camera: 当角色在跑动走动时，相机也会随着发生变化。非常重要的一方面，根据生物学的原理，让相机表达出更好的主观感受。

# 2. AI

## 2.1 Outline
AI Basic
• Navigation
• Steering
• Crowd Simulation
• Sensing
• Classic Decision Making Algorithms
Advanced AI
• Planning and Goals
• Machine Learning

## 2.2 Navigation
导航系统分为 Map representation -> Path finding -> Path smoothing

### 2.2.1 Map representation - Walkable Area
确定所有可以去的区域
表达Walkable Area的格式：
1. Waypoint Network 路点网络
2. Grid
3. Navigation Mesh 
4. Sparse Voxel Octree 空间八叉树
有些情况需要在游戏中使用多种格式

* Waypoint Network
1. 找最近的点。Find the nearest points to get on and off the network
2. Plan the path on the waypoint network
实现容易，但限制性较多，路点选择需要手动介入

* Grid
统一标准划分，统一的格子形状。
实现容易，更易于更新，统一的数据格式。缺点是存储空间造成浪费，在Grid中移动时，可能会造成较严重的cache miss，另外实现桥路和地下叠加路线较为复杂，像素的精准度问题。

* Navigation Mesh
解决重叠路面问题，对比waypoint，这里使用的是面覆盖的方式，且支持3D walkable surface。更加精准，更快的寻路，动态性更好。但生成较为复杂，对于3维空间来说无法处理
使用Polygon，且必须得是凸Polygon(Convex Polygon)，而不是凹Polygon(Concave Polygon)。
原因：
1. Pathfinding generates a series of polygon
(Polygon Corridor) need to walk through，寻路形成一系列的多边形走廊，可能出现在多边形之外。
2. Convexity guarantees the final path is limited in
the polygon and two adjacent polygons have only
one common edge (Portal)。 两两个多边形之间仅有一个共享的边

* Sparse Voxel Octree
对于空战游戏，就可以使用八叉树的分类方式处理3维空间。问题是存储的空间要求较高，寻路较为困难
![image-20230110113200418](/img/image-20230110113200418.png)

### 2.2.2 Pathfinding
所谓寻路的目标，1是找到一条可通达的道路，2是尽可能的找到相对近的路。
* 广度优先算法
  较费时

* 深度优先算法
  较费时

* Dijkstra 
每次遍历所有相邻的未访问过的点，找出与旧的点距离最短的点，直到找终点
![image-20230110114014623](/img/image-20230110114014623.png)

* A星
  基本基于Dijkstra的思路，额外加入一个新的启发函数，cost等于source+启发
这里的启发函数可以理解为方向，如两点之间的直线距离，任意路径点与此直线距离的得到最终的cost.
![image-20230110114632885](/img/image-20230110114632885.png)

Grid的启发算法：

![image-20230110115227819](/img/image-20230110115227819.png)


NavMesh的A星启发算法：
1. 一般使用边线的中点
![image-20230110115108325](/img/image-20230110115108325.png)

2. 计算欧拉距离
![image-20230110115404018](/img/image-20230110115404018.png)

Heuristic的行为：
h(n) 过低，更慢，但容易找到最短路径，过高，更快点达到终点

### 2.2.3 Path smoothing
让AI走得更真实更自然

* Funnel Algorithm
类似于人走路的算法实现，先从一个点看向通道，找出相邻边的多边形，再判断是否与能完全包裹多边形，是则往下个多边形减少范围。 否则找到与下个多边形最近的边来减少范围查找。
![image-20230110163319224](/img/image-20230110163319224.png)

![image-20230110163352132](/img/image-20230110163352132.png)

### 2.2.4 NavMesh的生成
* Voxelization  体素化自动生成NavMesh
> 库Raycast: 先让世界进行体素化生成各个Voxel，标记出能通行的区域，通过相邻的Voxel不能相差的方式找出。 再从所有的walkable voxel中找出所有的Edge，再按这些的Edge生成Distance Field 图，每个voxel找最近的edge，离edge的点最远的点找出，再从这个点向外扩散，以此形成 Distance Field，即距离场。更细节的处理，比如重叠的区域需要做剔除。

* Region Segmentation

  ![image-20230118114737725](/img/image-20230118114737725.png)

  ![image-20230118114746362](/img/image-20230118114746362.png)

  ![image-20230118114755560](/img/image-20230118114755560.png)

* Mesh生成
  通过 Region Segmentation生成 Mesh

  ![image-20230118114847714](/img/image-20230118114847714.png)

### 2.2.5 NavMesh的特性
* 为不同的地形标记NavMesh
如水面，地面，沙面等，对不同的地形发送事件以做不同的游戏逻辑处理

* Tile 
对于场景物体来说，运用NavMesh的特性，生成不同的Tile，而不是完全更新NavMesh

* Off-mesh Link
允许在不同的地形之间的特殊行为。 因为在基础的NavMesh不足的情况，需要手动建立不同地形间的连接线，实现地形间的穿梭

## 2.3 Steering
转向系统
分为三种行为：
* 1. Seek Flee 目标转向  追寻一个目标的运动
追踪与巡逻。 输入：自己位置与目标位置  输出：加速度
* 2. VelocityMatch 速度转向
追上目标的速度，当目标是静止和匀速时，较为容易，可由加速度公式求出，但如果目标的速度是不定时，需要在第一帧进行动态计算
输入： 自己速度，目标速度，匹配时间    输出：加速度
* 3. Align  角度转向
与2类似，只是这里处理的是角速度的匹配。
输入：自己的角度，目标角度   输出：角加速度 

## 2.4 Crowd Simulation
群体（行为）模拟

### 2.4.1 模拟方法
* 1. Microscopic Models - Rule-based Models  微观方法
预先为群体动态的个体制定一系列的规则来运动
* 2. Macroscopic Models 宏观方法
宏观上设计全局的LINE，让群体是沿着LINE行走和运动，但不考虑个体之间和与环境之间的关联
* 3. Mesoscopic Models
混合模式
群体分组，个体可以按1的Role，整体就有一个LINE的规则，如RTS游戏控制小兵。

### 2.4.2 碰撞避免
Collision Avoidance
* Force-based Models
影响人群行为的社会心理和物理力量的混合， 个人的实际运动取决于所期望的速度及其与环境有关相互作用， 且可以模拟逃离人群恐慌的动态特征
优点：适合人群模拟    缺点：与物理模拟类似，需要控制好模拟的步伐，以防模拟出错的情况

* Velocity-base Models
基于速度障碍生成的碰撞检测
当两个物体要相遇时，会在速度域形成一个障碍，以让各自进行速度调整来避让碰撞。
根据周边物体的信息，在速度域上做出决定。
算法分类：
1. Velocity Obstacle (VO)
计算它自己的躲避速度，假设其他座席无响应
适用于静态和无响应的障碍
容易跑过头
可能会引起两个互相避让物体之间的振荡

2. Reciprocal Velocity Obstacle (RVO)
假设另一方正在使用相同的决策过程(相互合作)
双方都只走一半避免的碰撞的路
仅保证两个物体间的无振荡和碰撞避免的情况

3. Optimal Reciprocal Collision Avoidance (ORCA)
在2的基础上解决了群体的无振荡和碰撞避免的情况

## 2.5 Sensing or Perception
感知系统

### 2.5.1 分类
内部信息+ 外部信息（静态空间信息，动态空间信息，角色信息）
* 内部信息
自身的信息，位置，血量，武器状态等
* 静态空间信息
放置tactical（战略）点，让AI知道某些点可以做为更优的选择
* 动态空间信息
Influence Map + Sight Area（视角区域）
动态获取当前的游戏的信息或游戏行为变动或事件发出，以影响AI在战场上的行为。
Game Objects
动态获取场景物体的行为来影响 AI。

### 2.5.2 Sensing 模拟
1.空间中的光，声音， 气味
2.最大行驶距离
3.以不同的模式在空间和时间上衰减
视线被障碍物挡住
嗅觉范围会随着时间的推移而缩小
4.辐射场可以模拟传感信号
可以简化为影响图
该字段覆盖的代理可以感知信息

> Sensing需要在引擎中设置开放的级别，以此控制对于性能方向的考虑和控制


## 2.6 Classic Decision Making Algorithms
### 2.6.1 分类
六大算法：
前向算法
• Finite State Machine
• Behavior Tree

• Hierarchical Tasks Network
• Goal Oriented Action Planning
• Monte Carlo Tree Search
• Deep Learning

### 2.6.2 Finite State Machine
状态机，两个状态通过一定的条件进行切换状态。
Transition + State+ Conditions
State过多时，整个网络的复杂度会比较复杂。 
可以使用Hierachy FSM做为优化，但反应速度较慢，交互也会有问题。

整体来说：
维护复杂，更新修改State难，重用性较差。

### 2.6.3 Behavior Tree
Decision Tree 决策树
用行为树来模拟出人类的思想决策
* Execution Nodes
叶子结点，也是行为结点，处理一个单位的行为。拥有Fail, Success, Running三种状态
* Control Nodes
条件结点， 通过返回结果去决定后面的流程的走向
Sequence： 从左往右（从上往下）依次执行子树，直达有结点返回Fail或Running, 返回，或者当所有的结点都成功，则返回成功
Select: 从左往右（从上往下）依次执行子树，直达有结点返回Success或Running, 立即终止并返回，或者当所有的结点都失败，则返回失败
Parallel: 逻辑上同时开始执行所有的子树，只要有任意M个子树执行成功，则返回成功，有N-M+1个结点失败则失败。 其他则返回Running

![image-20230118153654707](/img/image-20230118153654707.png)

* 如何去Tick?
要想人思考一样，每次从root结点去Tick， 每层的树结点按固定的顺序去执行，每个结点都要有固定的返回。 
> 从头Tick的可能会导致性能问题，这里的优化的方法可以是去以某些激活结点去执行，同时添加一些事件去让BT从头执行。但这只是一种变体且需要明确约定好规则和设计。
> 同时Running的结点可能有多个。

* 优化- Decorator
对于一个结点执行固定的几类动作， 如•循环执行 •执行一次 •计时器 •时间限制 •值修改器几种

* Precondition
把条件合并到结点内，以简化BT的结构

* Blackboard
BT的内存区，用K-V去存储数据，让行为树的结点去存取数据。

* BT的缺点
每个TICK都从头就会有性能问题。交互条件越多就越多的消耗。











