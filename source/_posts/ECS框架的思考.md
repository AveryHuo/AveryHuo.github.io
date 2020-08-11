---
title: ECS框架的思考
categories:
- Unity
---

# 对比ECSGameEngine框架的问题：
1.Archetype加入的优势 ？
2.Component与Entity不使用类概念的好处？



# 开发模式的变更（对比ECSGameEngine）：
1.System与数据对象之间无组合关系
* Unity ECS
读取所有数据方式都一样
* A: 在Awake时通过GetComponentGroup 注册需要的component
* B: 处理时使用group.ToComponentDataArray拿到Entity. 再从Entity取出Component数据

* ECSGameEngine：
读取其他数据：需要访问其他的System或某个manager来获取。
* A: 新建一个Entity对象，将Component数据预先存到对象里
* B: 此System需要某个Entity时，在awake时将Entity实例加入进去，访问其下Component拿数据

>ECSGameEngine框架，Component，Entity与System有组合关系，如果有共享Entity数据，这时要么System间相互访问，要么借助另一个公共类将Entity存起来。
>Unity的ECS，Entity是直属于EntityManager<- World层的。Entity与System没有任何关联。 Component 对应存储在Archetype中，并有entity的标签（id），System会通过componen类型找到对应的Entity，再从entity获取数据内容。

2.内存优化

* Unity ECS
同类的Component 存在Archetype中，Archetype存储着一堆chunk，一个chunk 16KB.

* ECSGameEngine
所有都为类，都将占用堆内存，第一次实例时内存将会有一个峰值，多次进出将重复利用内存。

3.应用层差别

* Unity ECS:
在LUA层这边，可以自由的组建Component数据到Table中，再将此数据以以下两种形式装载：
	*A: ECS.TypeManager.RegisterType("MyComponentData", {value=0}) --装载时即指定此Component数据（适合全局）
	*B: 在拥有Entity时，ECS.EntityManager:SetComponentData(entity, "MyComponentData", {value=123}) --通过设置entity里的数据设置（适合局部修改）
	
* ECSGameEngine:  
	* A： 定义一个类，继承自EntityComponent
	* B:  找到一个Entity来挂载或定义一个新的Entity类，继承自Entity
	* C: 