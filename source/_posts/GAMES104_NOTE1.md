---
title: GAMES104-NOTE1
cover: /img/1608804894728513117.png
date: 2022-10-19 17:54:05
updated: 2022-10-25 18:16:13
top_img: false
categories:
- 引擎
tags: 
- Engine
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

# 4.游戏引擎中的渲染实践

帧率的参考： >30帧， 实时。 10帧，可交互。 <10 offline rendering
挑战：
1. 同时处理的物体对象和类型，实现的效果的复杂性
2. 需要对于现在计算机硬件有一定的认知
3. 更高的帧率要求，更高的显示分辨率
4. 硬件环境对于游戏开发的限制

![GAMES104的渲染课程分类](/img/1608804894728513117.png)

## 4.1 SIMD与SIMT
SIMD Single Instruction Multiple Data  单指令同时在多个数据点时执行相同运算
SIMT 更多的拥有SIMD的核，进行并行计算
> C++ sse扩展宏
![SIMD与SIMT](/img/1608804894728513118.png)

## 4.2 GPU架构
![约十年前的N卡的现代GPU框架](/img/1608804894728513119.png)
冯-诺依曼架构，把计算和数据分开，但这里的问题是找数据的过程会有性能的问题
![数据传递](/img/1608804894728513120.png)
* 尽可能单向传输，从CPU转到GPU，而不要从GPU中读数据
* 缓存效率问题，提高达到更多的cache hit

## 4.3 GPU限制
* 内存的限制
* ALU的限制（数据计算）
* TMU的限制Texture Mapping Unit
* BW的限制Bandwidth

> 问题：为什么每个顶点都需要一个法线数据呢？ 
> 如果以面为顶点找法线，大部分情况是对的，但对于面是折面（如Cube）时，同样的顶点的法线可能完全不同

## 4.4 Submesh的概念
对于一个大的Mesh数据，通过取其中的数据，组合成各个小的submesh
* 但对于大量的submesh，可能会出现重复而导致内存浪费，这时需要使用一个Resource Pool 对于其进行管理。

## 4.5 GPU Batch Rendering
尽可能把绘制运算交给GPU，将相同的物体绘制一次批次传递给GPU，以加速渲染

## 4.6 PVS(Potential Visibility Set)
PVS的思想是基于多个Portal的结果，在某个位置上计算出最多能看到的地方结果，因此只需要渲染此范围内的物体
优势：
* BSP/Octree
* 更加的灵活 
* 预加载资源基于PVS

## 4.7 GPU Culling
将BVH数据完全丢给GPU，返回Occlusion的数据。
Early-Z技术，先由GPU提前画一次深度图，在正式渲染时把看不到物体直接不渲染

## 4.8 纹理压缩
Block Compression：
分块后，取最亮最暗值，以及像素权重（可由距离决定），来存储数据
PC: DXTC算法
Mobile: ASTC,不再是严格4x4分块

## 4.9 Cluster-Based Mesh pipeline
![现代mesh的生成方式对比](/img/1608804894728513121.png)

由一个单独的GPU算法过程把mesh生成为众多的小mesh，通过分成很多很多mesh，交由GPU处理
![Cluster-Based Mesh pipeline](/img/1608804894728513122.png)


# 5.渲染中的光和材质

## 5.1 理论基础
渲染方程
![渲染方程](/img/1608804894728513123.png)
挑战：
* 1. visiblity to light的问题，一块区域是否有光的问题？ 最熟悉的解释方式就是shadow， irradiance的计算问题
  > radiance 辐射度， 黑体辐射的逻辑，一个光在物体反射出去的能量叫radiance。 irradiance 为incoming radiance，表示入射的能量。
* 2. 如何做shading?  渲染方程的积分怎么做？
* 3. 光的反复弹射

## 5.2 简化的解决方案：主光源与环境光
对于ambient light的模拟，结合环境贴图，根据视角方向的角度，根据表面的法线向量进行反射，在cubemap中找到那个点。

## 5.3 Blin-Phong模型
体现光的可叠加原理： Ambient + Diffuse + Specular
所有的光不管来自什么地方，最后都可以线性叠加在一起。

![Blin-Phong](/img/1608804894728513124.png)

问题：
* 1. 能量不守恒
* 2. 与真实世界偏差较大，塑料感强

## 5.4 ShadowMap
算法流程：由光源渲染场景，得到相机到光这个点的距离，去做正面的相机位置渲染的时候，每一个点我通过反向投影，把你投影到那个光源视角的Projection的位置，我也可以得到一个距离，如果这个距离大于最近遮挡物的距离的话，那就在Shadow中；如果等于或者小于的话，就不在Shadow中

![总结](/img/1608804894728513125.png)

## 5.5 Spherical Harmonics

## 5.6 LightMap
把整个场景的光照预先算好烘焙到一张图上

利用5.5 进行几何的简化，要在参数空间进行分配，我们尽可能希望在同样的这个面积或者体积里面，给到的这个Texture Resolution（Texture的精度）
生成UV Atlas, Lightmap density

缺点是
* 非常长的预计算的时间
* 其次它只能处理静态的物体和静态的光，当你的物体一旦变了、光源动了，以前烘焙的内容就全部完蛋了，但是动态物体确实是有办法Hack的，在做一些简单物体的时候，可以从周围去Sampling一个点上的Lightmap，就可以猜到环境光长什么样子，这时候我给他一个光照等等
* 第三个缺点是既然这是一个空间换时间的策略，那么Lightmap本身占用几十兆到100兆左右的存储空间，这取决于场景的大小

## 5.7 LightProbe
算法极其困难，这里来个简单粗暴的，在空间上撒一堆的采样点：Light Probe，每个点上的光照就是一个半球、一个Probe，那就放置一堆Light Probe
现代游戏一般采用自动化生成，对空间的几何

## 5.8 ReflectionProbe
Light Probe采样的时候一般我们会采样的比较密，我们可能会用到一些压缩算法，比如说把精度压得非常的低，因为我们只要用它来做光照的话，光照如果只做Diffuse的话其实可以非常的低频，这个地方用Spherical Harmonics压缩也没太大的问题，但是游戏中会有很多光亮的东西，它走在这样的环境中，反射的内容会经常发生变化，所以有时候我们会专门做一种Probe：Reflection Probe

## 5.9 Probe 总结：
把【Light Probes（处理动态）】和【Reflection Probes（处理静态）】放在一起的话，就能够实现一个还很不错的GI的效果
* Runtime首先也是非常快的
* 它能够处理静态物体和动态物体
* 其实是可以在Runtime时候可以更新，如果这个场景发生了变化，人物发生位置上变化，实际上现代计算机上Light Probe是可以Runtime更新的，这其中有一个细节，我要去做Light Probe需要放一个相机，向上下左右观察，把周围拍6张照片，拼成一个图，拿到这个图之后，我再用我快速的GPU Shader对它继续各种处理，速度也会非常的快
  
缺点呢就是比不上Lightmap，因为他能给你场景中动的物体，非常好的光照感，环境也有这种感觉，但是环境无法像Lightmap那种非常软阴影的感觉、物体之间交叠的感觉，包括一些非常漂亮的Color的效果做的也不是特别的好，这就是因为你的采样太稀疏了，Lightmap在地图上要采样几百万个点，Light Probe几万个不得了了，所以其实Light Probe是Lightmap几百分之一的采样率肯定是达不到人家的效果的。

## 5.10 BRDF模型
GGX模型，光打到物体表面的两件问题：
* 1. 模型表面将光弹射了回去，至于能弹射多少取决于模型，表面的这个法向的分布，就是Roughness这个粗糙度，如果法线比较散乱，那么彼此之间就是发散，可以看到高光很发散。这部分是Specular
* 2. 但是还有一些光会射进物体里面，如果是金属，金属的电子可以捕获这些光子，那些电子就会将光子笑纳；如果是非金属，电子就没有能力捕获这些光子，这些光子就会在内部来回弹，以一个随机的方向射出，相当于一束光，射到物体表面，在其中发生了几次折射之后，全部散出去。这部分是什么呢？就是Diffuse
![BRDF模型](/img/1608804894728513126.png)

* 漫反射 diffuse的部分，这部分非常简单，如果你把球面上所有的漫反射的部分积分，积分起来的话，就是一个PI分之C，C取决于你的这个多少部分的能量传入进来（计算导出的话需要微积分的知识）
* 反射 specular的部分，引入了著名的【CookTorrance模型】，【CookTorrance模型】的数学公式看起来就很漂亮，有著名的三项：DFG，每个字母代表了一种光学现象

CookTorrance模型- D项：
![D](/img/1608804894728513127.png)
```C
// GGX / Trowbridge-Reitz
// [Walter et al. 2007, "Microfacet models for refraction through rough surfaces"]
float D_GGX( float Roughness, float NoH )
{
	float m = Roughness * Roughness;
	float m2 = m * m;
	float d = ( NoH * m2 - NoH ) * NoH + 1;	// 2 mad
	return m2 / ( PI*d*d );					// 2 mul, 1 rcp
}
```
引入了Roughness，表达了你的法向分布的随机度，Roughness越高，随机性越强；Roughness越低，随机性越弱，就越聚集，像一个镜子，有了随机度就可以得出另外一个部分

CookTorrance模型- G项：
Geometric attenuation term（Self-Shadowing），微表面几何内部的内遮挡
![G](/img/1608804894728513128.png)

比如说一个光100%能量射进来，根据Normal Distribution Function、就是模型的Roughness，我知道有比如30%的光被遮挡了，那我知道剩下的是70%，这些光是无数的光子，开始往我眼睛里去跑的时候，因为这个分布是各项同性Isotopic，又有70%中的30%被干掉了，所以最后流到眼睛中的是49%的光，就是这个原理。公式巧妙的地方在于，我们在计算Normal Distribution Function的时候引入变量a的时候，又完美的直接用在了G项中，就只需要设置一个参数Roughness，就可以得到两个结果

```C
// Smith term for GGX
// [Smith 1967, "Geometrical shadowing of a random rough surface"]
float G_Smith( float Roughness, float NoV, float NoL )
{
	float a = Square( Roughness );
	float a2 = a*a;

	float Vis_SmithV = NoV + sqrt( NoV * (NoV - NoV * a2) + a2 );
	float Vis_SmithL = NoL + sqrt( NoL * (NoL - NoL * a2) + a2 );
	return rcp( Vis_SmithV * Vis_SmithL );
}
```

CookTorrance模型- F项：
Fresnel Equation

当眼睛非常接近表面的切线方向的时候，反射系数会极具的增加，这时候就会产生倒影的效果。
![F](/img/1608804894728513129.png)

```C
float3 F_None( float3 SpecularColor )
{
	return SpecularColor;
}

// [Schlick 1994, "An Inexpensive BRDF Model for Physically-Based Rendering"]
// [Lagarde 2012, "Spherical Gaussian approximation for Blinn-Phong, Phong and Fresnel"]
float3 F_Schlick( float3 SpecularColor, float VoH )
{
	// Anything less than 2% is physically impossible and is instead considered to be shadowing 
	return SpecularColor + ( saturate( 50.0 * SpecularColor.g ) - SpecularColor ) * exp2( (-5.55473 * VoH - 6.98316) * VoH );

	//float Fc = exp2( (-5.55473 * VoH - 6.98316) * VoH );	// 1 mad, 1 mul, 1 exp 	//float Fc = pow( 1 - VoH, 5 );
	//return Fc + (1 - Fc) * SpecularColor;					// 1 add, 3 mad
}

float F_SchlickGray(float SpecularColor, float VoH)
{
	// Anything less than 2% is physically impossible and is instead considered to be shadowing 
	return SpecularColor + (1 - SpecularColor) * exp2( (-5.55473 * VoH - 6.98316) * VoH );

	//float Fc = exp2( (-5.55473 * VoH - 6.98316) * VoH );	// 1 mad, 1 mul, 1 exp 	//float Fc = pow( 1 - VoH, 5 );
	//return Fc + (1 - Fc) * SpecularColor;					// 1 add, 3 mad
}

float3 F_Fresnel( float3 SpecularColor, float VoH )
{
	float3 SpecularColorSqrt = sqrt( clamp( SpecularColor, float3(0, 0, 0), float3(0.99, 0.99, 0.99) ) );
	float3 n = ( 1 + SpecularColorSqrt ) / ( 1 - SpecularColorSqrt );
	float3 g = sqrt( n*n + VoH*VoH - 1 );
	return 0.5 * Square( (g - VoH) / (g + VoH) ) * ( 1 + Square( ((g+VoH)*VoH - 1) / ((g-VoH)*VoH + 1) ) );
}
```

所以大家发现【CookTorrance模型】这么复杂的一个反射方程，实际上只要用

* Roughness一个参数
* 再加上一个Fresnel参数（F0）

## 5.11 Disney 信条
![Disney 信条](/img/1608804894728513130.png)

* Specular Glossiness 模型
几乎没有什么参数，所有属性都用图来表达
![SG模型](/img/1608804894728513131.png)

太灵活了特别是Specualr的RGB通道，美术一旦设置不好，就会导致Fresnel项炸掉，那项叫F0，那一项一旦炸掉材质就会非常奇怪，所以在工业界，后来想到了一个“土法炼钢”，叫做【Metallic Roughness】

* Metallic Roughness 模型
![MR模型](/img/1608804894728513132.png)
可以理解为【Metallic Rougness 模型】是在【Specular Glossiness 模型】外面包了的一层，类似写了一个通用函数，但是通用函数很多人会用错，用不好会把整个操作系统搞炸掉，那在外部再包装一层小白用户指南，只允许几个开关，开关变少之后，但是会保证所有的参数都是有意思的，这样我的系统就不会炸掉，MR模型的核心思想就是这个

其中有一个Lerp函数，就是根据Metallic的数值：

* 如果是非金属的话，就把它直接锁死，那个数值很低大约是在0.02~0.3之间，Specular只能这么多
* 但是如果是金属的话，就逐渐的从BaseColor里把这个数值取出来
美术方面虽然灵活度下降了，但是它不容易出错，所以在行业实践中，很多会倾向【MR材质】而不是【SG】，这也是Disney 信条了不起的地方，当你管理上百人的团队制作游戏的时候，可控性反而是非常重要的，所以学习时，应先学习【SG模型】，再学习【MR模型】，这两个模型，基本上够用了，Unity和UE也是这么实现的

> 坏处，当你在非金属和金属之间过渡的时候，会容易产生一个小小的白边，这个可能注意不到。MR模型总体来说更加符合直觉，也不容易出错，这就是PBR的材质模型的介绍，下面有MR模型与SG模型的优缺点介绍

![MR模型实现](/img/1608804894728513133.png)

## 5.12 IBL (image-based Lighting)
* IBL最核心的想法是什么呢？
如果我能够对这个真实的这个环境的光照，做一些提前的预处理的话，是不是就可以快速的把它整个环境对我的光照，和我的这个材质的卷积运算，直接计算出来

IBL的思想，这个材质思想也很简单，就是看我们的这个材质模型，就两部分组成：Diffuse + Specular.
Diffuse部分观察起来非常简单，就是Cos函数在球面的分布。对于任何一个比如说法向的朝向点，给定一个光照的时候，可以计算出这个面，和这个球面上所有的点，进行积分之后，用Cos Loop进行积分之后，它的值是可以提前计算好的，就可以提前计算好一个叫做Diffuse的这个的卷积的结果，这个图叫做Diffuse Irradiance Map，当我知道了环境上这样一个漂亮的一个光照的时候，我知道它的Diffuse部分，无论这个表面上的法向怎么转，比如说以身上衣服为例，一条光照射过去，选择一个方向去采样Diffuse Irradiance Map我就知道和整个光场卷积的结果是什么

* Diffuse Irradiance Map
![Diffuse Irradiance Map](/img/1608804894728513134.png)
这个思路也是空间换时间，先计算好了卷积结果，记住就可以了。之所以重要是因为空间中的光场采样，比如说采样一个32x32，也就是几万个点，卷积计算用硬件加速是非常快的，但是当我去渲染这个游戏引擎画面的时候，实际上屏幕上是几百万甚至上千万的像素，而且每一帧都要做，每秒要做30次这样的运算，运算量非常大，所以这样的话，这部分计算如果用一张小的计算Texture，其实是预先计算好的，可以理解为一张计算表，查表就可以知道它的卷积的结果的话，速度将会快很多，这就是IBL最简单的思想


* Specular是非常复杂的，推导过程中，对Specular的解决方法做了大量的假设，本质上是三个方程乘法的积分，它变成了三个独立的方程的积分的乘法，最核心的想法是我们把Specular的东西进行沿着自己朝向积分，但是有一个变量Roughness，不同的粗糙度计算出来的结果不是不一样的吗，它有一个巧妙的方法就是利用硬件上的Cubemap中的Mipmap的功能，他把不同粗糙度的结果，存到了这个Mipmap的不同层级，即如下图右侧。这个是非常有道理的，相当于在三维空间中去查这个数据，第二个是，粗糙度越是高，对光照的敏感度也就越低，他就是越低频的数据，就可以放置到Mip的最低级（注意这里的Mip不是Mipmap二合一合出来的，真的是每一层都要单独计算出来的），而且实际上是一个速算表，Roughness从0到1的时候，就可以在里面迅速的去检查
![Specular](/img/1608804894728513135.png)
![Specular](/img/1608804894728513136.png)


还有一个值，学名叫做Look Up Table（LUT），LUT有两个维度，一个还是Roughness往里面放置，另一个是斜角Cos角与环境的关系
![Specular约等于LUT](/img/1608804894728513137.png)

> 利用这两个数值合在一起，就会发现它的Fresnel项变成了一个线性项，就能够基本上模拟【CookTorrance】这样一个在环境光照下的效果，所以这个IBL对Specular的解决，做了大量的假设之后给了一个近似的解，优点在于
这种近似让我们能够在这个环境光照中，看到一些高光的内容，注意这里的高光不是非常Shiny的高光，那种其实用Cubemap就能够解决，它是真的让人感觉这个地方好像有一点光亮，但又不完全光亮，并且能够模糊的让人感觉那边有内容
![总结](/img/1608804894728513138.png)

## 5.13 经典Shader解决方案
* Cascade Shadow Mapping(CSM)
shadow map的精度问题对于宽阔的场景来说非常头疼。因此对于shadow进行分层。
远处的Shadow就算有一个边界的话，投影到你的眼睛的话，相对来讲实际上也并不是特别的大，近大远小，远处的位置眼睛采样率也会下降的，从光的方向的采样率也下降了，两个部分就完美的配合在一起了，这就是【Cascade Shadow】一个简单的想法

> Cascade Shadow有一个经典的挑战就是在不同的层级之间，要做插值否则回出现一条非常硬的边界，如果这里不做任何事当你相机移动的时候，有个固定位置Shadow会破掉，具体的处理都是Shader中的Hack，所以当认真写这些算法的时候一定要认真的研究几个不同的方法和套路
> Cascade Shadow的问题呢就是以【空间换时间】，存储空间是挺大的，另外就是说要生成远处的Shadow，相当于将整个场景绘制了一遍，那个时候你要画大量的东西，成本不低，Shadow Rendering其实是游戏引擎里最贵的独立的一派，他并不是你真正绘制的那种精致材质的组成部分，它只是确保光的可见性是正确的，但是如果我们绘制假设是30ms的话，Shadow很多时候会吃掉4ms，所以Shadow是非常expensive的，要绘制四次，对场景做四次的这个裁剪，因为你在绘制那个最密集的Shadow的时候，你并不希望它画很多东西，其实你要重新计算一次Visibility，再去计算，这其中就有一堆的问题在其中

* 软阴影
  1. PCF：Percentage Closer Filter，使用滤波的方法， 实战中使用PCSS(Percentage Closer Soft Shadow)， 很大程度缓解了Shadow的这个Alias。
  2. Variance Soft Shadow map, 用平均的深度（一次方二次方）算出方差，近似得出深度的分布

## 5.14 总结：
AAA级游戏的渲染引擎（5-10年前）：
Lightmap + Lightprobe
PBR+IBL
Cascade shadow + VSSM

## 5.15 前沿技术：
随着硬件的飞速进步，实际上几乎是彻底颠覆了渲染的底层方法和逻辑，因为它把整个底层的计算全部开放出来了
1. 实时光追： 解决的问题不至Specular、ReTracing，实际上会彻底改变我们的光照体系：Real-Time Global Illumination，Lumen效果其实就是硬件的效果解放了出来
* 最高效的ScreenSpace GI，在屏幕空间快速的形成GI
* 包括基于有效距离厂的SDF做的GI
* 包括把这个世界分成各个Voxel，最著名的就是SVOGI、VXGI
* Reflective Shadow Map、RTX GI
  
2. 复杂的材质渲染
BSSRDF, BSDF(Stand-based hair)
Geometry Shader技术的发达，可以迅速的生成无数的细节，光影效果会做的非常复杂，3S材质可以用这种强大的算力，可以模拟光在材质里的Reflection的一些数学结果

3. Virtual Shadow Maps
  传统的【Cascade Shadow】挺好用的，UE5提出了Virtual ShadowMap，之前John Carmack大神提出过【Virtual Texture】，把游戏环境中所有要用到的纹理，全部Pack到一张巨大无比的纹理上去，这个纹理就叫做Virtual Texture，要使用的时候就把他调出来使用，不用的时候就把这些Texture卸载/Offload掉

## 5.16 Uber Shader and Variants
对于shader的管理，为防止过多的shader文件，设置不同的分支和变体，生成shader.

Uber Shader，我们一般会使用宏定义，去把各种情况给分出来，每一种宏定义就代表了函数的一种可能的分支，之前提过GPU里面最讨厌的就是分支，因为比如说一个函数跑起来，他有一个分支的时候，就会导致它的执行的时间长短是不一致的，但是GPU采取的是SMT的架构，它希望我1P指令扔出去的时候，结束的时间最好是一致的，所以我们就会把这些所有的分支，编译成铺天盖地的Shader

> 那为什么Uber Shader是有道理的，因为你想期望的Shader，假设今天发现了一个Bug，需要改一类Shader算法的时候，如果不采取Uber Shader的方式的话，需要逐次的改它所有可能的组合，这就很可能会改错，但是用Uber Shader这种方式的话，就自动编译出了各种组合，所以它是有道理的，这些Shader都是其实是现代游戏引擎非常重要的一个方法论和概念
> 在做shader，需要考虑好平台性，编译到各个平台。