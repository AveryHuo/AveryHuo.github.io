---
title: Jenkins打包事项
categories:
- 工作相关
tags: 
- Jenkins
- CI
---

# Jenkins 打包说明



## 脚本准备

### 自动化脚本

> 1. AutoCi.rar文件
> 2. 将文件解压至与Assets同级目录即可

### Unity脚本

> 1. Editor 目录下创建类BundleMakerUtil.cs， 添加如下函数：
>
>    ```C#
>      public static bool HasRawArg(string name)
>      {
>          var args = System.Environment.GetCommandLineArgs();
>          for (int i = 0; i < args.Length; i++)
>          {
>              if (args[i].Trim() == name)
>              {
>                  return true;
>              }
>          }
>          return false;
>      }
>    
>    ```
>
>    
>
> 2. Editor目录下创建类BuilderMenu.cs　使用命名空间SGameBundleMaker. （也可自定义，但需要修改auto_ci.py里的配置）
>
> 3. BuilderMenu.cs类中创建 build_bundle_for_ci() 静态函数，示例：

 ```c#
   public static void build_bundle_for_ci()
   {
   		 //... Code for build build 
          AssetBundleManifest bundle_manifest = null;
            try
            {
                bundle_manifest = BuildPipeline.BuildAssetBundles(BundleMaker.BUNDLE_DIR, all_build, BuildAssetBundleOptions.DeterministicAssetBundle | BuildAssetBundleOptions.ChunkBasedCompression, EditorUserBuildSettings.activeBuildTarget);
            }
            catch (Exception e)
            {
                error_code_ = BundleMakerErrorCode.UNKNOWN;
                Debug.LogError("BuildAssetBundles Error: " + e.Message);
                return;
            }
   }
 ```



> 4. BuilderMenu.cs中创建 build_for_ci() 静态函数
>
>    注：-proj, -path 也可修改，需要与auto_ci.py中代码对应
>
>    示例如下:

```c#
public static void build_for_ci()
{
    //！Builder类需要自己实现，具体作为对应不同平台打包用
    string build_path = string.Empty;
    #if UNITY_ANDROID
        //是否输出项目文件或APK的标识
        bool is_proj = BundleMakerUtil.HasRawArg("-proj");
    Debug.Log("build_for_ci, is_proj: " + is_proj);
    Builder.is_android_proj = is_proj;
    if(Builder.is_android_proj){
        build_path = Const.PROJECT_DIR + "autopack/android/XGameProject";
    }else{
        build_path = Const.PROJECT_DIR + "autopack/android/XGame.apk";
    }
    #elif UNITY_IPHONE
        build_path = BundleMakerUtil.GetArg("-path");
    if (string.IsNullOrEmpty(build_path))
    {
        Debug.LogError("------build path null");
        return;
    }
    Debug.Log("build_for_ci, build_path: " + build_path);
    //build_path = string.Format("{0}autopack/ios/XcodeProject{1}", new DirectoryInfo(Const.PROJECT_DIR).Parent.FullName, System.DateTime.Now.ToString("yyyy-MM-dd--HH-mm-ss"));
    #else
        build_path = Const.PROJECT_DIR + "autopack/win32/XGame.exe";
    #endif
        //是否是debug版本的标识
        bool is_debug = BundleMakerUtil.HasRawArg("-debug");
    Builder.is_debug_build_ = is_debug; 
    Builder.build_package(build_path, true);
}
```



## Jenkins配置

> 1. Jenkins安装 Powershell插件，在 插件列表中搜索到这个：

<img src="./images/1571217538404.png" alt="1571217538404" style="zoom:100%;" />

> 2. 安装完后，重启下Jetkins
> 3. 在项目配置->构建 里选择使用Windows PowerShell:

<img src="./images/1571217610540.png" alt="1571217610540" style="zoom:100%;" />

> 4. 添加如下配置在Command格内：

```powershell
echo ${ENV:WORKSPACE}
cd ${ENV:WORKSPACE}/Unity
./AutoCi/autobuild_android.ps1
```

<img src="./images/1571217788247.png" alt="1571217788247" style="zoom:100%;" />



## 打什么样的包？  设置环境变量

> 1. 找到Jenkins环境变量设置
>
>    **Manage Jenkins**   ->  **Configure System**



![1571216524617](./images/1571216524617.png)

<img src="./images/1571216565243.png" alt="1571216565243" style="zoom:67%;" />



> 2.  打 Apk 

设置 IsApk 为 true



> 3. 打 aar到平台

设置 IsApk 为false或其他



> 4. 带Debug的包

设置 IsDebug为true,  当不为true时则默认为relase包



## CI的执行脚本说明

> 1. auto_ci.py -仅打aar到平台需要
>    * 修改manifest.xml文件，去掉intent-filter
>    * 修改build.gradle文件，设置为library，去掉applicationId，设置gradle版本，添加jcenter(),google()到 all projects块
> 2. jksdk_util.py -上传aar到平台
>    
>    * 需要打开文件，更改下id为对应项目
>    
>    * 上传到平台，需要改成指定格式的名字： 
>    
>        游戏名称-框架类型-debug/release-version.出包号.aar



## 注意事项

> 1. Powershell 脚本访问Jenkins环境变量记得加 **ENV:** 前缀
> 2. 在build.gradle加入的all projects块的代码，是由于gradle有时会找不到相关的jar包，又不会启动自动下载导致

