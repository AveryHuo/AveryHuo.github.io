---
title: UI系统制作流程
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- 公司
tags: 
---

			* [一、准备UI预制](#一-准备ui预制)
			* [二、控制脚本](#二-控制脚本)
			* [三、UI系统的对象池](#三-ui系统的对象池)
			* [三、配入UI表](#三-配入ui表)
			* [四、窗口的显示或关闭](#四-窗口的显示或关闭)

#### 一、准备UI预制
先准备好效果图和资源图集
* 1.新建空场景，在目录下建好资源图集
* 2.找到 ***LoginUI.prefab*** ， 施入场景后，Unpack prefab completed完全解除关联
* 3.清空根结点的Animator组件和Reference Collector组件，并改名， 以 #Name#UI 的方式
* 4.清空Panel下所有内容，让结构保持为Bg, Panel两个一级子结点
*  *5.复制Bg结点，放入美术做好的效果图
* 5.根据UGUI规则完成预制制作
* 6.根结点添加Reference Collector Group组件
* 7.完成后交由特效师添加动画
* 8.将资源放入Addressable Groups的UI组里，右键使用Simplify Addressable Name, 将名字简化

#### 二、控制脚本
1.创建： 在Hotfix 建立文件夹，名字以功能命名，建立Compoents文件夹，新建控制脚本，命名以   UI#Name#Window的方式，如LoginUI，脚本名应为UILoginWindow.cs
2.类的规则以 UIClickWindow.cs为参考。
3.必须有的构造，以指明加载需要的预制名
```csharp
public UIClickWindow():base()
{
	mPrefabName = #Name#;//TODO
}
```
4.必须重写有如下函数：
```csharp
/// <summary>
/// 界面资源加载完成， 一会用于获取各预制及组件，每次新建UI预制将调用
/// </summary>
protected virtual void InitUI()

/// <summary>
/// 界面显示，一般处理每次显示需要即时更新的逻辑，每次setActive将调用
/// </summary>
protected virtual void ResetUI()

/// <summary>
/// 界面关闭，隐藏时调用的，一般与ResetUI放置成对的逻辑
/// </summary>
protected virtual void HideUI()

/// <summary>
/// 界面资源销毁，在预制将销毁时调用与InitUI成对。
/// </summary>
protected virtual void UnInitUI()
```

5. 可选的函数
```csharp
/// <summary>
/// 界面Update更新
/// </summary>
public virtual void Update()
```
#### 三、UI系统的对象池
1.命名池子模板对象的key于头部，如：
```csharp
private const string TaskItemTemplate = "UICarnivalWindow_TaskItemTemplate";
private const string NormalCardItemTemplate = "UICarnivalWindow_NormalCardItemTemplate";
private const string HighlightCardItemTemplate = "UICarnivalWindow_HighlightCardItemTemplate";
```
2.添加对象为模板，让底层创建一个以模板为基的池子
```csharp
AddTemplate(NormalCardItemTemplate, normalItemObj);
AddTemplate(HighlightCardItemTemplate, highlightItemObj);
AddTemplate(TaskItemTemplate, taskItemObj);
```

3.获取： 仅获取一个对象

```csharp
GetTemplateInstance(string name, Transform parent, bool isActive)
```
传入1.定义的模板名字，父对象，是否隐藏就决定获取出来后是否立即隐藏。

4.定义对应模板对象的控制类
* 必须继承UIBaseComponent类
* 继承覆写函数：
```csharp
///初始化函数，每次设置预制时都将会自动调用一次
public virtual void InitObjs()

//销毁时调用
public virtual void Dispose() 
```
5.获取: 获取一个带对象控制器的类对象（将同时生成一个对象放在类的Root）

```csharp
GetTemplateComponent<T>(string name, Transform parent, bool isActive) where T : UIBaseComponent
```
传入1.定义的模板名字，父对象，是否隐藏就决定获取出来后是否立即隐藏。

6.回收
* 回收预制：`FreeTemplateInstance(NormalCardItemTemplate);`
* 回收预制管理类，不会回收预制：`FreeTemplateComponent(NormalCardItemTemplate);`
所以一般两个需要成对调用，如：
```csharp
 FreeTemplateInstance(NormalCardItemTemplate);
FreeTemplateComponent(NormalCardItemTemplate);
FreeTemplateInstance(HighlightCardItemTemplate);
FreeTemplateComponent(HighlightCardItemTemplate);
FreeTemplateInstance(TaskItemTemplate);
FreeTemplateComponent(TaskItemTemplate);
```

７.销毁池子
* 使用UIBaseWindow自带函数销毁单个模板的池子
```csharp
/// 移除模板
void RemoveTemplate(string name)
```
Window在销毁时将调用DestroyAllTemplates() 先回收所有的预制，再清空池子。**因此一般不需要在逻辑里手动移除池子.**

#### 三、配入UI表

1.找到资源表 fgame_ui_config.elsx 按表内的说明配置UI的参数
2.导表

#### 四、窗口的显示或关闭

* 使用UIManager提供的函数显示或关闭一个Window，如：

```csharp
//同步函数显示一个Window
UIManager.Instance.ShowWindowSync("UIClickWindow");
//异步函数
await UIManager.Instance.ShowWindow("UIClickWindow");

//关闭窗口
UIManager.Instance.CloseWindow("UIClickWindow");

```
