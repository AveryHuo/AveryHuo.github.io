---
title: Addressable 研究
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1579072055300.png
categories:
- Unity学习
tags: 
- Unity学习
---

## 什么是Addressable？
![什么](/img/1579072055300.png)

## Addressable的实例函数

![实例函数](/img/1579077588215.png)

## 以label形式加载

![以label加载](/img/1579078623846.png)

## 模式选择

![模式](/img/1579078890824.png)

Data Builders：在Addressable窗口菜单中能够选择的在编辑器下的数据构建模式，一般来说附带的这几个已经可以满足大部分要求，你也可以新建适合自己项目的模式。
Fast Mode：加载资源不通过资源包，直接使用AssetDatabase加载。
Virtual Mode：会形成AssetBundle布局，但是不需要打包，加载资源通过ResourcesManager加载，并且可以在RM Profiler中查看包体布局。
Packed Mode：需要额外步骤打包AssetBundle，运行时资源也是在AssetBundle中进行加载。

## 迁移指南

![从自己框架移植](/img/1579081015473.png)

![从Resources移植](/img/1579081031342.png)


## 使用注意项：
1.每调用一次Addressables.Instantiate方法，会将该Asset的引用计数加一；而Addressables.ReleaseInstance会减少这个引用计数。如果你使用Object.Destroy释放了它，则原始资源会一直存在于内存中。所以应当避免使用Object.Destroy方法了~
2.非使用 Addresables.Instantiate 方法实例化出来的对象，如使用Unity自带的Instantiate实例出来的对象，也可以使用Addressables.ReleaseInstance来释放，这并不会对计数有影响，只是单纯的释放。
3.任何通过Addresables.Instantiate 方法实例化出来的对象，在切换场景的时候，如果没有标记为 DontDestroyOnLoad ,则会被自动调用Addressables.ReleaseInstance来释放掉。


## 总结：
* 1. 出包时将自动带上catalog.json在包内，出包的时候不用带 catalogxxx.json 和catalog.hash文件
* 2. 可使用接口随时重加载catalog文件。如：

``` csharp
//注意： 一定要先清除所有resoucelocators
Addressables.ClearResourceLocators();
//重加载下载好的catalog文件
await Addressables.LoadContentCatalogAsync(Path.Combine(ResourceConfig.GetLocalBundlePath(), "catalog.json"),true).Task;
```

3. 因此 ： 流程可采用如下的方式：
 > 1. 将设置好assetbundle provider，这里仍用旧的方式，对资源加载时的路径进行跳转限制，优先找SD卡资源，再找包体资源。
 > 2. 出APK包，在 catalog打完包，在资源中不需要带，直接删除掉。资源+version.txt即可
 > 3. 出资源包时，带上新名字的catalog文件作为清单。
 > 4.下载模块完全用自己实现！ 先加载SD卡的catalog文件，没有，则默认用包内的。 如果有新的，再次调用加载catalog，这样读取就是最新的。