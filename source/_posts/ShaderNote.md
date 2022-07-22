---
title: Shader学习笔记
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- 图形学
tags: 
- 图形学
---

==本篇主要针对shader #2196F3==

## 参考文献
[Unity] - Technical Artist in Shading and Effects
https://certification.unity.com/products/expert-technical-artist-shading-effects
[虚幻] - 虚幻引擎职业讲堂：技术美术师
https://www.unrealengine.com/zh-CN/tech-blog/jobs-in-unreal-engine---technical-artist?sessionInvalidated=true
[Catlike] - Catlike大神的Unity系列教程
https://catlikecoding.com/unity/tutorials/
[霜狼_may] - TA技术美术学习体系框架
https://www.bilibili.com/video/av77755500
[毛星云] - 浅墨的游戏编程
https://zhuanlan.zhihu.com/game-programming
[云影] - 技术美术的魔法工坊
https://zhuanlan.zhihu.com/c_1082217056598007808
[一只大熊猫]-中国特色技术美术
https://zhuanlan.zhihu.com/c_1078237708161363968
[知乎] - 技术美术会是一个长期存在的职业吗？
https://www.zhihu.com/question/325535382/answer/1149431577
[马甲] - 总结一些TA（技术美术）学习的网站
https://zhuanlan.zhihu.com/p/84550677
[书籍] - 《OpenGL 编程指南》红宝书
https://book.douban.com/subject/26220248/
[书籍] - 《OpenGL 超级宝典》蓝宝书
https://book.douban.com/subject/10774590/
[书籍] - 《DirectX 9.0 3D游戏开发编程基础》
https://book.douban.com/subject/2111771/
[书籍] - 計算機圖形: 入門/API類
https://www.douban.com/doulist/1445744/

## 一、内置shader库

### Unity支持的語義

* 1，从应用阶段传递模型数据给顶点着色器时支持的语义如下表
  
  
|语义	|描述|
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
|POSITION	  |模型空间中的顶点位置 通常float4  |
|NORMAL	  |   顶点法线 通常float3|
|TANGENT	|顶点切线 通常float4|
TEXCOORD(n)	|该顶点的纹理坐标 n组|
|COLOR	|顶点颜色 通常fixed4 float4|

* 2，丛顶点着色器传递到片元着色器时支持的语义如下表：
 
|语义	|描述|
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| SV_POSITION	| 裁剪空间中的顶点坐标 结构体必须包含一个该词修饰的变量| 
| COLOR0	| 通常用于输出第一组顶点颜色| 
| COLOR1	| 通常用于输出第二组顶点颜色| 
| TEXCOORDN（0~7）	| 通常用于输出纹理坐标| 
  
  
* 3，片元着色器输出时支持的语义
  
|语义	|描述|
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| SV_Target| 	输出值将会存储到渲染目标中| 

* 4. 數據類型對比

|类型	|精度|
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
|float	|最高精度 通常32位|
|half	|中等精度 通常16位|
|fixed	|最低精度 通常11位|

### 常用数学函数

| 函数	| 说明	| 实例| 
| ----------|----------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| radians(degree)	| 角度变弧度(一般默认都用弧度)	|  
| degrees(radian)	| 弧度变角度	|  
| sin(angle), cos(angle), tan(angle)	| 三角函数	|  
| asin(x)| 	arc sine, 返回弧度 \[-PI/2, PI/2];	|  
| acos(x)	| arc cosine,返回弧度 \[0, PI]	|  
| atan(y, x)	| arc tangent, 返回弧度 \[-PI, PI];	|  
| atan(y/x)	| arc tangent, 返回弧度 \[-PI/2, PI/2];	|  
| pow(x, y)	| x的y次方	|  
| exp(x)	| 指数, log(x)	|  
| exp2(x)| 	2的x次方， log2(x)	|  
| sqrt(x)	| x的根号；	|  
| inversesqrt(x)| 	x根号的倒数	|  
| abs(x)| 	绝对值	|  
| sign(x)| 	取当前数值的正负符号,返回 1, 0 或 -1	|  （x>0;x=0;x<0）|  
| floor(x)	| 底部取整	|  
| ceil(x)	| 顶部取整	|  
| fract(x)	| 取小数部分	|  
| mod(x, y)	| 取模， x - y\*floor(x/y)	|  
| min(x, y)	| 取最小值	|  
| max(x, y)| 	取最大值	|  
| clamp(x, min, max)	| min(max(x, min), max);	|  
| mix(x, y, a)| 	x, y的线性混叠， x(1-a) + y\*a;	|  
| step(edge, x)| 	如 x smoothstep(edge0, edge1, x): threshod smooth transition时使用。 edge0<=edge0时为0.0， x>=edge1时为1.0	|  
| length(x)	| 向量长度	|  
| distance(p0, p1)| 	两点距离， length(p0-p1);	|  
| dot(x, y)	| 点积，各分量分别相乘 后 相加	|  
| cross(x, y)	| 差积 | 	x\[1]\*y\[2]-y\[1]\*x\[2], x\[2]\*y\[0] - y\[2]\*x\[0], x\[0]\*y\[1] - y\[0]\*x\[1] |  
| normalize(x)	| 归一化| 	length(x)=1;| 
| faceforward(N, I, Nref)| 	如 dot(Nref, I)< 0则N, 否则 -N	| 
| reflect(I, N)	| I的反射方向| 	I -2\*dot(N, I)\*N, N必须先归一化| 
| refract(I, N, eta)| 	折射	| k=1.0-etaeta(1.0 - dot(N, I) * dot(N, I)); 如k<0.0 则0.0，否则 etaI - (etadot(N, I)+sqrt(k))\*N| 
| matrixCompMult(matX, matY)| 	矩阵相乘, 每个分量 自行相乘	| r\[j] = x\[j]\*y\[j];| 
| lessThan(vecX, vecY)	| 向量 每个分量比较 x < y	| 
| lessThanEqual(vecX, vecY)| 	向量 每个分量比较 x<=y	| 
| greaterThan(vecX, vecY)	| 向量 每个分量比较 x>y	| 
| greaterThanEqual(vecX, vecY)	| 向量 每个分量比较 x>=y	| 
| equal(vecX, vecY)	| 向量 每个分量比较 x==y	| 
| notEqual(vecX, vexY)| 	向量 每个分量比较 x!=y| 	
| any(bvecX)	| 只要有一个分量是true， 则true	| 
| all(bvecX)	| 所有分量是true， 则true	| 
| not(bvecX)	| 所有分量取反| 


### 1. UnityCG.cginc 
* 包含最常用的帮助函数，宏，结构钵
*  数据结构:
struct appdata_base：顶点着色器输入，包含位置、法线和一个纹理坐标。
struct appdata_tan：顶点着色器输入，包含位置、法线、切线和一个纹理坐标。
struct appdata_full：顶点着色器输入，包含位置、法线、切线、顶点颜色和两个纹理坐标。
struct appdata_img: 顶点着色器输入，包含位置和一个纹理坐标。

* 顶点变换函数
 

| 功能                                    | 描述                                                                                                                       |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| float4 UnityObjectToClipPos(float3 pos) | 将对象空间中的点变换到齐次坐标中的摄像机裁剪空间。这等效于 mul(UNITY_MATRIX_MVP, float4(pos, 1.0))，应该在适当的位置使用。 |
| float3 UnityObjectToViewPos(float3 pos) | 将对象空间中的点变换到视图空间。这等效于 mul(UNITY_MATRIX_MV, float4(pos, 1.0)).xyz，应该在适当的位置使用。                |


* 通用helper函数
  
| 功能	| 描述| 
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| float3 WorldSpaceViewDir (float4 v)	| 返回从给定对象空间顶点位置朝向摄像机的世界空间方向（未标准化）。| 
| float3 ObjSpaceViewDir (float4 v)	| 返回从给定对象空间顶点位置朝向摄像机的对象空间方向（未标准化）。| 
| float2 ParallaxOffset (half h, half height, half3 viewDir)	| 计算视差法线贴图的 UV 偏移。| 
| fixed Luminance (fixed3 c)	| 将颜色转换为亮度（灰阶）。| 
| fixed3 DecodeLightmap (fixed4 color)	| 从 Unity 光照贴图（RGBM 或 dLDR，具体取决于平台）解码颜色。| 
| float4 EncodeFloatRGBA (float v)	| 将 \[0..1) 范围浮点数编码为 RGBA 颜色，用于存储在低精度渲染目标中。| 
| float DecodeFloatRGBA (float4 enc)	| 将 RGBA 颜色解码为浮点数。| 
| float2 EncodeFloatRG (float v)	| 将 \[0..1) 范围浮点数编码为 float2。| 
| float DecodeFloatRG (float2 enc)	| 解码先前编码的 RG 浮点数。| 
| float2 EncodeViewNormalStereo (float3 n)	| 将视图空间法线编码为 0 到 1 范围内的两个数字。| 
| float3 DecodeViewNormalStereo (float4 enc4)	| 从 enc4.xy 解码视图空间法线。| 

* 仅支持前向渲染的helper函数， 仅当使用前向渲染（ForwardBase 或 ForwardAdd 通道类型）时，这些函数才有用。

| 功能	| 描述| 
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| float3 WorldSpaceLightDir (float4 v)	| 根据给定的对象空间顶点位置计算朝向光源的世界空间方向（未标准化）。| 
| float3 ObjSpaceLightDir (float4 v)	| 根据给定对象空间顶点位置计算朝向光源的对象空间方向（未标准化）。| 
| float3 Shade4PointLights (...)	| 计算四个点光源的光照，将光源数据紧密打包到矢量中。前向渲染使用它来计算每顶点光照。| 

* 屏幕空间用的helper函数
* 以下 helper 函数可计算用于采样屏幕空间纹理的坐标。它们返回 float4，其中用于纹理采样的最终坐标可以通过透视除法（例如 xy/w）计算得出。
 
 | 功能	| 描述| 
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
|float4 ComputeScreenPos (float4 clipPos)	| 计算用于执行屏幕空间贴图纹理采样的纹理坐标。输入是裁剪空间位置。| 
|float4 ComputeGrabScreenPos (float4 clipPos)	| 计算用于 GrabPass 纹理采样的纹理坐标。输入是裁剪空间位置。| 

* UnityCG.cginc 中的顶点光照 helper 函数：
* 仅当使用每顶点光照着色器（“Vertex”通道类型）时，这些函数才有用。

 | 功能	| 描述| 
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| float3 ShadeVertexLights (float4 vertex, float3 normal)	| 根据给定的对象空间位置和法线计算四个每顶点光源和环境光的光照。| 

### 2. UnityShaderVariables.cginc 【自动添加】
 * 包含常用的内置全局变量，如UNITY_MATRIX_MVP

### 3. HLSLSupport.cginc 【自动添加】
 * 跨平台用的宏和帮助定义
  
### 4. AutoLight.cginc 【表面着色器使用】
* 光照和阴影的函数库

### 5. Lighting.cginc 【表面着色器自动添加】
 * 包含标准表面着色器的光照模型
   
### 6. TerrainEngine.cginc 
* 提供为地形vegetation相关shader的帮助函数



## 二、 基础的光照模型

### Unlit 頂點著色器模板：

``` c
Shader "Unlit/MyShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
		_SpecularColor("Specular",color)=(1,1,1,1)
		_Shininess("Shininess",range(1,64))=8
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
             CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
			#include "Lighting.cginc"
            struct v2f
            {
            	float3 normal:NORMAL;
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float4 vertex : TEXCOORD1;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
			float4 _SpecularColor;
			float _Shininess;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.vertex = v.vertex;
                o.normal = v.normal;
                o.uv = TRANSFORM_TEX(v.texcoord.xy, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                // sample the texture
                fixed4 col = tex2D(_MainTex, i.uv);

                // 在这里实现光照

                return col;
            }
            ENDCG
        }
    }
}

```

### 1. Lambert 漫反射模型
* 最基础的光照模型: 法向量与入射光的点积作为反射光
* 将反射光乘上主色再乘上环境即可

``` c
 fixed4 frag (v2f i) : SV_Target
{
	// sample the texture
	fixed4 col = tex2D(_MainTex, i.uv);

	//获取法向量
	float3 N = UnityObjectToWorldNormal(i.normal);
	//获取入射光
	float3 L = normalize(WorldSpaceLightDir(i.vertex));

	// Diffuse:
	float diffuseScale = saturate(dot(N,L));
	col = UNITY_LIGHTMODEL_AMBIENT + _LightColor0* col * diffuseScale;


	return col;
}
```

### 2. Phong 镜面反射模型
``` c
fixed4 frag (v2f i) : SV_Target
{
	// sample the texture
	fixed4 col = tex2D(_MainTex, i.uv);

	//获取法向量
	float3 N = UnityObjectToWorldNormal(i.normal);
	//获取入射光
	float3 L = normalize(WorldSpaceLightDir(i.vertex));
	//视角坐标
	float3 V = normalize(WorldSpaceViewDir(i.vertex));

	// Diffuse:
	float diffuseScale = saturate(dot(N,L));
	col = UNITY_LIGHTMODEL_AMBIENT + _LightColor0* col * diffuseScale;

	//Phong:
	float3 R = -reflect(L,N); // reflect(I,N) = 2* dot(N,L)*N - L;
	R = normalize(R);
	float specularScale = pow(saturate(dot(V,R)),_Shininess);
	col += _SpecularColor*specularScale;

	return col;
}
```

### 3. Blin-Phong 半角镜面反射模型

``` c
fixed4 frag (v2f i) : SV_Target
{
	// sample the texture
	fixed4 col = tex2D(_MainTex, i.uv);

	//获取法向量
	float3 N = UnityObjectToWorldNormal(i.normal);
	//获取入射光
	float3 L = normalize(WorldSpaceLightDir(i.vertex));
	//视角坐标
	float3 V = normalize(WorldSpaceViewDir(i.vertex));

	// Diffuse:
	float diffuseScale = saturate(dot(N,L));
	col = UNITY_LIGHTMODEL_AMBIENT + _LightColor0* col * diffuseScale;

	//Phong:
	// float3 R = -reflect(L,N); // reflect(I,N) = 2* dot(N,L)*N - L;
	// R = normalize(R);
	// float specularScale = pow(saturate(dot(V,R)),_Shininess);
	// col += _SpecularColor*specularScale;

	//Blin-Phong:
	float3 H =  normalize(L+V);
	float specularScale = pow(saturate(dot(H,N)),_Shininess);
	col += _SpecularColor*specularScale;

	return col;
}
```


### 4. 菲涅尔环境反射

``` c
....
Properties
  {
	  _Color("Color Tint", Color) = (1,1,1,1)
	  _ReflectColor("Reflection Color",Color) = (1,1,1,1)
	  _FresnelScale("Fresnel Scale",range(0,1)) = 0.5
	  _CubeMap("Reflection CubeMap",cube) = "_skybox"{}
}
.......
 fixed4 frag(v2f i) : SV_Target
    {
        fixed3 worldNormal = normalize(i.worldNormal);
        fixed3 worldViewDir = normalize(i.worldViewDir);
        fixed3 worldLightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));

        fixed3 ambient = UNITY_LIGHTMODEL_AMBIENT.xyz;
        fixed3 col = texCUBE(_CubeMap, i.worldRef).rgb;
        fixed3 reflection = col * _ReflectColor.rgb;

        fixed3 diffuse = _LightColor0.rgb*_Color.rgb*saturate(dot(worldNormal, worldLightDir));
        fixed fresnel = _FresnelScale + (1 - _FresnelScale)*pow(1 - dot(worldViewDir, worldNormal), 5);

        UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);
        fixed3 color = ambient + lerp(diffuse, reflection, saturate(fresnel))*atten;
        return fixed4(color,1.0);
    }
```