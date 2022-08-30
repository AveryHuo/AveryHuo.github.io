---
title: 计算机图形学编程笔记3
cover: /img/160880489472851388.png
categories:
- 图形学
tags: 
- 图形学
katex: true
top_img: 'linear-gradient(20deg, #0062be, #925696, #cc426e, #fb0347)'
description: CG笔记3
keywords: "CG, 图形学"
date: 2022-08-12 18:31:18
updated: 2022-08-24 10:56:47
sticky: 1
---

#### 一、材质
Material == BRDF

##### 漫反射材质
假如一个物品不吸引能量，绝对白板在能量守恒的前提下，可以得出如图：
![能量守恒的渲染方程](/img/160880489472851388.png)
对半球的立体角积分就是PI。 得出BRDF如果完全不吸引时其实是1/PI

##### Glossy材质
带点镜面，带点金属
![Glossy](/img/160880489472851389.png)
![Glossy](/img/160880489472851390.png)

##### Refractive材质
带折射，传播过程中会部分吸收
![折射](/img/160880489472851391.png)

##### 反射公式推导
![推导](/img/160880489472851392.png)

##### 折射
![折射](/img/160880489472851393.png)
![折射](/img/160880489472851394.png)

全反射现象
如果入射的介质的折射率大于反射的介质折射率时，会发生全反射现象，不会折射
![全反射](/img/160880489472851395.png)

统称BSDF => BTDF(折射)+BRDF 

##### Fresnel
入射光与法线的角度决定了有多少光会被反射

当我们人眼离物体表面（玻璃，水或者桌子等）比较近时，此时我们的视线几乎与表面垂直，我们可以看见更多折射过来的光（水底的鱼，玻璃外的东西）。而当们人眼离物体表面比较远时，此时我们的视线几乎与表面平行，我们可以看见更多反射过来的光（倒影）。如图：
![Fresnel](/img/160880489472851396.png)
![Fresnel项](/img/160880489472851397.png)

通过菲涅尔效应我们不难发现，当入射光方向接近垂直表面时，大部分的能量会被折射，所以我们能看清水底的东西。而当入射光方向接近平行表面时，大部分的能量会被反射，所以我们会看见远处的倒影。
参考： https://zhuanlan.zhihu.com/p/375746359

##### 二、微表面模型
通过描述微表面的法线变化程度决定表面的粗糙
![微表面](/img/160880489472851398.png)

Fresnel+Geometry(用于修正当某些表面无法被照到)+法线分布
![微表面模型](/img/160880489472851399.png)
问题：diffuse可能会过弱，因此有许多不同的微表面模型，如cook-terrance

##### 三、区分材质
各向同性材质Isotropic(法线没什么方向性，比较均匀)
各向异性Anisotropic（法线方向性强）
![材质区分](/img/1608804894728513100.png)

从BRDF角度考虑，当旋转入射角时，BRDF值都一样，那就是各向同性。反之，就是各向异性。
即各向异性与绝对方位角有关

##### 四、BRDF 属性
1. 值永远是非负的
2. 所谓线性性质，可以分成很多部分进行独立运算再加起来
3. 可逆性，交换入射与出射的角色，得到的值一定是一样的
4. 能量守恒，BRDF 一定不会使能量变多
5. 对于各向同性，可以降低维度计算

##### 五、BRDF 测量
由于许多物理上的结果与现实并不一样，因此需要测量

普遍的实现：
```
foreach outgoing direction wo
 move light to illuminate surface with a thin beam from wo
 for each incoming direction wi
 move sensor to be at direction wi from surface
 measure incident radiance
```
优化的方案：
1.利用各向同性降维
2.通过对称性减少测量
3.选择性算法测量

著名的BRDF库： MERL BRDF Database

##### 六、高级光线传播

###### 1 unbias： 无偏估计，期望值一直为正确的结果，不管使用多少样本
* Path Tracing
* BDPT 双向Path Tracing
当光线传播在光源旁边时，较为适合。
缺点是慢，实现复杂

* Matropolis Light Transport MLT
通过Markov Chain选取新样品来估计
适合多除复杂light paths的情况
缺点： 无法预估收敛点，不能保证每块像素的收敛值是相同的，无法用于动画情况

###### 2 bias: 有偏估计 
Photon Mapping 光子映射， 有偏但是一致

处理SDS（specular-diffuse-specular）的路径情况， 处理caustics

步骤1： 从光源出发，反射折射，直到打到diffuse时，就停下
步骤2：从相机出发，反射折射，直到打到diffuse时，就停下

以上两步得到光子的集合，对于这些集合，计算Local density estimation，对于局部计算密度。
由于这个局部的值不可能与现实的密度一样，只有在面积dA足够小时，附近的光子足够多，才会得出更接近现实的值。

> caustics: 由于光线的聚焦产生不同的形状的情况 
> 在渲染里，得到的结果与正确有模糊，则是有偏的。 只要样本足够多，就可以收敛到不模糊的结果，则是一致的。
> variance噪声 和 bias模糊的 妥协

###### 3 Vertex Connection and Merging
BDPT+Photon Mapping 
对于BDPT无法merge的光点，将这些光点进行光子映射

###### 4 Instant Radiosity IR
实时辐射度
对于已经照亮的点，再次做为新的点光源继续照亮
* 1. 生成Virutal Point Light
* 2. 继续使用VPLs渲染场景
缺点： 无法处理glossy 材质 ，接缝的表面处理会有莫名光点(light sampling,对立体角采样改为对面积采样，面积*cos / 距离，因此当距离极近时，就会得到一个光点)。 


##### 七、Advanced Appearance Modeling
高级外观建模

#### 1. 非表面模型
Participating media 散射介质, FOG/CLOUD...
在行进过程中，会有被吸引(absorbed)，会被反射scattering(in / out)
大概流程，由一条光路，经历内部反射后，由光源再计算各个光路贡献
* 巧克力也是一种散射介质，只是光线进去后消失
* 头发

![Kajiya-Kay](/img/1608804894728513101.png)
![效果](/img/1608804894728513102.png)

Marschner Model:
考虑一部分反射R，也考虑穿透T。
![Marschner](/img/1608804894728513103.png)

Double Cylinder Model
双层圆柱模型： 针对头发皮层，有一层Medulla层需要再进行考虑
![Double Cylinder Model](/img/1608804894728513104.png)

Granular material 颗粒状模型
沙子

#### 2. 表面模型

Translucent Material:从某个地方进表面再从另个地方出，并在其中发生大量散射，并不是只是沿一个光线传播（区别半透明）
次表面散射： 在表面下发生散射，与BRDF区别，光线并不作用于一个点，可以从任意一个其他地方出去。
适合人物皮肤
![BSSRDF](/img/1608804894728513105.png)
![双光源的估计近似](/img/1608804894728513106.png)

https://cgelves.com/10-most-realistic-human-3d-models-that-will-wow-you/

Cloth：
把性质转换为散射介质，当成一个体积进行渲染

Detailed Appearance：复杂有细节的材质

##### 八、相机

1. 成像方式：
* 通过合成的方法：Sythesis
光栅化， 光线追踪

* 捕捉的方法：Capture
针孔相机与Lens相机，快门-控制光在多少秒进入相机。 
传感器只能记录irradiance

针孔相机-没有景深的效果

2. Field Of View 视场
一般认为35mm格式的胶片为标准,注意手机上显示的是等效的焦距
![视场](/img/1608804894728513107.png)


3. 曝光 Exposure
Exposure = time X irradiance 
记录到最后的就是能量，总时间的能量
 ![控制曝光](/img/1608804894728513108.png)

*  ISO感光
增益，简单的往上乘，以调整亮度
但同时也会造成Noisy问题

* F-Num(F-Stop) 光圈
焦距 /Lens的直径
一般为 1.4, 2,.28,4,5.6, 8, 11, 16, 22, 32

* Shutter Speed
过慢或者物体移动过快
* 产生motion blur
* 产生扭曲。（不同的位置记录的是不同时刻的光）

##### 九、Thin Lens
理想情况下，Lens出来的平行光能完全在一个焦点，但很难使用一个Lens实现，因此需要Lens组

* 1. 约定： 平行光过焦点，过焦点也是平行光
确定焦距与物距z0，相距z1之间的关系：
 ![thin lens公式](/img/1608804894728513109.png)

* 2. Circle of Confusion现象 - Defocus Blur
 ![CoC](/img/1608804894728513110.png)

* 3. Depth of Field 景深
使用，景深对应CoC比较小的一段。 （表示清晰的范围）
对于不同的深度，与Lens联系起来，推导如下：
 ![DoF](/img/1608804894728513111.png)

##### 十、Lumigraph
记录所有可能的光的方向

通常取两个平面(u,v)(s,t)，四维方程记录所有的光线
* Light Field Camera 光场照相机 由原来的irradiance -> radiance
对比普通照相机，每个像素结果记录了完整的光场信息
可以做到虚拟移动相机的位置
问题：
由于存储信息问题，分辨率会变差
为了分辨率，需要非常高成本

##### 十一、Physical Base Color
光谱可视范围：400-700之间
SPD 谱功率密度，在每个波长上的光的数量

Color
* Color is a phenomenon of human perception; it is not a 
universal property of light 
* Different wavelengths of light are not “colors”

Metamerism 同色异谱
通过调整不同的光谱使得人眼看到的颜色一样
 ![同色异谱](/img/1608804894728513112.png)
颜色匹配函数
使用调合RGB三种值来配出所有颜色

