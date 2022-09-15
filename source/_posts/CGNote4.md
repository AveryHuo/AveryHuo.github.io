---
title: 计算机图形学编程笔记4
cover: /img/1608804894728513114.png
categories:
- 图形学
tags: 
- 图形学
katex: true
top_img: 'linear-gradient(20deg, #0062be, #925696, #cc426e, #fb0347)'
description: CG笔记4
keywords: "CG, 图形学, opengl"
date: 2022-09-14 18:23:51
updated: 2022-09-15 16:33:44
sticky: 1
---

本笔记针对 GLSL-PathTracer源码学习
主要使用opengl实现

> opencl： computing language 专注处理GPGPU情况，让显卡更能处理图形以外的计算, opencv， 图片分析的库，用于数字处理等。


# 一、各格式文件介绍
gltf：
https://zhuanlan.zhihu.com/p/65265611
https://github.com/KhronosGroup/glTF/blob/main/specification/2.0/figures/gltfOverview-2.0.0b.png

![gltf格式文件](/img/1608804894728513114.png)

本质上是一个JSON文件。这一文件描述了整个3D场景的内容。它包含了对场景结构进行描述的场景图。场景中的3D对象通过场景结点引用网格进行定义。材质定义了3D对象的外观，动画定义了3D对象的变换操作(比如选择、平移操作)。蒙皮定义了3D对象如何进行骨骼变换，相机定义了渲染程序的视锥体设置。

glb文件： 二进制版的gltf

scene文件： 纯文件记录文件

hdr文件：环境贴图

# 二、第三方插件
* TinyGLTF： 加载gltf model文件
* Tinydir： https://github.com/cxong/tinydir 用于快速读取文件夹
* Tinyobjloader: https://github.com/tinyobjloader/tinyobjloader obj加载器
* stb: image加载器
* RadeonRays： 实现了一套bvh相关的框架
* oidn:开源渲染去噪系统Open Image Denoise（OIDN）
* imguizmo: Immediate mode 3D gizmo for scene editing and other controls based on Dear Imgui
* imgui: 实时GUI框架
* gl3w: 一个获取opengl函数地址的库（gl3w is the easiest way to get your hands on the functionality offered by the OpenGL core profile specification.）参考：https://blog.csdn.net/Weies/article/details/116103739
* SDL2: Simple DirectMedia Layer的缩写，相类似的有glfw，简单直接的多媒体层，不仅包括图像处理，音频处理，输入输出，还支持多线程和事件的开发，而且SDL是跨平台的。因为SDL开源性质，所以非常多的应用都是用SDL作为底层。参考： https://zhuanlan.zhihu.com/p/428302382


# 三、主体流程

1. 加载Scene
2. SDL创建主window，得到全局SDL_GLContext
3. 初始化gl3w
4. 初始化imgui,并与sdl和gl3w的对象绑定
5. 初始化Renderer对象，shader的Program初始化也在这里
6. 进入主循环UPDATE: MainLoop(window, context)
7. 删除renderer对象，清理gl对象，sdl对象，删除窗口

# 四、MainLoop流程详细

1. while处理完所有SDL_Event
2. imgui大循环处理所有事件
3. Update 处理imgui的鼠标事件，最后执行renderer的Update：
   ![Update流程](/img/1608804894728513116.png)
        object的transform发生变动: scene->instancesModified?
            更新transform, materials, BVH

        添加新的envMap时： scene->envMapModified?
            envmap的加载和shader应用
        界面选项：scene->enableDenoiser?
            应用oidn的Denoiser
        
        scene->dirty?
            这里直接清空所有 gl buffer空间，准备re-render
        没有dirty?
            检测tile.y小于0时，这时帧率增加，表示已经渲染完一帧
        更新Shader（Use, stopUse）
4. 执行Renderer渲染
    Renderer类中的Quad负责绘制
    scene->dirty?
        应用 pathTraceShaderLowRes 绘制
    没有dirty?
        应用 PathTraceShader 绘制
        应用 outputShader 绘制
        应用 tonemapShader 绘制
5. SDL_GL_SwapWindow(window)

# 五、GLSL实现的Path trace
