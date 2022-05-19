---
title: 四元数旋转函数学习
categories:
- Unity学习
tags: 
- Unity学习
---

## LookRotation(Vector3 forward, [DefaultValue("Vector3.up")] Vector3 upwards)

理解为将Z轴正方向转到第一个”forward“参数位置，把UP正方向转到第二个’upwards‘位置

> LookRotation的含义就是，计算让Z轴对齐forward，让y轴对齐upward 所需要的旋转四元数。

## FromToRotation(Vector3 fromDirection, Vector3 toDirection)

> 从一个转向到另一个目标转向。如：
> Quaternion.LookRotation(new Vector3(1,0,0)) 等价于 Quaternion.FromToRotation(Vector3.forward, new Vector3(1,0,0));


[参考学习](https://blog.csdn.net/narutojzm1/article/details/51276433)

## AngleAxis(float angle, Vector3 axis)

> 以axis为轴，转一个角度。 

示例：如以A（0，10，0）到B（10，0，0）形成一个方向，以此方向转90。
起始位置如图：
![起始位置](/img/1578566566815.png)

转90度后如图：
![转后](/img/1578566598445.png)