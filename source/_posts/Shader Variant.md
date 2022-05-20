---
title: Shader Variant
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---

#### multi_compile与shader_feature

multi_compile与shader_feature可在shader中定义宏。两者区别如下图所示：

|              | multi_compile           | shader_feature           |
| ------------ | ----------------------- | ------------------------ |
| 定义方式     | #pragma multi_compile A | #pragma shader_feature A |
| 宏的适用范围 | 大多数shader            | 一般仅针对shader自身     |
| 变体的生成   | 生成所有的变体          | 可自定义生成何种变体     |
| 默认定义的宏 | 默认定义首个宏          | 默认定义首个宏           |


1. 定义方式
定义方式中值得注意的是，#pragma shader_feature A其实是 #pragma shader_feature _ A的简写，下划线表示未定义宏(nokeyword)。因此此时shader其实对应了两个变体，一个是nokeyword，一个是定义了宏A的。
而#pragma multi_compile A并不存在简写这一说，所以shader此时只对应A这个变体。若要表示未定义任何变体，则应写为 #pragma multi_compile __ A。

2. 宏的适用范围
multi_compile定义的宏，如#pragma multi_compile_fog，#pragma multi_compile_fwdbase等，基本上适用于大部分shader，与shader自身所带的属性无关。
shader_feature定义的宏多用于针对shader自身的属性。比如shader中有_NormalMap这个属性(Property)，便可通过#pragma shader_feature _NormalMap来定义宏，用来实现这个shader在material有无_NormalMap时可进行不同的处理。

3. 变体的生成
#pragma multi_compile A B C
#pragma multi_compile D E
则此时会生成 A D、A E、B D、B E、C D、C E这6中变体。
shader_feature要生成何种变体可用shader variant collection进行自定义设置。

4. 默认定义的宏
当material中的keywords无法对应shader所生成的变体时，Unity便会默认定义宏定义语句中的首个宏，并运行相应的变体来为这个material进行渲染。
multi_compile与shader_feature都默认定义首个宏。

#### 如何控制项目中Shader变体的生成

| 生成方式                                              | 优点                                             | 缺点                                                                                                                       |
| ----------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| shader与material打在一个包中                          | 变体根据material中的keywords自动生成             | 多个不同的material包中可能存在相同的shader变体，造成资源冗余，若在程序运行时动态改变material的keyword其变体可能并没有被生成 |
| Shader单独打包，使用multi_compile定义全部宏           | 全部变体都被生成，不会发生需要的变体未生成的情况 |                                                                                                                          生成的变体数量庞大，严重浪费资源   |
| Shader单独打包，shader_feature与multi_compile结合使用 | 能够有效控制变体数量                             |                                                                                                                            如何确定哪些变体需要生成，容易遗漏需要生成的变体|


#### Shader编写规范

1. 建议使用shader_feature时将定义语句写成完整模式，并且不要在一个语句中定义多个宏。
完整模式：#pragma shader_feature _ A，不建议写成#pragma shader_feature A。
不建议在一个语句中定义多个宏，如： #pragma shader_feature _ A B C，若一定要定义多个宏，请务必将其写成完整模式，不使用完整模式在切换shader时可能会与想要的效果不一致，具体原因尚未测得。

2. 若在shader中使用shader_feature，请为这个shader指定一个CustomEditor
每个使用shader_feature来定义Keyword的shader都需要再末尾加个 CusomEditor “xxxx”，并在代码中实现类xxxx(需继承自UnityEditor.ShaderGUI)，用来对Keywords定义进行设定。
这么做是因为Material中的部分Keyword是由shader中的属性(Properties)所控制的。比如shader中含有_NormalMap的属性并且定义了与_NormalMap相关的Keyword，这个Keyword需要在Material含有NormalMap时添加，不含NormalMap时移除。这个功能可由自定义的CustomEidtor实现。
具体如何写这个CustomEditor类可参考Unity builtin_shaders\Editor\StandardShaderGUI.cs。该文件可去Unity官网下载，下载时选择内置着色器即可。