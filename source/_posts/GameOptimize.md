---
title: 性能优化相关
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---
1.渲染

- 利用reflect probe代替反射、折射，尽量不用RTT、GrabPass、RenderWithShader、CommandBuffer.Blit (BuiltinRenderTextureType.CurrentActive...)
- 建立统一后处理框架(bloom、hdr、DOF等)代替多后处理，可以共用模糊函数，减少多次blit；另外要注意RTT的尺寸。
- 空气折射、热浪扭曲等使用GrabPass不是所有硬件都支持，改为RTT或者后处理来优化。
- 建立统一shader材质代替单一shader，充分利用shader_feature、multi_compile，并将宏开关显示于界面。
- 图像混合代替多通道纹理，阴影投射、阴影接收、MetaPass、forwardadd 等pass不需要时要剔除。
- 少用alpha test、discard、clip、Alpha Converage等，因为会影响Early-Z Culling、HSR的优化。
- 避免Alpha Blend穿透问题（权重混合、深度剥离等透明排序方法代价太大了）。
- 光照贴图代替动态阴影、尽量不用实时光；阴影贴图、环境贴图用16位代替32位；利用projector+rtt或者光圈代替实时阴影。
- 将环境参数（风、雨、太阳）等shader全局参数统一管理。
- 非主角可以用matcap代替pbr、无金属不一定要用pbr，仔细选择物理渲染所用的FDG（F:schlick、cook-torrance、lerp、要求不高用4次方，D：blinn-phong、beckmann、GGX、GGX Anisotropic,G:neumann、cook-torrance、Kelemen、SmithGGX；standard shader要注意选择BRDF1-BRDF3），渲染要求不高时不用GGX；可以用LH来优化GGX。
- 用fixed、half代替float,建立shader统一类型（fixed效率是float的4倍，half是float的2倍），小心选择shader变量的修饰(uniform、static、全局),选择Mobile或Unlit目录下shader
- 使用高低配渲染，内存足够时可以考虑开启mipmap
- 使用surface shader注意关掉不用的功能，比如：noshadow、noambient、novertexlights、nolightmap、nodynlightmap、nodirlightmap、nofog、nometa、noforwardadd等
- standard shader的变体太多（3万多），导致编译时间较长，内存占用也很惊人（接近1G），如果使用要关掉没用的shader_feature,比如：==**_PARALLAXMAP、SHADOWS_SOFT、DIRLIGHTMAP_COMBINED DIRLIGHTMAP_SEPARATE、_DETAIL_MULX2、_ALPHAPREMULTIPLY_ON；另外要去掉多余的pass** #F44336==
- shaderforge、Amplify Shader Editor生成的shader有多余代码要程序专门优化，Amplify Shader Editor功能更强大一些，而且开源，建议学习。
- 不要用unity自带terrian，因为即使只用3张splat图，shader也是对应4个的，建议T4M或者转为mesh。
- 模型和材质相同且数量巨大时用Instance来优化，比如草。
- 利用查找纹理(LUT)来优化复杂的光照渲染，比如：皮肤、头发、喷漆等。
- 尽量不要使用Procedural Sky，计算瑞丽散射和米氏散射效率比较低。
- 尽量不要使用speedtree，改为模型加简单树叶动画，不过SpeedTreeWind.cginc里面的动画函数很丰富，- TerrianEngine中的SmoothTriangleWave很好用。
- 多用调试工具检查shader性能，常用工具有：FrameDebug、Nsight、RenderDoc 、AMD GPU -ShaderAnalyzer / PVRShaderEditor、Adreno Profiler 、腾讯Cube、UWA等；另外可以内置GM界面，比如开关阴影，批量替换shader等方便真机调试。

> 另一方面，Matcap是完全不考虑光照影响的渲染方法，因此也不存在能量守恒，只能通过采样贴图的绘制做出能量守恒的效果，所以不是真正的PBR，也因此能做出很多PBR无法实现的效果。



2.脚本

减少GetComponent、find等查找函数在Update等循环函数中的调用、go.CompareTag代替go.tag 、
减少SendMessage等同步函数调用；减少字符串连接；for代替foreach，5.5以后版本foreach已经优化过了；少用linq；
大资源改为异步加载
合理处理协程调用
将AI、网络等放在单独线程
发布优化：关闭log、剔除代码
伪随机
脚本挂载类改为Manager等全局类实现
lua中尽量不实现update、fixedupdate等循环函数，lua和csharp互调用的效率比较低。

3.内存管理

池子管理粒子、float UI等小资源，频繁地GC会造成卡顿
必要时主动调用GC.Collect()
按照不同资源、不同设备管理资源生命周期，Resources.Load和Assetbundle统一接口，利用引用计数来管理生命周期，并打印和观察生命周期。保证资源随场景而卸载，不常驻内存，确定哪些是预加载，哪些泄漏。
内存泄漏（减少驻留内存）：Container内资源不remove掉用Resources.UnloadUnusedAssets是卸载不掉的；对于这种情况，建议直接通过Profiler Memory中的Take Sample来对其进行检测，通过直接查看WebStream或SerializedFile中的AssetBundle名称，即可判断是否存在“泄露”情况；通过Android PSS/iOS Instrument反馈的App线程内存来查看；
堆内存过大：避免一次性堆内存的过大分配，Mono的堆内存一旦分配，就不会返还给系统，这意味着Mono的堆内存是只升不降的。常见：高频调用new；log输出；
CPU占用高：NGui的重建网格导致UIPanel.LateUpdate（按照静止、移动、高频移动来切分）；NGUI锚点自身的更新逻辑也会消耗不少CPU开销。即使是在控件静止不动的情况下，控件的锚点也会每帧更新（见UIWidget.OnUpdate函数），而且它的更新是递归式的，使CPU占用率更高。因此我们修改了NGUI的内部代码，使锚点只在必要时更新。一般只在控件初始化和屏幕大小发生变化时更新即可。不过这个优化的代价是控件的顶点位置发生变化的时候（比如控件在运动，或控件大小改变等），上层逻辑需要自己负责更新锚点。 加载用协程； 控制同一个UIPanel中动态UI元素的数量，数量越多，所创建的Mesh越大，从而使得重构的开销显著增加。比如，战斗过程中的HUD血条可能会大量出现，此时，建议研发团队将运动血条分离成不同的UIPanel，每组UIPanel下5~10个动态UI为宜。这种做法，其本质是从概率上尽可能降低单帧中UIPanel的重建开销。
资源冗余：AssetBundle打包打到多份中；动态修改资源导致的Instance拷贝多份（比如动态修改材质，Renderer.meterial，Animation.AddClip）。
磁盘空间换内存：对于占用WebStream较大的AssetBundle文件（如UI Atlas相关的AssetBundle文件等），建议使用LoadFromCacheOrDownLoad或CreateFromFile来进行替换，即将解压后的AssetBundle数据存储于本地Cache中进行使用。这种做法非常适合于内存特别吃紧的项目，即通过本地的磁盘空间来换取内存空间

4.美术

建立资源审查规范和审查工具：PBR材质贴图制作规范、场景制作资源控制规范、角色制作规范、特效制作规范；利用AssetPostprocessor建立审查工具。
压缩纹理、优化精灵填充率、压缩动画、压缩声音、压缩UI（九宫格优于拉伸）；严格控制模型面数、纹理数、角色骨骼数。
粒子：录制动画代替粒子、减少粒子数量、粒子不要碰撞
角色：启用Optimize Game Objects减少节点,使用（SimpleLOD、Cruncher）优化面数。
模型：导入检查Read/Write only、Optimize Mesh、法线切线、color、禁用Mipmap
压缩纹理问题：压缩可能导致色阶不足；无透明通道用ETC1,现在安卓不支持ETC2已不足5%，建议放弃分离通道办法。
UI：尽可能将动态UI元素和静态UI元素分离到不同的UIPanel中（UI的重建以UIPanel为单位），从而尽可能将因为变动的UI元素引起的重构控制在较小的范围内； 尽可能让动态UI元素按照同步性进行划分，即运动频率不同的UI元素尽可能分离放在不同的UIPanel中； 尽可能让动态UI元素按照同步性进行划分，即运动频率不同的UI元素尽可能分离放在不同的UIPanel中；
ugui：可以充分利用canvas来切分不同元素。
大贴图会导致卡顿，可以切分为多个加载。
iOS使用mp3压缩、Android使用Vorbis压缩


5.批次

开启static batch
开启dynamic batch：要求模型小于900顶点，用法线小于300，用切线小于180，缩放不一致、使用lightmap、多通道材质等会使dynamic batch无效。
减少GameObject，场景模型数量对fps影响巨大。
批次不是越少越好，过大的渲染数据会给总线传输带来压力。

6.物理

不需要移动的物体设为Static
不要用Mesh碰撞，角色不用碰撞体
触发器逻辑优化
寻路频率、AI逻辑频率 、Fixed Timestep、降帧到30
出现卡顿的复杂计算，例如寻路、大量资源加载 可以用分帧或者协成异步来处理