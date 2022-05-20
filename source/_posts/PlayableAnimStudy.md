---
title: Playable动画系统研究
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity学习
tags: 
- Unity学习
---

## 1. Playable是什么
Playable是一组API，可以用来组合、混合、修改多个数据源，然后通过一个输出，将这些数据源处理完的结果播放出来。

## 2. 简单使用：播放单个动画
* PlayableGraph的AnimationOutput依然是基于Animator组件的，不过你可以不用关心它了。
* 主要实现目的是可以不创建animationcontroller，用代码实现其中的一些功能

``` csharp
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;
 
public class PlayClipOnObject : MonoBehaviour
{
   public AnimationClip myClip;
   private PlayableGraph graph;
 
   void Start () {
      PlayAnimation(gameObject, myClip);
   }
   
   public void PlayAnimation(GameObject target, AnimationClip clip) {
      // Create the PlayableGraph, which is the root of the Playable API stuff
      graph = PlayableGraph.Create();
 
      //We need an Animator to play stuff, even if we're not using an AnimatorController. So just add one:
      var animator = target.AddComponent<Animator>();
 
      //Wrap the clip in a thing the Playable system understands:
      var clipPlayable = AnimationClipPlayable.Create(graph, clip);
 
      //Create the output, and make the clip be the output's source. This API is a bit wordy :p
      var animOutput = AnimationPlayableOutput.Create(graph, "some name", animator);
      animOutput.SetSourcePlayable(clipPlayable);
 
      //play the thing
      graph.Play();
    }
 
   void OnDestroy()
   {
      // If you don't destroy the graph, it leaks in the engine (and Unity whines), so destroy it!
      // IsValid will be false if the graph was never created (ie. this component is never enabled before it's destroyed)
      if(graph.IsValid())
         graph.Destroy();
   }
}
```


创建步骤：
1. 创建Graph

```csharp
playableGraph = PlayableGraph.Create();
```
2. 创建Ouput
   

``` csharp
var playableOutput = AnimationPlayableOutput.Create(playableGraph, "Animation", GetComponent<Animator>());
```

3. 为clip创建针对的Playable对象
   

``` csharp
 var clipPlayable = AnimationClipPlayable.Create(playableGraph, clip);
```

4. 设置playable对象到Output中
   

``` csharp
 playableOutput.SetSourcePlayable(clipPlayable);
```

5. 让Graph执行play
   

``` csharp
playableGraph.Play();
```

* 6. 需要在结束时销毁Graph对象
  

``` csharp
playableGraph.Play();
```

> Playable Output类型
为了避免GC，所有类型都是使用struct实现的。
构建PlayableGraph一般有如下的流程：

创建一个PlayableGraph，方法是PlayableGraph.Create("graph的名字")
创建输出节点，常用的有
``` csharp
AnimationPlayableOutput.Create(playableGraph, "name", GetComponent<Animator>());
AudioPlayableOutput.Create(playableGraph, "name", GetComponent<AudioSource>());
```

还可以创建自定义的输出节点


创建各种playables。所有的Playable都有一个静态的Create()方法，用来创建playable实例。需要注意的是自定义的PlayableBehaviour需要使用
``` csharp
ScriptPlayable<T>.Create(playableGraph);
```
来创建。

``` csharp
AnimationClipPlayable.Create(playableGraph, animationClip);
AudioClipPlayable.Create(playableGraph, audioClip, true);
ScriptPlayable<T>.Create(playableGraph);
```

连接playable和output：PlayableOutput.SetSourcePlayable()
playable之间的连接：PlayableGraph.Connect()。
播放graph：PlayableGraph.Play()
如果graph不再使用，记得销毁：PlayableGraph.Destroy()。调用这个方法后会销毁所有的playbles和output。

## 3. 替代AnimationController

1. 创建混合树AnimationMixerPlayable，实现AnimationController之间连线控制功能：
  

``` csharp
using UnityEngine;

using UnityEngine.Playables;

using UnityEngine.Animations;
using UnityEngine.Experimental.Animations;

[RequireComponent(typeof(Animator))]

public class PlayAnimationSample : MonoBehaviour

{

    public AnimationClip clip0;
    public AnimationClip clip1;
    
    PlayableGraph playableGraph;
    private AnimationMixerPlayable m_Mixer;

    public float tranTime = 2;
    private float leftTime;
    
    void Start()

    {

        playableGraph = PlayableGraph.Create("测试");

        playableGraph.SetTimeUpdateMode(DirectorUpdateMode.GameTime);

        var playableOutput = AnimationPlayableOutput.Create(playableGraph, "Animation", GetComponent<Animator>());

        // Wrap the clip in a playable

        m_Mixer = AnimationMixerPlayable.Create(playableGraph, 2);
        
        AnimationClipPlayable clipPlayable0 = AnimationClipPlayable.Create(playableGraph, clip0);
        AnimationClipPlayable clipPlayable1 = AnimationClipPlayable.Create(playableGraph, clip1);

        playableGraph.Connect(clipPlayable0, 0, m_Mixer, 0);
        playableGraph.Connect(clipPlayable1, 0, m_Mixer, 1);
        
        m_Mixer.SetInputWeight(0,1);
        m_Mixer.SetInputWeight(1,0);
        // Connect the Playable to an output

        playableOutput.SetSourcePlayable(m_Mixer);
        playableOutput.SetSortingOrder(0);
            
            // Plays the Graph.
        leftTime = tranTime;
        playableGraph.Play();

    }

    void Update()
    {
        leftTime = Mathf.Clamp(leftTime - Time.deltaTime, 0, 2);
        float weight = leftTime / tranTime;
        Debug.Log("weight:"+weight);
        m_Mixer.SetInputWeight(0, 1 - weight);
        m_Mixer.SetInputWeight(1, weight);
    }
    
    void OnDestroy()
    {
        // Destroys all Playables and PlayableOutputs created by the graph.
        playableGraph.Destroy();
    }
}
```

## 5. 实现自定义的PlayableBehaviour

实现
* 1.继承 PlayableBehaviour 
* 2.在初始化函数中传入graph, playable对象，分别为每个动画创建Playable并添加到mixer中，设置weight

调用
* 1.使用ScriptPlayable.Create创建自定义的Playable对象
* 2.从Playable中获取behaviour并利用此behaviour调用初始化函数

``` csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;

public class CustomPlayable : PlayableBehaviour
{
    private int m_CurrentClipIndex = -1;
    private float m_TimeToNextClip;
    private Playable mixer;
    public void Initialize(AnimationClip[] clipsToPlay, Playable owner, PlayableGraph graph)
    {
        owner.SetInputCount(1);
        mixer = AnimationMixerPlayable.Create(graph, clipsToPlay.Length);
        graph.Connect(mixer, 0, owner, 0);
        owner.SetInputWeight(0, 1);
        for (int clipIndex = 0 ; clipIndex < mixer.GetInputCount() ; ++clipIndex)
        {
            graph.Connect(AnimationClipPlayable.Create(graph, clipsToPlay[clipIndex]), 0, mixer, clipIndex);
            mixer.SetInputWeight(clipIndex, 1.0f);
        }
    }
    
    override public void PrepareFrame(Playable owner, FrameData info)
    {
        if (mixer.GetInputCount() == 0)
            return;
        // Advance to next clip if necessary
        m_TimeToNextClip -= (float)info.deltaTime;
        if (m_TimeToNextClip <= 0.0f)
        {
            m_CurrentClipIndex++;
            if (m_CurrentClipIndex >= mixer.GetInputCount())
                m_CurrentClipIndex = 0;
            var currentClip = (AnimationClipPlayable)mixer.GetInput(m_CurrentClipIndex);
            // Reset the time so that the next clip starts at the correct position
            currentClip.SetTime(0);
            m_TimeToNextClip = currentClip.GetAnimationClip().length;
        }
        // Adjust the weight of the inputs
        for (int clipIndex = 0 ; clipIndex < mixer.GetInputCount(); ++clipIndex)
        {
            if (clipIndex == m_CurrentClipIndex)
                mixer.SetInputWeight(clipIndex, 1.0f);
            else
                mixer.SetInputWeight(clipIndex, 0.0f);
        }
    }
}

```

``` csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Animations;
using UnityEngine.Playables;

public class PlayCustomPlayableSample : MonoBehaviour
{
    public AnimationClip[] clipsToPlay;

    PlayableGraph m_Graph;

    void Start()
    {
        m_Graph = PlayableGraph.Create();
        var custPlayable = ScriptPlayable<CustomPlayable>.Create(m_Graph);

        var playQueue = custPlayable.GetBehaviour();

        playQueue.Initialize(clipsToPlay, custPlayable, m_Graph);

        var playableOutput = AnimationPlayableOutput.Create(m_Graph, "Animation", GetComponent<Animator>());

        playableOutput.SetSourcePlayable(custPlayable);
        playableOutput.SetSourceInputPort(0);

        m_Graph.Play();
    }

    void OnDisable()

    {

        // Destroys all Playables and Outputs created by the graph.

        m_Graph.Destroy();

    }
}

```


## 4. 工具：  PlayableGraph Visiualizer
  * 停止更新于去年4月
    
>在场景中的Animator运行时，将自动映射动画到Visiualizer中显示
>在创建好的PlayableGraph ，运行时也会在其中显示


