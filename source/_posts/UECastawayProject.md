---
title: UE5 Castaway项目记录
date: 2022-07-12 16:15:27
updated: 2022-07-12 16:15:27
cover: /img/160880488888801.png
categories:
- UE
tags: 
- UE
- Note
katex: true
top_img: 'linear-gradient(20deg, #0062be, #925696, #cc426e, #fb0347)'
description: Castaway项目
keywords: "UE, 项目"
---

描述：生存类游戏
#### 一、项目环境搭建
1. 选择ThirdPerson模板创建
2. 删除无用背景地形等，保留Light Source, PostProcessVolume, SkyLight, Fog, ReflectionCapture, NetworkPlayerStart, SkySphereBlueprint, ThirdPersonCharactor.
3. 安装Landmass和water插件
4. 设置默认启动场景
5. 设置移动平台的SDK等[可选]
* 插曲：如果发现MobileStarterContent找不到，这里从根目录下复制一下即可

![项目环境:](/img/160880488888801.png)

#### 二、地编
快捷键推荐：
G隐藏Gizmos
Shift反向编辑地形
打开Landscape，创建一个地形，进入Sculpt阶段。

1. 材质：四层，Sand, Rock, Grass, Auto
2. Material Function 
3. 制作Landscape,通过Landscape添加多个Layer（最终对应实际意义上的笔刷）![ML_Landscape:](/img/160880488888802.png)
4. 添加+Water ocean

#### 三、导入自己的模型
1. Mixamo处下载模型 fbx，导入
2. 双击打开后，修复可能出现的材质问题
3. 制作Humanoid的Avator 
   ![制作avator:](/img/160880488888804.png)
4. Skeleton Tree调整为动画结构
   ![显示retargeting选项:](/img/160880488888805.png)
   ![遍历设置为translation retargeting skeleton:](/img/160880488888806.png)
   ![设置为动画缩放:](/img/160880488888807.png)
5. 生成新的动画蓝图
   ![生成新动画蓝图:](/img/160880488888808.png)
6. 将旧的Skeleton的Rig设置为Humanion
   ![设置Humanion:](/img/160880488888809.png)
7. 编辑新的角色蓝图（可以从旧的复制一个），更换MESH，更换动画蓝图，设置好位置
   ![编辑新的角色蓝图,更换MESH:](/img/160880488888810.png)
   ![更换动画蓝图:](/img/160880488888811.png)
   ![设置好位置:](/img/160880488888812.png)


#### 四、UI界面的制作 
1. 关卡的总蓝图上使用Create Widget结点
2. 设置数据绑定 - Create Binding。 添加Get函数与属性值对应起来
   
#### 五、主逻辑
1. 人物的蓝图上添加FUNCTIONS:
   HungerSetter, ThirstSetter.用于设置饥饿和饥渴。并判断小于0时，则GG
2. 关卡蓝图添加OnActorBeginOverlap，判定碰撞到的对象为人物，添加属性
3. 人物蓝图上添加 计时器 Event Tick，使用Sequence在每条线上添加Delay，扣除数值
4. 添加死亡的UI ![死亡UI:](/img/160880488888803.png)
