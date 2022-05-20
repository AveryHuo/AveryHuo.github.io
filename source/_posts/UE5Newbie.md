---
title: UE5初入
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- UE
tags: 
- UE
- Note
---
# UE5初入

## 创建初始场景
* 1. 光源
    需要天空光照，平行光源（太阳光）

* 2. 视觉效果
    天空大气，指数雾，体积云

* 3. 设置场景光（当前默认设置）
    设置平行光源与场景天空对应

## 快捷键
使用End，可以让一个物体底部定到下个物体的表面
使用鼠标结合WSADQE精细调整
使用ctrl+space打开项目内容面板，使用过滤等功能。S.M表示静态mesh
使用Engine资源，在内容面板上的settings中勾选show engine content
使用ctrl+L+移动鼠标，可以改变阳光的状态

## 后处理
选中Game setting以保证游戏内看到的与editor相同
* 1. 添加volumn->post processing volumn
* 2. 设置1的属性，post processing setting下的unbound可应用于全场景
* 3. 设置exposure(曝光)，选择manual模式，设置exposure compensation来补光

## 材质
基本四层:
Base Color
Metallic / Metal
Roughness
Normal

在内容面板Content下新建材质文件夹，新建Material。注意通常命名一般为M_前缀
材质编辑器的使用说明：
1.双击材质打开
2.右键以拖动或点击以创建一个结点， 使用alt+点击可以删除一个连线
3.快速创建1,2,3向量结点，按1/2/3再点左键即可。 快速创建UV结点，按U点左键
4.Save将自动 apply到材质 

Channel Packing技术 ：将不同的信息存储在一张图的不同通道里
*使用FlattenNormal可以改变Normal的凸起程度
*使用StaticSwitchParam。转为开关参数
> 使用右键选中的节点为Parameter转成动态参数
> 在有创建好参数的材质球（类似于Unity的shader）右键创建 材质实例,一般以MI为前缀
> 双击材质实例则可以打开此材质并编辑其参数

## Light
属性： Static 表示为静态灯光，一般用于烘焙。 Movable 表示百分百动态的灯光（类似于实时光源，过多将消耗性能）。Stationary (介于动态与静态之间，允许动态与烘焙并存)
Source radius: 反射后显示的源光源的大小，一般需要一个反射接受面才能感觉到不同。 Soft Source radius: 表明光源边缘的柔软度