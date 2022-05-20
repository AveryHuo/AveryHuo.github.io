---
title: DOTS-研究学习
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1584498872491.png
categories:
- Unity
---

### 1. What is DOTS?

DATA-ORIENTED TECH STACK
多线程式数据导向型技术堆栈

 核心-高性能
充分利用多核处理器，多线程，让游戏运行速度更快。
组成部分如下：
* C# 任务系统， Job System，用于高效运行多线程代码
* 实体组件系统，ECS， 默认编写的高性能代码的框架结构
* Burst编译器，用于生成高度优化的本地代码

Job System 与ECS是独立的，两者结合实际才能发挥最大优势。

### 2. Job System

* 在Job System之前，unity 仅在内部支持多线程，外部都必须运行在主线程上
* C#虽然支持多线程，但在unity中只处理数据，如网络消息，下载等等，且在线程中调用Unity的API是不行的。
* 有了Job System,可以充分利用多核CPU，比如在多线程中修改Transform等
* 例：MMO游戏判断碰撞，大量同步角色坐标，大量血条飘字等较为适合
* 不必过于担心线程安全，加锁的问题
* 配合Burst更佳

2.1 HPC# -High Performance C#

介绍：
* IL2Cpp虽然将IL转成C++，但实际还是模拟了.NET的垃圾回收，效率并非等同C++
* 使用NativeArray代替T[]，数据类型包括了值类型和其他类型指针
* NativeArray可以在C#层分配 C++中的对象，主动释放而不进行C#的垃圾回收。

Burst性能对比：
* .Net Code 比C++慢2倍
* Mono比.NET Code慢3倍
* IL2CPP与.NET Code相当
* Burst将比C++运行更快。

http://aras-p.info/blog/2018/03/28/Daily-Pathtracer-Part-3-CSharp-Unity-Burst/

2.2 代码使用

* 数据类型只能是值类型和其他类型的指针
* 不能使用引用类型，如T[]数组就不能在job中使用，应用HPC#的NativeArray代替

![enter description here](/img/1584498872491.png)

> IJob与IJobParallelFor
> IJob是一个一个的开线程任务，顺序执行的，所以正确性有保证
> 如果想让线程真正并行，则应使用JobParallelFor。这样并行后的数据就不会有前后依赖关系。
> 使用ReadOnly标记的数据，只读后让Job不为其加锁。
> 默认的数据是Read/Write的，这样在改变数据后，Job一定会等它。
> 加解锁unity已经做好了，不需要自己实现逻辑。
> 
![enter description here](/img/1584499275880.png)

### 3.Burst编译器

3.1 原理
* 以开源LLVM为基础的后端编译技术
* 原理的5个步骤：源代码》前端》优化器》后端 》机器码
* LLVM定义抽象语言IR，前端负责将源代码（C#）翻译成IR，优化器优化，后端将IR生成目标语言（机器码）。
* IR的存在，所以LLVM支持众多语言
* LLVM对C#的GC支持不好，目前burst只支持值类型。

3.2 内存别名
* 之前的编译器无法知道运行时两个指针指向同一个地址的情况，编译出的代码必然要占用额外寄存器多次拷贝，无法优化。
* NativeArray的API禁止限制了内存别名，不存在两个指针指向同一地址的情况。所以它更加高效。


3.3 Unity.Mathmatcis数学库
* 更高效的数据库，提供矢量类型float3,float4. 直接映射到SIMD寄存器
* Math类中也提供了直接映射 到硬件SIMD寄存器。
* SIMD可以一次性计算完毕。
* 旧Math类是不支持SIMD寄存器的。
*

3.4 启动BurstCompile
* 添加标签即可：
* Struct必须实现IJob接口
![enter description here](/img/1584499995727.png)


### 4. ECS

4.1 组合模式：
需要什么功能加什么组件

4.2 传统脚本的问题：
* 耦合度过高
* 引用类型
* 挂脚本过重，产生 0.01s耗时
* 热更支持不好

4.3 Entity  实体
A entity is a key.
* 非常轻量级，一个ID用Int保存。
* 根据需要绑定组件
* 对Cache友好，将相同的组件排列在一起，遍历更快。

4.4 Component 组件
数据层，只有数据
* 实现IcomponentData接口的结构体，不能写方法，没有任何行为
* 注意使用新的数学库代替一些变量。

> ArcheType原型
> 组件命中率高得益于Archetype
> unity规定每个archetype为16K，不够再开，保证连续性

![enter description here](/img/1584500576606.png)

> 共享组件
> 区别IcomponentData于，IsharedComponentData共享组件。是为了避免结构体存储的数据完全相同，从而占用多份内存
> 典型的例子：场景中很多相同mesh和材质的物体。
> 必须实现IEquatable接口！

![共享组件](/img/1584501076960.png)
![enter description here](/img/1584501108996.png)

4.5 System系统
A system is a data tranform.
* 只与Component关联，不关心entity
* 在Update中可以统一更新自己关心的组件

![enter description here](/img/1584500759081.png)

4.6 World世界
Worlds ars for isolation
* 包含EntityManager, ComponentSystem, ArcheTypes.
* ECS默认提供了一个World，也可自己创建
* 世界之间不互通，可以同时并行

### 5. ECS + Job + Burst让性能飞起来

5.1 JobComponentSystem 

* 使用继承于ComponentSystem的JobComponentSystem
* JobComponentSystem的Update效率更高，复杂运算将由Job完成
*  标识ReadOnly让Job的数据并行
*  如果Job数据变更，此Job就不能与其他访问此数据的JOB并行

5.2 JCS与CS混合

* JCS中的实体有任何 结构数据变更修改都带来硬性同步点
* JCS必须保证后面执行的CS拿到的数据准确性，实体增删改都会带来同步点，导致线程卡顿。


5.3 ECS渲染

* ECS自身不包含渲染，但游戏中的渲染与实体是紧密绑定的
* 原理大致是ECS在Job中先准备渲染的数据，通过GPU Instancing一次渲染，中间不产生gameobject.
* GPU instancing不带裁剪，且需要每帧在Update中调用刷新。建议使用CommandBuffer来渲染Gpu instancing，如果在有变化时再刷新。

https://www.xuanyusong.com/archives/4683

* 使用BatchRendererGroup代替Graphics.DrawMeshInstanced和CommandBuffer.DrawMeshInstanced
* BRG强制需要镜头裁剪的JOB方法，自己实现
* BRG需要提供每个渲染物体的包围盒区载用于job中判断是否不在视野。
* BRG内部会调自动Graphics.DrawMeshInstanced且没有1023的数量限制。

![enter description here](/img/1584502302892.png)

![enter description here](/img/1584502316800.png)


### 6.实践

6.1  装Entites, Burst, Hybrid Render, Dots Editor

>报错了？The type or namespace name 'CompilerServices' does not exist in the namespace 'Unity.Burst' (are you missing an assembly reference?)
>选择安装preview下的最高版本，如burst会默认安装非preview的版本

6.2 实例1 创建entity

```csharp
using UnityEngine;
using Unity.Transforms;
using Unity.Entities;
using Unity.Rendering;
using Unity.Mathematics;
public class Spawner : MonoBehaviour
{
    [SerializeField] private Mesh unitMesh;
    [SerializeField] private Material unitMat;

    private EntityManager unitManager;
    private EntityArchetype entityArcheType;
    // Start is called before the first frame update
    void Start()
    {
        InitEntityManager();
        CreateArcheType();
        CreateEntity();
    }

    void InitEntityManager()
    {
        unitManager = World.DefaultGameObjectInjectionWorld.EntityManager;
    }

    void CreateEntity()
    {
        Entity hero = unitManager.CreateEntity(entityArcheType);
        unitManager.AddComponentData(hero, new Translation(){
            Value = new float3(1, 1, 1)
        });

        unitManager.AddComponentData(hero, new Scale()
        {
            Value = 1.0f
        });

        unitManager.AddSharedComponentData(hero, new RenderMesh()
        {
            mesh = unitMesh,
            material = unitMat
        });
        
    }

    void CreateArcheType()
    {
        var translationType = ComponentType.ReadWrite<Translation>();
        var scaleType = ComponentType.ReadWrite<Scale>();
        var rotationType = ComponentType.ReadWrite<Rotation>();
        var renderType = ComponentType.ReadWrite<RenderMesh>();
        var renderBoundsType = ComponentType.ReadWrite<RenderBounds>();
        var localToWorldType = ComponentType.ReadWrite<LocalToWorld>();
        entityArcheType = unitManager.CreateArchetype(translationType, scaleType, rotationType, renderType, renderBoundsType, localToWorldType);
    }
}
```

> 注意： RenderBounds 如果不加，会导致不显示。。

6.2 实例2 自定义system

System定义后，将自动执行update函数。

```csharp
using Unity.Entities;
using Unity.Mathematics;
using Unity.Transforms;

public class MoveSystem : ComponentSystem
{
    protected override void OnUpdate()
    {
        Entities.ForEach((ref Translation trans, ref MoveBySpeedData moveSpeed, ref WaveData waveData) =>
        {
            float zPos = waveData.amplitude * math.sin((float)Time.ElapsedTime * moveSpeed.Value
                + trans.Value.x * waveData.xOffset + trans.Value.y * waveData.yOffset);
            trans.Value = new float3(trans.Value.x, trans.Value.y, zPos);
        });
    }
}

```

6.3 实例3 加入JOB与Burst

在实例2的基础上加上Job和Burst

```csharp

using Unity.Burst;
using Unity.Collections;
using Unity.Entities;
using Unity.Jobs;
using Unity.Mathematics;
using Unity.Transforms;

public class MoveSystem : JobComponentSystem
{
    [BurstCompile]
    private struct MoveJob : IJobChunk
    {
        public double ElapsedTime;

        public ArchetypeChunkComponentType<Translation> TranslationType;
        [ReadOnly] public ArchetypeChunkComponentType<MoveBySpeedData> MoveBySpeedDataType;
        [ReadOnly] public ArchetypeChunkComponentType<WaveData> WaveDataType;
        public uint LastSystemVersion;
        public void Execute(ArchetypeChunk chunk, int chunkIndex, int firstEntityIndex)
        {

            var chunkTrans = chunk.GetNativeArray(TranslationType);
            var chunkSpeedDatas = chunk.GetNativeArray(MoveBySpeedDataType);
            var chunkWaveDatas = chunk.GetNativeArray(WaveDataType);

            for (var i = 0; i < chunk.Count; i++)
            {
                var moveSpeed = chunkSpeedDatas[i];
                var waveData = chunkWaveDatas[i];
                var trans = chunkTrans[i];
                float zPos = waveData.amplitude * math.sin((float)ElapsedTime * moveSpeed.Value
               + trans.Value.x * waveData.xOffset + trans.Value.y * waveData.yOffset);

                // Rotate something about its up vector at the speed given by RotationSpeed.
                chunkTrans[i] = new Translation
                {
                    Value = new float3(trans.Value.x, trans.Value.y, zPos)
                };
            }
        }
    }
    EntityQuery m_Group;
    protected override void OnCreate()
    {
        m_Group = GetEntityQuery(ComponentType.ReadOnly<MoveBySpeedData>(),
                               ComponentType.ReadOnly<WaveData>());
    }

    protected override JobHandle OnUpdate(JobHandle inputDeps)
    {
        var job = new MoveJob()
        {
            TranslationType = GetArchetypeChunkComponentType<Translation>(false),
            MoveBySpeedDataType = GetArchetypeChunkComponentType<MoveBySpeedData>(true),
            WaveDataType = GetArchetypeChunkComponentType<WaveData>(true),
            ElapsedTime = Time.ElapsedTime
        };
        return job.Schedule(m_Group, inputDeps);
    }
}

```

### 7. 使用Conversion
流程明细：
```c#
// ??? <- IDeclareReferencedPrefabs 调用.
GameObjectDeclareReferencedObjectsGroup.Update()
// ??? <- discovery 阶段结束, 无法再声明更多 asset.
GameObjectBeforeConversionGroup.Update()
GameObjectConversionGroup.Update() <-- 你的 Convert 方法在这时运行
GameObjectAfterConversionGroup.Update()
// ??? <- LinkedEntityGroup + Prefab 都已就绪.
GameObjectExportGroup.Update()
```

7.1 ConversionToEntity
* 为GameObject添加ConversionToEntity将自动转换为ECS的entity. 
* 添加ConversionToEntity(Stop)将保持为原gameobject

7.2 ConversionMode
* Convert And Destroy模式：如果没有conversion system处理的组件，在Conversion world 被带入的东西在world销毁时也同时销毁。
* Convert and inject 模式： 此模式下，相比上一个组件都会保留。
> Convert and inject模式是用于当你需要在 conversion 的结果上面回溯原有对象的情况下才有用, 而 Hybrid Renderer 显然无需回溯。

7.3 IConvertGameObjectToEntity
* 继承此接口，在方法Convert里自由控制conversion的过程
> Unity 内置了另一种名为ConvertGameObjectToEntitySystem 的 conversion system. 该 system 会迭代 conversion world 中所有的GameObject, 接着使用GetComponents 并判断是否实现IConvertGameObjectToEntity 接口, 然后再调用该接口的.Convert 方法

7.4 LinkedEntityGroup
* 为原层次结构做关联的组件。同时也是一个dynmaic buffer。 
* 调用Instantiate方法时, 会同时实例化所有 buffer 中的 entity, 同时也会创建相同的LinkedEntityGroup. 注意实例化并不一定和ECS中的Prefab component 直接关联.
* 调用DestroyEntity时也会同时销毁 LinkedEntityGroup中的所有 entity. 类似在编辑器中删除GameObject
* 调用 entityManager.SetEnabled 加上的 Disabledcomponent 会告知 ECS 的查询系统忽略它们, 而 LinkedEntityGroup 中的 entity 也会受到同样的影响. 有点类似禁用GameObject 时同时会禁用整个层级树.

> 当有子物体Disable状态时，此子物体自身不会生成linkedentitygroup的子结构,但可以手动在此disable上添加

> 注意如果buffer 中的 entity 也有LinkedEntityGroup, 系统不会递归地执行instantiation/destroy/disabled 过程.
这些过程在具体执行当中也有一些细微不同.Instantiate和SetEnabled只要检测到 buffer 便在所有成员上一次性执行, 不会做其他更多事. 这意味着关联该 buffer 的 entity 必须要把自己包括在内才能正常工作. 然而DestroyEntity则无所谓, 因为它会先销毁传入的entity, 然后再迭代 buffer 中的 entity 进行销毁.
要注意LinkedEntityGroup 和 Parent并不一样 (虽然它们经常同时出现). 后者是递归地工作, 循环依赖也是不允许的.

* 为gameobject添加
```c#
public class CubeConvert : MonoBehaviour, IConvertGameObjectToEntity
{
    public void Convert(Entity entity, EntityManager dstManager, GameObjectConversionSystem conversionSystem)
    {
        conversionSystem.DeclareLinkedEntityGroup(this.gameObject);
    }
}
```

> 在 entities-0.5.1版本里, TypeManager.cs 源码中可看到, 任何没有[InternalBufferCapacity] 的buffer 类型都会默认 128/size 的容量. LinkedEntityGroup里面装的是 entity, 因此其容量是 128/8 = 16 .
每个 Entity 关联的LinkedEntityGroup(或者其他未指定 capacity 的buffer) 将占据 128 bytes. 这是 chunk 容积变小的原因.
层级中超过16个子对象并不是什么好事, 一旦超过这个数量, 这些 linked entities 不得不从排列良好的 chunk 内存中挪到堆内存中. 可能 Unity 认为 16 是一个不太可能达到的值, 而 8 又太过于常见.
除非显式调用, LinkedEntityGroup仅仅在 prefab 的 conversion 过程中被自动创建, 因此你只需要注意你的 prefab 里面嵌套的 GameObject 数量
在运行时, 所有嵌套 prefab 和 prefab variant 工作流并不受影响, 系统内部只把它们看过一个单独的 prefab. 你无法把嵌套 prefab 从父 prefab 中拿出来, 并期望LinkedEntityGroup正常工作.
最后, 16个entities 一个 chunk ，  1MB 大概包含 60 个 chunk. 如上例, 你能在 1MB 存储大约 2700 个转换后的GameObject , 这样看来或许45 的 chunk 容量也不用太担心了(当然具体情况具体分析).

7.5 创建额外的entity
使用如下方式：
```c#
  Entity additional1 = conversionSystem.CreateAdditionalEntity(this.gameObject);
        dstManager.SetName(additional1, $"{this.name}_Add1");
        Entity additional2 = conversionSystem.CreateAdditionalEntity(this.gameObject);
        dstManager.SetName(additional2, $"{this.name}_Add2");
```

> 注意：此方式创建的entity将不在linkedentitygroup内，且是完全空的entity
