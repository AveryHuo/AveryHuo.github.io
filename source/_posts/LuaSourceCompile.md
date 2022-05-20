---
title: Lua源码编译流程
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---

## 一、配置环境

示例： 新建lua文件夹，放置到环境变量的Path中


## 二、下载lua源码
https://www.lua.org/ftp/

1.下载tar文件后
2.解压：使用powershell的 tar zxf .\lua5.3.4.tar.gz文件
3.拷贝src文件到【一】的文件夹中，注：不需要makefile文件

## 三、创建VS项目工程

1.使用Visual C++ 的空项目为模板
2.Source Files中添加现有项：添加所有【二】的文件夹的h和c文件

## 四、库形式编译

1.移除项目中的luac.c文件， lua.c文件
2.改变编译环境为x64， Release模式
3.设置项目属性的 配置类型： 动态库（dll）
4.C/C++ -> 预处理器 -> 预处理定义：添加： LUA_BUILD_AS_DLL
5.生成解决方案！

得到 .lib 和.dll文件

## 五、编译生成compiler

1.删除 LUA_BUILD_AS_DLL 的定义
2.设置项目属性的 配置类型：exe
3.添加回luac.c文件， 编译得到luac.exe文件（compiler）
 
 ## 六、编译生成interpreter
 
1.清空source Files中的文件
2.仅添加lua.c文件
3.配置：在C/C++ 中的Additional Include Directories中添加 【二】的源码文件夹
4.配置： Linker中的Input, Additional Dependencies: 添加lua.lib
5.配置： Linker中的General, Additional Library Dependencies: 添加lib文件所在地
6.生成解决方案，得到lua.exe（~=18KB）

## 七、源码学习

1.移入所有代码，源文件和头文件到 VS c++项目
2.新建main.cpp文件，复制 lua.c的main函数 一些结构
3.注释掉.lua.c luac.c的main函数代码
4.添加.lua文件到资源目录，执行测试