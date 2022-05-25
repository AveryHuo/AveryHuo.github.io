---
title: 安装Opencv
date: 2022-05-25 14:14:12
updated: 2022-05-25 14:14:12
top_img: false
cover: false
categories:
- 图形学
tags: 
- 图形学
description: CG笔记1
keywords: "CG, 图形学"
---

#### 一、Windows下安装opencv

1. Eigen3的安装
* 从官网下载zip
[官网下载](https://eigen.tuxfamily.org/index.php?title=Main_Page)
* 解压后，用cmake，选择x64，生成到任意的build路径即可，注意最终生成的是在INSTALL的配置项下
* 生成后的项目，一定要用管理员权限打开！！！ 
* 选择INSTALL项目，直接build即可

使用，在项目的Config的C++ -> General-> Additional Include Directories下添加安装目录下的include目录

2. Opencv的安装
下载MSVC的版本，安装到目录A
[参考文章](https://towardsdatascience.com/install-and-configure-opencv-4-2-0-in-windows-10-vc-d132c52063a1)

