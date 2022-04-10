---
title: UE5初入
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

## 后处理
选中Game setting以保证游戏内看到的与editor相同
* 1. 添加volumn->post processing volumn
* 2. 设置1的属性，post processing setting下的unbound可应用于全场景
* 3. 设置exposure(曝光)，选择manual模式，设置exposure compensation来补光