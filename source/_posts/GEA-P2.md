---
title: GEA-P2
categories:
- IT阅读
tags: 
- Game
---

## (1.6) Runtime Engine Architecture

![Runtime Engine Architecture](/img/1574738644796.png)

>自底向上的顺序大概为：
>硬件层 
>驱动层
> 系统层 
>ＳＤＫ层
＞平台独立层
> 核心库
>资源库 
>　渲染，调试，物理检测，游戏平台基础
＞游戏级渲染，各上层动画机制，相机机制，ＡＩ机制
＞游戏逻辑层

### 操作系统层

分为PC与主机（游戏）系统，PC系统如windows 提供了一种线程的机制为分享硬件资源，而主机游戏一般来说则可占用所有的硬件资源，但这两者的差距在逐渐减少。

>Operating systems like Microsoft
Windows employ a time-sliced approach to sharing the hardware with multiple running programs, known as preemptive multitasking. 
>On a console, the game typically
“owns” the entire machine.
>So the gap between console and PC development is
gradually closing (for better or for worse).

###  3rd Party SDKS

> DirectX Opengl
> Havok, PhysX ODE etc.. 实现增强物理效果的SDK
> Boost++ C++标准库之一
> STL C++标准库之一
> Kynapse 游戏AI开发的中间件
> Granny, Havok Animation，处理动画骨骼等
> Euphoria， 小型的游戏开发套件：https://sourceforge.net/projects/euphoriasdk/

#### 数据结构与算法

C++ 库
1. STL : strings, data structures, stream-based I/O  
2. STLport :portable and optimized of STL
3. Boost :Powerful data structures and algorithms library
4. Loki :Powerful generic programming template library


#### 图形

>硬件图形库
> Glide  早期的3D图形SDK，针对Voodoo显卡。
> OpenGL widely used!
> DirectX Microsoft's 3D graphics SDK
> libgcm   更底层的接口针对PS3的图形硬件，OpenGL更高效处理的选择。
> Edge Naughty Dog 和Sony提供的PS3平台的库

#### 物理与碰撞

> Havok industrial-strength physics and collision engine.
> PhysX  NVIDIA
> Open Dynamics Engine.  open source

#### 角色动画

> Granny:
> In my opinion, the Granny SDK
has the best-designed and most logical animation API of any I’ve seen,
commercial or proprietary, especially its excellent handling of time

> Havok Animation
>  The line between physics and animation is becoming
increasingly blurred as characters become more and more realistic.

> Edge  PS3 from Sony

#### 生物力学角色模型 Biomechanical Character Models

>Endorphin and Euphoria. These are animation packages that produce
character motion using advanced biomechanical models of realistic human movement.
> Endorphin, is a Maya plug-in that permits animators to
run full biomechanical simulations on characters and export the resulting animations as if they had been hand animated
>Euphoria, is a real-time version of Endorphin intended
to produce physically and biomechanically accurate character motion at runtime under the influence of unpredictable forces.

> Endorphin， MAYA插件，执行动作的角色将运行一个完整的生物力学模拟同时导出动画。
> Euphoria,  在一些不可预测的因素影响下，将动作更精细的模拟表现出来。
https://space.bilibili.com/430600560/channel/detail?cid=75669


### Platform Independence Layer

>the platform independence layer ensures consistent
behavior across all hardware platforms.


### Rendering Engine
> The rendering engine is one of the largest and most complex components of
any game engine.

#### Low-Level Renderer
![Low-Level Renderer](/img/1574756479212.png)

> Graphics Device Interface
> DirectX, OpenGL

> The low-level renderer usually provides a viewport abstraction with an associated camera-to-world matrix and 3D projection parameters, such as field of view and the location of the near and far clip planes.

>  底层的渲染提供一个显示区域，关联到相机-世界和投影的参数。

#### Scene Graph / Culling Optimizations

> For very small game worlds, a simple frustum cull (i.e., removing objects
that the camera cannot “see”) is probably all that is required. For larger game
worlds, a more advanced spatial subdivision data structure might be used to
improve rendering efficiency by allowing the potentially visible set (PVS) of
objects to be determined very quickly. 

> potentially visible set (PVS)

> 理想状态下，底层渲染应该完全不关心spatial subdivision或scene graph的使用类型。 
>OGRE open source rendering engine (http://www.ogre3d.org) is a great example of this principle in action. OGRE provides a plug-and-play scene graph
architecture. Game developers can either select from a number of preimplemented scene graph designs, or they can provide a custom scene graph implementation.

### Front End
![Front End](/img/1574759871996.png)

> HUD, Heads-up Display
> 在顶层显示
> FMV, Full-Motion Video 动作完整的视频回放
This system is responsible for playing full-screen movies that have been recorded earlier.
> IGC, in-game cinematics system.  游戏内的视频，一般当玩家不可操作时显示


### Profiling and Debugging Tools
>常用
• Intel’s VTune,
• IBM’s Quantify and Purify (part of the PurifyPlus tool suite), and
• Compuware’s Bounds Checker.

>However, most game engines also incorporate a suite of custom profiling
and debugging tools. For example, they might include one or more of the
following:
>* a mechanism for manually instrumenting the code, so that specific sections of code can be timed;
>* a facility for displaying the profiling statistics on-screen while the game
is running;
>* a facility for dumping performance stats to a text file or to an Excel
spreadsheet;
>* a facility for determining how much memory is being used by the engine, and by each subsystem, including various on-screen displays;
>* the ability to dump memory usage, high water mark and leakage stats
when the game terminates and/or during gameplay;
>* tools that allow debug print statements to be peppered throughout the
code, along with an ability to turn on or off different categories of debug
output and control the level of verbosity of the output; and
>* the ability to record game events and then play them back. This is tough
to get right, but when done properly it can be a very valuable tool for
tracking down bugs.

### Collisions & Physics

Collision and physics are usually quite tightly coupled. 
>* Havok is the gold standard in the industry today. It is feature-rich and
performs well across the boards.
>* PhysX by NVIDIA is another excellent collision and dynamics engine.
It was integrated into Unreal Engine 4 and is also available for free as
a stand-alone product for PC game development. PhysX was originally
designed as the interface to Ageia’s new physics accelerator chip. The
SDK is now owned and distributed by NVIDIA, and the company has
adapted PhysX to run on its latest GPUs.

>Open source physics and collision engines are also available. Perhaps the best-known of these is the Open Dynamics Engine (ODE)
>I-Collide, V-Collide and RAPID are other popular non-commercial collision detection engines. 开发于University of North Carolina
>http://www.ode.org


### Animations
>类型：
>* sprite/texture animation,
>* rigid body hierarchy animation, 
>* skeletal animation, 骨骼动画，
>* vertex animation， 顶点动画
>* morph targets.， 拉伸变形目标

![enter description here](/img/1574826629863.png)
![enter description here](/img/1574826985515.png)

### Human Interface Devices (HID)

input from the player , 玩家的输入设备
> keyboard, mouse
> joypad
> other specialized game controllers, like steering wheels, fishing rods,
dance pads, the Wiimote, etc.  方向盘，鱼竿，跳舞板，手柄控制器等

>The HID engine component is sometimes architected to divorce the lowlevel details of the game controller(s) on a particular hardware platform from the high-level game controls.
>It sometimes also includes a system for detecting
chords (multiple buttons pressed together), sequences (buttons pressed in sequence within a certain time limit) and gestures (sequences of inputs from the
buttons, sticks, accelerometers, etc.).
> HID engine 组件通常设计为划分出低等级的游戏控制器到高级游戏操作。
> 通常也会考虑检测组合按钮等情况

### Audio

Audio engines vary greatly in sophistication.
> For DirectX platforms (PC, Xbox 360, Xbox One), Microsoft provides an excellent audio tool
suite called XACT, supported at runtime by their feature-rich XAudio2 andX3DAudio APIs. 

>Electronic Arts has developed an advanced, high-powered
audio engine internally called SoundR!OT

>In conjunction with first-party studios like Naughty Dog, Sony Computer Entertainment America (SCEA) provides a powerful 3D audio engine called Scream

### Online Multiplayer/Networking

> That said, it is usually better to design multiplayer features from day one, if you
have that luxury.
尽早设置多人在线的模式

> 从多人在线转单机版，往往较为简单
>The Quake engine is well known
for its client-on-top-of-server mode, in which a single executable, running on a
single PC, acts both as the client and the server in single-player campaigns.

### Gameplay Foundation Systems

> 用于连接low-level engine systems 与 gameplay code。为了上层游戏逻辑可以更方便使用。

![enter description here](/img/1574912330296.png)

### Game Worlds and Object Models

> 游戏内的对象：
>* static background geometry, like buildings, roads, terrain (often a special case), etc.;
>* dynamic rigid bodies, such as rocks, soda cans, chairs, etc.;
>* player characters (PC);
>* non-player characters (NPC);
>* weapons;
>* projectiles;
>* vehicles;
>* lights (which may be present in the dynamic scene at runtime, or only
used for static lighting offline);
>* cameras;


### Scripting System & Event

> Many game engines employ a scripting language in order to make development of game-specific gameplay rules and content easier and more rapid.

### Artificial Intellience Foundations

游戏的人工智能模块，一些游戏引擎已经在引入这一模块到引擎，虽然这并不是引擎模块考虑的。
Kynogon 
>A company called Kynogon developed a middleware SDK named Kynapse, which provided much of the low-level technology required to build commercially viable game AI.  This SDK provides low-level AI building blocks such as nav mesh generation, path finding, static and dynamic object avoidance, identification of vulnerabilities within a play space (e.g., an open window from which an ambush could come) and a well-defined interface between AI and animation. 

### Game-Specific Subsystems

 顶端的游戏开发层
> Practically speaking, this line is never perfectly distinct. At least
some game-specific knowledge invariably seeps down through the gameplay
foundations layer and sometimes even extends into the core of the engine
itself.


## (1.7) Tools and the asset pipeline

游戏数据层的组成：
如图：粗黑箭头， 表示源数据是怎样从工具中生成出
		细线箭头，表示不同数据资源之间的引用关系
![enter description here](/img/1574995793894.png)

### Digital Content Creation Tools

游戏资源从3D mesh到图片bitmaps再到音频之类的，都需要设计师用工具制作，而这些工具被称为DCC（Digital Content Creation）

> Maya,3d Max
> SoundForge
> Photoshop
。。。

>That said, tools must be relatively **easy to use**, and they absolutely must be reliable, if a game team is going to be able to develop a highly polished product in a timely manner.
>工具的使用需要按项目所需来决定，关键在于好用，不一定要非常完美的工具。


### The Asset Conditioning Pipeline

往往DCC生成的文件并不能直接在游戏开发中使用，原因有下：
1. DCC导出的数据，存在许多游戏开发不需要的，比如maya中会存储directed acyclic graph的场景结点，和复杂的联结的网络结构。

2. DCC文件格式加载读取很慢，而且通常格式是各个DCC专属的

>Once data has been exported from the DCC app, it often must be further
processed before being sent to the game engine. And if a game studio is shipping its game on more than one platform, the intermediate files might be processed differently for each target platform. 
DCC应用一般需要生成给游戏引擎用的文件。

>The pipeline from DCC app to game engine is sometimes called the asset
conditioning pipeline (ACP). Every game engine has this in some form.
这种途径：从DCC应用到游戏引擎通常被称为: ACP

#### 3D Model/Mesh Data

>A mesh is a complex shape composed of triangles and vertices. A mesh typically has one or more materials applied to it in order to define
visual surface properties
> MESH：由三角面和点组成的复杂的形状

> In this book, I will use the term “mesh” to refer to a single renderable shape,
and “model” to refer to a composite object that may contain multiple meshes,
plus animation data and other metadata for use by the game.

>Brush Geometry
>Brush geometry is defined as a collection of convex hulls, each of which is defined by multiple planes.Brushes are typically created and edited directly in the game world editor. This is essentially an “old school” approach to creating
renderable geometry, but it is still used in some engines.
> 笔刷型的图形，每个都由多个平面组成，通常是凹凸面的一种实现工具。
> Pros:
• fast and easy to create;
• accessible to game designers—often used to “block out” a game level for
prototyping purposes;
• can serve both as collision volumes and as renderable geometry.
>Cons:
• low-resolution;
• difficult to create complex shapes;
• cannot support articulated objects or animated characters.


#### Skeletal Animation Data

A skeletal mesh is a special kind of mesh that is bound to a skeletal hierarchy for
the purposes of articulated animation. 
>Each vertex of a skeletal mesh contains a list of indices indicating to which
joint(s) in the skeleton it is bound. A vertex usually also includes a set of joint
weights, specifying the amount of influence each joint has on the vertex.
>骨骼mesh，包含骨骼连接点信息，通常还会有点的权重和数量影响的数据

>In order to render a skeletal mesh, the game engine requires three distinct
kinds of data:
>1. the mesh itself,
>2. the skeletal hierarchy (joint names, parent-child relationships and the
base pose the skeleton was in when it was originally bound to the mesh),
and58 1. Introduction
>3. one or more animation clips, which specify how the joints should move
over time.

> Mesh与skeleton通常由DCC导出在一个文件里，当然，当有多个mesh对应一个骨骼时，骨骼通常需要单独导出，另外动画文件一般也是单独导出。有些引擎会让这三者在一个大文件里。

>An unoptimized skeletal animation is defined by a stream of 4 × 3 matrix
samples, taken at a frequency of at least 30 frames per second, for each of the
joints in a skeleton (of which there can be 500 or more for a realistic humanoid
character).
因此动画文件一般需要使用高强度的压缩方式来存储。

#### Audio Data

Audio clips are usually exported from Sound Forge or some other audio production tool in a variety of formats and at a number of different data sampling rates.

#### Particle Systems Data

Modern games make use of complex particle effects. These are authored by
artists who specialize in the creation of visual effects. Third-party tools, such
as Houdini, permit film-quality effects to be authored


### The World Editor

The game world is where everything in a game engine comes together. To my
knowledge, there are no commercially available game world editors
>* Some variant of the Radiant game editor is used by most game engines
based on Quake technology.
>* The Half-Life 2 Source engine provides a world editor called Hammer.
>* UnrealEd is the Unreal Engine’s world editor. This powerful tool also
serves as the asset manager for all data types that the engine can consume.

### The Resource Database

Every asset also carries with it a great deal of metadata. metadata with the following information:
• A unique id that identifies the animation clip at runtime.
• The name and directory path of the source Maya (.ma or .mb) file.
• The frame range—on which frame the animation begins and ends.
• Whether or not the animation is intended to loop.
• The animator’s choice of compression technique and level. (Some assets
can be highly compressed without noticeably degrading their quality,
while others require less or no compression in order to look right ingame.)

### Some Approaches to Tool Architecture

As an interesting and unique example, Unreal’s world editor and asset
manager, UnrealEd, is built right into the runtime game engine.It permits the tools to
have total access to the full range of data structures used by the engine and
avoids a common problem of having to have two representations of every
data structure—one for the runtime engine and one for the tools.
>  运行时编辑和访问游戏所有数据为开发带来便利和加速

![一些游戏的工具架构](/img/1575083811284.png)
![一些运行时可编辑的架构](/img/1575083796324.png)

####  Web-Based User Interfaces
网页基础的页面显示。这里主要指工具。
>At Naughty Dog, we use a number of web-based
UIs. Naughty Dog’s localization tool serves as the front-end portal into our
localization database. Tasker is the web-based interface used by all Naughty
Dog employees to create, manage, schedule, communicate and collaborate on
game development tasks during production. A web-based interface known
as Connector also serves as our window into the various streams of debugging
information that are emitted by the game engine at runtime.



