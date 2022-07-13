---
title: Git Note
date: 2019-05-13 15:01:05
updated: 2022-07-13 15:01:05
top_img: false
cover: /img/1573879504277.png
tags: 
- Git
---

# 工作流程
Rebase的工作流程：
示例：
![master分支做了更改](/img/gitpic2022071302.jpg)
![个人分支做了更改](/img/gitpic2022071303.jpg)

使用指令： git rebase 【基】 【自己的分支】
切到dev分支下：使用
git rebase master (与 git rebase master dev 等价)

使用工具：记得这里的Branch是选择PICK的分支，右侧为新的基。下图所示，是在最新的master为基，把自己不同的提交pick到顶端去
![使用Tortoise工具进行变基](/img/gitpic2022071301.jpg)

总结，用指令是更形象更直观的说明rebase后的状态，而工具相关的设计需要根据实际选择的Pick来理解。

# 公司升级方法

## 安装Git

以下网站里选择自己电脑平台，下载安装即可
https://git-scm.com/downloads
注：安装过程选择默认选项

## 安装Git工具

推荐使用乌龟工具，界面与之前的SVN近似，而且可以结合window文件系统。
https://tortoisegit.org/download/

注：安装过程选择默认选项

## 装好之后设置账号信息

![装好之后设置账号信息](/img/1573879504277.png)


## 克隆服务端的项目代码
>1.右键选择git clone. 
2.输入项目地址：http://172.16.100.8:8081/x1/client.git 

![克隆服务端的项目代码](/img/1573881914065.png)

## 切换到自己所在的分支
> 美术： art 
> 策划和程序： feature

![切换到自己所在的分支](/img/1573883470572.png)

## 【可选】用旧项目的library
>复制原SVN的UNITY目录下的library文件夹，粘贴到已经拉下来的unity目录下。这样重打开项目不用等待太多。

## 如何拉取
![如何拉取](/img/1573881886011.png)

## 如何提交
![如何提交](/img/1573880787198.png)
