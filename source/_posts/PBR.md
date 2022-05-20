---
title: 基于物理的渲染-PBR
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1608604177769.png
categories:
- Unity
---

## 一、PBR核心理论

### 1. 基础理念
* 微平面理论（Microfacet Theory）。微平面理论是将物体表面建模成做无数微观尺度上有随机朝向的理想镜面反射的小平面（microfacet）的理论。在实际的PBR 工作流中，这种物体表面的不规则性用粗糙度贴图或者高光度贴图来表示。
* 能量守恒（Energy Conservation）。出射光线的能量永远不能超过入射光线的能量。随着粗糙度的上升镜面反射区域的面积会增加，作为平衡，镜面反射区域的平均亮度则会下降。
* 菲涅尔反射（Fresnel Reflectance）。光线以不同角度入射会有不同的反射率。相同的入射角度，不同的物质也会有不同的反射率。万物皆有菲涅尔反射。F0是即 0 度角入射的菲涅尔反射值。大多数非金属的F0范围是0.02~0.04，大多数金属的F0范围是0.7~1.0。
* 线性空间（Linear Space）。光照计算必须在线性空间完成，shader 中输入的gamma空间的贴图比如漫反射贴图需要被转成线性空间，在具体操作时需要根据不同引擎和渲染器的不同做不同的操作。而描述物体表面属性的贴图如粗糙度，高光贴图，金属贴图等必须保证是线性空间。
* 色调映射（Tone Mapping）。也称色调复制（tone reproduction），是将宽范围的照明级别拟合到屏幕有限色域内的过程。因为基于HDR渲染出来的亮度值会超过显示器能够显示最大亮度，所以需要使用色调映射，将光照结果从HDR转换为显示器能够正常显示的LDR。
* 物质的光学特性（Substance Optical Properties）。现实世界中有不同类型的物质可分为三大类：绝缘体（Insulators），半导体（semi-conductors）和导体（conductors）。在渲染和游戏领域，我们一般只对其中的两个感兴趣：导体（金属）和绝缘体（电解质，非金属）。其中非金属具有单色/灰色镜面反射颜色。而金属具有彩色的镜面反射颜色。

### 2.PBR范畴
寒霜(Frostbite)引擎在SIGGRAPH 2014的分享《Moving Frostbite to PBR》中提出，基于物理的渲染的范畴，由三部分组成：

* 基于物理的材质（Material）
* 基于物理的光照（Lighting）
* 基于物理适配的摄像机（Camera）


## 二、渲染方程 BxDF

### 1.渲染方程与反射方程

* 渲染方程
物理基础是能量守恒定律：　在一个特定的位置和方向，出射光 Lo 是自发光 Le 与反射光线之和，反射光线本身是各个方向的入射光 Li 之和乘以表面反射率及入射角。

![某一点的渲染方程](/img/1608604177769.png)

* 反射方程
 
 在实时渲染中，我们常用的反射方程(The Reflectance Equation)，则是渲染方程的简化的版本，或者说是一个特例：
 ![某一点的反射方程](/img/1608604253600.png)
 
 ### 2. BxDF
 
 ![BxDF](/img/1608604419905.png)
 
 BxDF一般而言是对BRDF、BTDF、BSDF、BSSRDF等几种双向分布函数的一个统一的表示。
其中，BSDF可以看做BRDF和BTDF更一般的形式，而且BSDF = BRDF + BTDF。
而BSSRDF和BRDF的不同之处在于，BSSRDF可以指定不同的光线入射位置和出射位置。
> 在上述这些BxDF中，BRDF最为简单，也最为常用。因为游戏和电影中的大多数物体都是不透明的，用BRDF就完全足够。而BSDF、BTDF、BSSRDF往往更多用于半透明材质和次表面散射材质。

## 三、迪士尼原则的BxDF

基于物理的渲染，其实早在20世纪就已经在图形学业界有了一些讨论，2010年在SIGGRAPH上就已经有公开讨论的Course 《SIGGRAPH 2010 Course: Physically-Based Shading Models in Film and Game Production》，而直到2012~2013年，才正式进入大众的视野，渐渐被电影和游戏业界广泛使用。

迪士尼动画工作室则是这次PBR革命的重要推动者。迪士尼的Brent Burley于SIGGRAPH 2012上进行了著名的talk《Physically-based shading at Disney》，提出了迪士尼原则的BRDF（Disney Principled BRDF）， 由于其高度的通用性，将材质复杂的物理属性，用非常直观的少量变量表达了出来（如金属度metallic和粗糙度roughness），在电影业界和游戏业界引起了不小的轰动。从此，基于物理的渲染正式进入大众的视野。

## 3.1 迪士尼的BRDF
在2012年迪士尼原则的BRDF被提出之前，基于物理的渲染都需要大量复杂而不直观的参数，此时PBR的优势，并没有那么明显。

在2012年迪士尼提出，他们的着色模型是艺术导向（Art Directable）的，而不一定要是完全物理正确（physically correct）的，并且对微平面BRDF的各项都进行了严谨的调查，并提出了清晰明确而简单的解决方案。

> 迪士尼的理念是开发一种“原则性”的易用模型，而不是严格的物理模型。正因为这种艺术导向的易用性，能让美术同学用非常直观的少量参数，以及非常标准化的工作流，就能快速实现涉及大量不同材质的真实感的渲染工作。而这对于传统的着色模型来说，是不可能完成的任务。

> 迪士尼原则的BRDF（Disney Principled BRDF）核心理念如下：
* 应使用直观的参数，而不是物理类的晦涩参数。
* 参数应尽可能少。
* 参数在其合理范围内应该为0到1。
* 允许参数在有意义时超出正常的合理范围。
* 所有参数组合应尽可能健壮和合理。

颜色参数（baseColor）和下面描述的十个标量参数：

* baseColor（基础色）：表面颜色，通常由纹理贴图提供。
* subsurface（次表面）：使用次表面近似控制漫反射形状。
* metallic（金属度）：金属（0 =电介质，1=金属）。这是两种不同模型之间的线性混合。金属模型没有漫反射成分，并且还具有等于基础色的着色入射镜面反射。
* specular（镜面反射强度）：入射镜面反射量。用于取代折射率。
* specularTint（镜面反射颜色）：对美术控制的让步，用于对基础色（base color）的入射镜面反射进行颜色控制。掠射镜面反射仍然是非彩色的。
* roughness（粗糙度）：表面粗糙度，控制漫反射和镜面反射。
* anisotropic（各向异性强度）：各向异性程度。用于控制镜面反射高光的纵横比。（0 =各向同性，1 =最大各向异性）
* sheen（光泽度）：一种额外的掠射分量（grazing component），主要用于布料。
* sheenTint（光泽颜色）：对sheen（光泽度）的颜色控制。
* clearcoat（清漆强度）：有特殊用途的第二个镜面波瓣（specular lobe）。
* clearcoatGloss（清漆光泽度）：控制透明涂层光泽度，0 =“缎面（satin）”外观，1 =“光泽（gloss）”外观。

![Disney BRDF](/img/1608606276958.png)

## 四、漫反射BRDF模型（Diffuse BRDF）

Diffuse BRDF可以分为传统型和基于物理型两大类。其中，传统型主要是众所周知的Lambert。

而基于物理型，从1994年的Oren Nayar开始，这里一直统计到今年（2018年）。

其中较新的有GDC 2017上提出的适用于GGX+Smith的基于物理的漫反射模型（PBR diffuse for GGX+Smith），也包含了最近在SIGGRAPH2018上提出的，来自《使命召唤：二战》的多散射漫反射BRDF（MultiScattrering Diffuse BRDF）：

Oren Nayar[1994]
Simplified Oren-Nayar [2012]
Disney Diffuse[2012]
Renormalized Disney Diffuse[2014]
Gotanda Diffuse [2014]
PBR diffuse for GGX+Smith [2017]
MultiScattrering Diffuse BRDF [2018]


## 五、镜面反射BRDF模型（Specular BRDF）

基于物理的渲染领域中最活跃，最主要的部分。
游戏业界目前最主流的基于物理的镜面反射BRDF模型是基于微平面理论（microfacet theory）的Microfacet Cook-Torrance BRDF。

![Cook-Torrance的BRDF公式](/img/1608610266103.png)

![展开反射方程](/img/1608610379037.png)

由于假设微观几何尺度明显大于可见光波长，因此可以将每个表面点视为光学平坦的。 如上文所述，光学平坦表面将光线分成两个方向：反射和折射。

每个表面点将来自给定进入方向的光反射到单个出射方向，该方向取决于微观几何法线（microgeometry normal）m的方向。 在计算BRDF项时，指定光方向l和视图方向v。 这意味着所有表面点，只有那些恰好正确朝向可以将l反射到v的那些小平面可能有助于BRDF值（其他方向有正有负，积分之后，相互抵消）。

在下图中，我们可以看到这些“正确朝向”的表面点的表面法线m正好位于l和v之间的中间位置。l和v之间的矢量称为半矢量（half-vector）或半角矢量（half-angle vector）; 我们将其表示为h。
![有效的BRDF贡献点](/img/1608607466758.png)

并非所有m = h的表面点都会积极地对反射做出贡献;一些被l方向（阴影shadowing），v方向（掩蔽masking）或两者的其他表面区域阻挡。Microfacet理论假设所有被遮蔽的光（shadowed light）都从镜面反射项中消失;实际上，由于多次表面反射，其中一些最终将是可见的，但这在目前常见的微平面理论中一般并未去考虑，各种类型的光表面相互作用如下图所示。

![m=h的表面并全是BRDF贡献点](/img/1608607682403.png)

### 5.1 从物理现象到BRDF

其实可理解为金属质感
![Specular BRDF公式](/img/1608607797277.png)

其中：

* D(h) : 法线分布函数 （Normal Distribution Function），描述微面元法线分布的概率，即正确朝向的法线的浓度。即具有正确朝向，能够将来自l的光反射到v的表面点的相对于表面面积的浓度。
* F(l,h) : 菲涅尔方程（Fresnel Equation），描述不同的表面角下表面所反射的光线所占的比率。
* G(l,v,h) : 几何函数（Geometry Function），描述微平面自成阴影的属性，即m = h的未被遮蔽的表面点的百分比。
* 分母 4(n·l)(n·v）：校正因子（correctionfactor），作为微观几何的局部空间和整个宏观表面的局部空间之间变换的微平面量的校正。

>关于Cook-Torrance BRDF，需要强调的两点注意事项：
对于分母中的点积，仅仅避免负值是不够的 ,也必须避免零值。通常通过在常规的clamp或绝对值操作之后添加非常小的正值来完成。
Microfacet Cook-Torrance BRDF是实践中使用最广泛的模型，实际上也是人们可以想到的最简单的微平面模型。它仅对几何光学系统中的单层微表面上的单个散射进行建模，没有考虑多次散射，分层材质，以及衍射。Microfacet模型，实际上还有很长的路要走。

### 5.2 Specular D

法线分布函数（Normal Distribution Function, NDF）D的常见模型可以总结如下：

Beckmann[1963]
Blinn-Phong[1977]
GGX [2007] / Trowbridge-Reitz[1975]
Generalized-Trowbridge-Reitz(GTR) [2012]
Anisotropic Beckmann[2012]
Anisotropic GGX [2015]

![GGX与blinn-phong效果对比](/img/1608608044790.png)

在这里m表示用来与平面上微平面做比较用的中间向量，而a表示表面粗糙度。

> 另外，需要强调一点。Normal Distribution Function正确的翻译是法线分布函数，而不是正态分布函数。google翻译等翻译软件会将Normal Distribution Function翻译成正态分布函数，而不少中文资料就跟着翻译成了正态分布函数，这是错误的。

>镜面分布，从统计学上近似的表示了与向量m取向一致的微平面的比率。举例来说，假设给定向量m，如果我们的微平面中有35%与向量m取向一致，则正态分布函数或者说NDF将会返回0.35
### 5.3 Specular F
菲涅尔效应（Fresnel effect）作为基于物理的渲染理念中的核心理念之一，表示的是看到的光线的反射率与视角相关的现象

菲涅尔项的常见模型可以总结如下：

Cook-Torrance [1982]
Schlick [1994]
Gotanta [2014]

![Schlick公式](/img/1608608155043.png)

![近似方程](/img/1608609564859.png)

![Unity中的F0的线性运算](/img/1608609585831.png)
## 5.4 Specular G

几何项G的常见模型可以总结如下：

Smith [1967]
Cook-Torrance [1982]
Neumann [1999]
Kelemen [2001]
Implicit [2013]

另外，Eric Heitz在[Heitz14]中展示了Smith几何阴影函数是正确且更准确的G项，并将其拓展为Smith联合遮蔽阴影函数（Smith Joint Masking-Shadowing Function），该函数具有四种形式：

分离遮蔽阴影型（Separable Masking and Shadowing）
高度相关掩蔽阴影型（Height-Correlated Masking and Shadowing）
方向相关掩蔽阴影型（Direction-Correlated Masking and Shadowing）
高度-方向相关掩蔽阴影型（Height-Direction-Correlated Masking and Shadowing）

目前较为常用的是其中最为简单的形式，分离遮蔽阴影（Separable Masking and Shadowing Function）。

该形式将几何项G分为两个独立的部分：光线方向（light）和视线方向（view），并对两者用相同的分布函数来描述。根据这种思想，结合法线分布函数（NDF）与Smith几何阴影函数，于是有了以下新的Smith几何项：

Smith-GGX
Smith-Beckmann
Smith-Schlick
Schlick-Beckmann
Schlick-GGX
其中UE4的方案是上面列举中的“Schlick-GGX”，即基于Schlick近似，将k映射为 [公式] ,去匹配GGX Smith方程：

![Schlick-GGX方程](/img/1608608340955.png)