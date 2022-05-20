---
title: LWRP官方说明
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1578468743022.png
categories:
- Unity学习
tags: 
- Unity学习
---

## Render Pipeline 的build-in 的流程

![build-in流程](/img/1578468743022.png)

## Command Buffer说明
![Command Buffer说明](/img/1578468782581.png)

## 语法说明

>原先shader使用的cginc引入，改成Include官方的hlsl文件
>材质变量需要CBuffer块套好，这样才能使用LWRP的batcher
>可使用LWRP独有的宏声明采样器
>属性名的变更：使用Attribute替代input, 使用Varying替代v2f
>获取顶点信息的函数变更


![LWRP的shader](/img/1578469710690.png)
![单独申明的采样器](/img/1578469737158.png)
![顶点函数](/img/1578469925626.png)
![LWRP](/img/1578470183627.png)
![手写LWRP](/img/1578470217523.png)
![LWRP Batcher](/img/1578470471751.png)


## SRP Batcher
![SRP Batcher](/img/1578470502893.png)
![不支持情况](/img/1578470577651.png)