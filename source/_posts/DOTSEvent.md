---
title: DOTS-事件
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---

### 方式一、使用NativeQueue循环检测
* 1. 获取JOB可写的多线程NativeQueue对象
```c#
NativeQueue<PipePassedEvent>.ParallelWriter eventQueueParallel = eventQueue.AsParallelWriter();
```

* 2. 发出事件
```c#
eventQueueParallel.Enqueue(new PipePassedEvent());
```

* 3. 事件机
```c#
while (eventQueue.TryDequeue(out PipePassedEvent evnt))
        {
            //Debug.Log("Get EVENT!!");
            OnPipePassed?.Invoke(this, EventArgs.Empty);
        }
```

4.接收事件
```c#
World.DefaultGameObjectInjectionWorld.GetOrCreateSystem<PipeMoveSystem_Done>().OnPipePassed += TestingDOTSEvents_OnPipePassed;
```


### 方式二、使用EntityCommandBuffer

* 1. 获取CommandBuffer的System
* 2. 从System中创建一个commandbuffer, 并拿其Concurrent
* 3. 利用2的concurrent就可以在job中创建一个entity.
* 4.使用Entities.WithoutBurst().ForEach执行触发事件，并在触发完后一定将entity删除掉。

```c#
 EntityCommandBuffer entityCommandBuffer = endSimulationEntityCommandBufferSystem.CreateCommandBuffer();
        EntityCommandBuffer.Concurrent entityCommandBufferConcurrent = entityCommandBuffer.ToConcurrent();
        EntityArchetype eventEntityArchetype = EntityManager.CreateArchetype(typeof(EventComponent));

        double ElapsedTime = Time.ElapsedTime;

        JobHandle jobHandle = Entities.ForEach((int entityInQueryIndex, ref Translation translation, ref Pipe pipe) => {
            float xBefore = translation.Value.x;
            translation.Value += moveDir * moveSpeed * deltaTime;
            float xAfter = translation.Value.x;

            if (pipe.isBottom && xBefore > 0 && xAfter <= 0) {
                // Passed the Player
                Entity eventEntity = entityCommandBufferConcurrent.CreateEntity(entityInQueryIndex, eventEntityArchetype);
                entityCommandBufferConcurrent.SetComponent(entityInQueryIndex, eventEntity, new EventComponent {
                    ElapsedTime = ElapsedTime
                });
            }
        }).Schedule(inputDeps);

        endSimulationEntityCommandBufferSystem.AddJobHandleForProducer(jobHandle);

        EntityCommandBuffer captureEventsEntityCommandBuffer = endSimulationEntityCommandBufferSystem.CreateCommandBuffer();

        Entities.WithoutBurst().ForEach((Entity entity, ref EventComponent eventComponent) => {
            Debug.Log(eventComponent.ElapsedTime + " ### " + ElapsedTime);
            OnPipePassed?.Invoke(this, EventArgs.Empty);
            captureEventsEntityCommandBuffer.DestroyEntity(entity);
        }).Run();
```

>  不用EndSimulationEntityCommandBufferSystem 也可以直接定义EntityCommandBuffer。只要在 job complete时，手动dispose()即可。
```c#
entityCommandBuffer.Playback(EntityManager);
        entityCommandBuffer.Dispose();
```