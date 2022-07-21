---
title: Git Note
date: 2022-07-13 15:02:24
updated: 2022-07-14 16:20:52
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

参考命令集：
1. 保存本地更新并rebase远端：
```
git stash clear
git stash 
git checkout develop
git checkout .
git fetch origin develop
git rebase orgin develop
git pull origin develop
git submodule update --force
git checkout work
git rebase develop
git stash pop
```
2. 把自己工作的目录推送到远端最新
```
git checkout develop
git checkout .
git pull origin develop
git checkout work
git rebase develop
git checkout develop
git merge work
git push origin develop
```

> Update to revision的操作在Git中需要使用git reset实现。 注意这时丢失非remote端的暂存区提交！ 
> 1. 继续再使用git checkout .回到准确的那个分支点。
> 2. 指针重置可以向前也可以向后，只是改变基提交点。

> Revert，会对文件级进行内容判定，可能会产生冲突。
> 如果与任意revert的点的文件判定产生冲突，则一定会生成新的提交点
> 以上两种都不会导致本地未保存的内容丢失

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
