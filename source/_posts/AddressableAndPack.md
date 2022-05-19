---
title: 最新Addressable资源打包与加载框架
categories:
- 公司
tags: 
---

#### 一、Addressable介绍

Addressable是Unity最新推出且正式发布的资源管理系统，内含引用计数管理，快速资源热更，资源性能查看器，资源冗余工具等等，据官方的说法，这就像当初AssetBundle取代Resources一样，Addressable就是为了取代直接使用AssetBundle而生。

#### 二、Addressable下载更新
> 内容均在ResDownloadComponent中。

##### 1. 打包资源
手动： 使用 Build ->New Build -> Default Build Script。 也可用打包脚本，`AddressableAssetSettings.CleanPlayerContent();
        AddressableAssetSettings.BuildPlayerContent();`
生成的资源将在Library->com.unityengine.addressable下
> 建议本机初次导项目后，先执行一次打包资源，再使用Use Existing Build的Play Mode Script方式，以bundle加载运行，方便测试。

##### 2. 更新资源
* 在发完包的情况下，在打包的机器上的Unity，选择Tools -> Check for Content Update Restriction 来获取变更的资源
* 将这些资源应用出来一个新的Group， 再统一挂上updates的标签！
* 选择Build -> Update a previous build 选择android的bin文件，等待完成，将会生成新的updates开头的更新文件，将这些文件上传即可更新。
> 更新完后之后，如果再需要出包，请将资源归还到原group中，以防下次混乱了。

#### 3.打包工具使用
本地打包，可使用Tools -> 打包工具，勾选 是否打包工程，将导出一个gradle的工程，否则将先打出工程后接着打出apk。
打包机不可使用此工具打包，由CI控制。

#### 三、Addressable内置接口介绍

> 针对Addressable有两个缓存池，一个针对asset的 AssetCachePoolComponent，用于存放所有的资源，一般存放不需要实例化的资源，如material等。  另一个针对实例对象的 ResGameObjectPoolComponent， 用于存放实例出来的资源，会记录对象的handle句柄和对象实例列表。

 ##### 1. 加载接口

1.1 LoadAssetAsyncHandle(assetName, saveToCache = false, isGlobal = false)
 * 以asset的形式加载资源不实例化，只返回相应资源句柄. [saveToCache]意为加载完的资源将直接记到缓存池，[isGlobal] 决定了是全局缓存池还是场景缓存池
**注意： [isGlobal]只在[saveToCache]为 true 时才会使用,用于保存在全局缓存池或对应场景的池子中**
```csharp
 ETTask<AsyncOperationHandle<T>> LoadAssetAsyncHandle<T>(string assetName, bool saveToCache = false, bool isGlobal = false)
```

>简单用法使用示例：(加载配置文件的Config预制)
>
>```csharp
> //获取加载完的句柄
>var configGOHandle = await ResourceLoaderComponent.Instance.LoadAssetAsyncHandle<GameObject>("Config");
>//从Handle中获取结果
> configGO = configGOHandle.Result;
> //当时即销毁此Handle
>ResourceLoaderComponent.Instance.ReleaseHandle(configGOHandle);


>深度使用示例：
>```csharp
>//预加载需要用的材质，设值记录到缓存, 且非全局资源
>await ResourceLoaderComponent.Instance.LoadAssetAsyncHandle<Material>("GrayMaterial",true,false);
> //从缓存加载对应的材质
> Material MAT_GARY = ResourceLoaderComponent.Instance.LoadFromCache<Material>("GrayMaterial", false);
>//从缓存删除对应的材质
> ResourceLoaderComponent.Instance.ReleaseFromCache("GrayMaterial",false,typeof(Material));
>```

1.2 LoadAssetsAsyncHandle(assetName, label = ResourceLabel.none, saveToCache = false, isGlobal = false)
* 以asset的形式加载资源不实例化，只返回相应此资源数组句柄. 区别于1.1接口，此接口可配置多一个label的参数指明资源标签。
**注意：如果保存到缓存中，则是一个数组，LoadFromCache时必须使用一个数组返回。**
```csharp
 ETTask<AsyncOperationHandle<IList<T>>> LoadAssetsAsyncHandle<T>(string assetName, ResourceLabel label = ResourceLabel.none, bool saveToCache = false, bool isGlobal = false)
```

>使用示例：
>```csharp
>var handle = await Game.Scene.GetComponent<ResourceLoaderComponent>().LoadAssetsAsyncHandle<GameObject>("HeadResSmallSize",ResourceLabel.ui);
>var userIcon = handle.Result[0];
>``` 
 
1.3 LoadPrefab(assetName, label, dontDestroy = false, parent = null)
* 以asset和label的形式加载资源并实例化, 如果dontDestroy为true，则为全局资源，不随场景删除
```csharp
 ETTask<GameObject> LoadPrefab(string assetName, ResourceLabel label = ResourceLabel.none, bool dontDestroy = false, Transform parent = null)
```

>使用示例：
>```csharp
>//(配置Buff的预制)
> GameObject configGo = await Game.Scene.GetComponent<ResourceLoaderComponent>().LoadPrefab($"{buffCfg}",ResourceLabel.buff);
 >```

1.4 LoadPrefab(assetName, label, scene, parent = null)
* 以asset和label的形式加载资源并实例化,同1.3，不过传入一个框架里的Scene对象用于存储此对象的缓存池
```csharp
 ETTask<GameObject> LoadPrefab(string assetName, ResourceLabel label = ResourceLabel.none, bool dontDestroy = false, Transform parent = null)
```

 ##### 2. 缓存类接口
 
 2.1 ReleaseFromCache(string key, bool isGlobal, Type resType)
* 将某个key直接从【AssetCachePool】对象池子里释放，isGlobal决定了使用全局缓存池还是场景缓存池

2.2 LoadFromCache<T>(string key, bool isGlobal) where T: UnityEngine.Object
 * 从【ResGameObjectPool】缓存池加载一个类型T的对象，isGlobal决定了使用全局缓存池还是场景缓存池

2.3 RecyclePrefab(string poolKey,GameObject o, bool isGlobal = false)
* 将对象o回收进某个key对应的【ResGameObjectPool】缓存池，isGlobal决定了使用全局缓存池还是场景缓存池

2.4 RecyclePrefab(string assetName, ResourceLabel resLabel, GameObject o, bool isGlobal = false)
* 将对象o回收进某个资源名及label对应的【ResGameObjectPool】缓存池，isGlobal决定了使用全局缓存池还是场景缓存池

2.5 ReleasePrefab(string assetName, ResourceLabel resLabel, bool isGlobal = false)
*  将对应assetName和resLabel的实例对象从【ResGameObjectPool】池子中释放（清除），isGlobal决定了使用全局缓存池还是场景缓存池


##### 3. addressable接口

3.1 ReleaseHandle(AsyncOperationHandle handle)
* 释放一个addressable的异步句柄 

