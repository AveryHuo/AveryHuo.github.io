---
title: 计算机图形学编程笔记1
cover: /img/16088048947285131.png
categories:
- 图形学
tags: 
- 图形学
katex: true
top_img: 'linear-gradient(20deg, #0062be, #925696, #cc426e, #fb0347)'
description: CG笔记1
keywords: "CG, 图形学"
date: 2022-05-19 20:58:49
updated: 2022-05-20 17:21:11
---

#### 一、搭建OPENGL 的C++环境

* 1.1 准备工作
 1. VS下的C++环境
 2. 窗口显示库： GLFW 
>GLFW 安装编译的方法，32位使用编译会有问题，这里如果用64的话是： [具体细节](https://www.cnblogs.com/collectionne/p/6937644.html)
>1. 进入GLFW官方网站glfw.org，下载源码
>2.  安装CMAKE，使用CMAKE编译源码生成工程
>3.生成完工程，打开工程，编译生成lib文件

3.扩展库： GLEW，[官网下载]( http://glew.sourceforge.net/) 取出lib和dll文件即可
4.数学库：GLM， 官网下载完即可。
5.纹理库：SOIL2
>SOIL2 安装方法：[具体细节](https://blog.csdn.net/Wonz5130/article/details/82828817)
>1. 下载SOIL2源码
>2.下载premake4
>3.将premake4放到SOIL2的文件夹
>4.终端cd到SOIL2的文件夹，执行命令： premake4 vs2012， 将生成工程文件
>5.打开上面生成的VS工程，编译即可得到库

* 1.2 制作项目模板
1.准备lib文件夹，放glew,glfw, soil2的lib文件
2.准备include文件夹，放GLEW的GL文件夹，GLFW的GLFW文件夹，glm文件夹， SOIL2的SOIL2文件夹。
3.新建VS空C++项目，配置为win32
4.配置项目的VC++的常规里的包含目录，添加Include文件夹
5.链接器配置，常规添加lib文件夹，输入配置前面三个lib文件名加上opengl32.lib

* 1.3 正式的项目开发
1. 使用1.2创建的模板新建工程
2. 拷贝glew32.dll到项目的debug或release目录中。

#### 二、3D图形数据

2.1 绘制流程描述：
* init() 初始化时
* 1. 创建一个缓冲区
* 2. 将顶点数据复制到缓冲区
* display()每帧刷新时。
* 1. 启用缓冲区
* 2. 将缓冲区数据绑定至顶点属性
* 3. 启用顶点
* 4. 使用glDrawArray画出来。

2.2 VAO（Vertex Array Object）, VBO(Vertex Buffer Object)
顶点数据会先放在一个缓冲区，而这个缓冲区就存储在VBO里。同场景可能有多个VBO。
顶点数组对象则是opengl3.0引入的类似于VAO的组织性结构。
>例： 当绘制两个对象时，可以声明两个VBO，一个VAO，glGenVertexArray生成VAO，glBindVertexArray激活VAO与顶点属性关联，再使用glGenBuffers生成缓冲区。

2.3 使用统一变量
在shader中将变量标记为Uniform后，在opengl中使用glGetuniformlocation得到对应的GL 的id。这样再通过glm::value_ptr取出对应的数值指针设值！。
> 统一变量在每次从顶点缓存区拿值时都是不变的，可以理解为常量

2.4 绘制立方体
* 1.VAO,VBO初始化
* 2.从相机的位置获取视角矩阵，V_MATRIX。 使用glm:translate
* 3.从物体位置获取模型矩阵，M_MATRIX。 使用glm:translate
* 4.从窗口，获取到P_MATRIX透视矩阵.。 使用glm:perspective
* 5.将MV,P矩阵传到顶点shader里
 
> 矩阵变换从右往左变换，将transMatrix * rotMatrix。先旋转再变位置。

> 注意shader中的设值：
> ```c++
> 	//VBO关联，顶点着色器的location为0的值被找出来。并从第一个VBO库中将值给过去
> 	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
> 	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
> 	glEnableVertexAttribArray(0);
> ```

>注意Opengl的glm与GLSL中矩阵的定义规则：
> GLSL中的矩阵与GLM都是以列读取的！

```c++
//glm的定义矩阵，以下两个矩阵变量是相同的，且以1,2,3,4为列往后排
glm::mat4 test = {
	{1,2,3,4},
	{5,6,7,8},
	{9,10,11,12},
	{13,14,15,16},
};
glm::mat4 test2 = {
	1,2,3,4,
	5,6,7,8,
	9,10,11,12,
	13,14,15,16,
};
```

2.5 使用矩阵栈来处理分层模型
* 例 ：行星系统的实现流程
* 1. 初始栈，实例一个vMatrix视觉矩阵
* 2. 实现太阳：复制一个到栈顶，生成太阳的MV矩阵，复制一个到栈顶，生成太阳的旋转。画太阳，然后POP出太阳的旋转。
* 3. 当前栈顶的是太阳的MV矩阵。以此复制到栈顶，生成行星的MV矩阵，复制到栈顶，生成行星的旋转。画行星，然后POP出行得的旋转。
* 4. 当前栈顶是行星的MV矩阵，以此复制到栈顶，生成月亮的MV矩阵，生成旋转，生成缩放。
* 5.前面四个步骤，此时栈，共有四个元素。从顶到底分别是，月亮，行星，太阳，视觉矩阵。依次弹出清空栈。
  
2.6 优化策略
  * display帧刷新函数中不要定义或申请变量内存
  * 背面剔除：
  * 1.使用glEnable(GL_CULL_FACE) 激活此功能
  * 2.使用glFrontFace(GL_CCW)设置逆时针为正向
  * 3.使用glCullFace(GL_BACK)将背面剔除（默认）。 GL_FRONT 和GL_FRONT_AND_BACK
   
#### 纹理贴图-使用SOIL2

3.1 使用纹理贴图
* 1.使用SOIL_LOAD_TEXTURE获取到texture ID
* 2.构建纹理坐标，以左下角为0,0为定，右上角为1,1。把纹理2D坐标点与3D模型坐标相映射。
* 3.在display中使用glActiveTexture激活，用glBindTexture(GL_TEXTURE_2D, "注：1中的texture ID")
* 4.vertex shader 收到纹理坐标传至 fragment shader
* 5.fragmenet shader中使用sampler2d采样器，利用4中得到的坐标点取颜色值返回。

3.2 多级渐远纹理贴图 Mipmapping - 避免校正采样误差伪影
* 纹理中存储相同图像的连续一系列较低分辨率副本 。大小将比原图像大1/3
* 如何在OpenGL使用：
* 1.激活纹理。glBindTexture(GL_TEXTURE_2D, textureRef);
* 2.使用glTexParameteri的GL_TEXTURE_MIN_FILTER 指明，四个方法：
* GL_NEAREST_MIPMAP_NEAREST//取最近的纹素
* GL_LINEAR_MIPMAP_NEAREST//线性
* GL_NEAREST_MIPMAP_LINEAR//双线性
* GL_LINEAR_MIPMAP_LINEAR //三线性

3.3 各向异性过滤-AF
恢复MIPMAPPING丢失的细节，标准MipMapping使用正方形分辨率MIP纹理，而AF可以使用各种矩形分辨率来采样。
```c++
if (glewIsSupported("GL_EXT_texture_filter_anisotropic")) {
	cout<<"支持各向异性！"<<endl;
}

```
3.4 环绕和平辅
* 当纹理坐标不是\[0, 1]\的范围时，需要设置填充参数：
* GL_REPEAT, GL_MIRRORED_REPEAT（当奇数时坐标反转）, GL_CLAMP_TO_EDGE（0，1以外强设成边界值）, GL_CLAMP_TO_BORDER(0，1以外的设成颜色)

3.5 透视变形
考虑情形如：矩形棋盘结构的纹理填充，在X轴旋转时将导致三角面交接处发生变形。
默认opengl将会开启透视修复。
> 使用noperspective 禁止opengl透视修复
> ```c++
> noperspective out texcoord;//顶点
> noperspective in texcoord;//片面
> ```

#### 三、数学

1.1 点乘
Dot Product
向量点乘规则：
对应坐标的相乘的和： (x1,y1) Dot (x2,y2) = x1*x2 + y1*y2

向量点乘的几何应用：
1. 查找两个向量之间的夹角
2. 找一个向量到另一个向量的projection
![投影计算示例:](/img/16088048947285131.png)
3.计算两个向量有多接近
4.关于一个前与后的信息
![方向:](/img/16088048947285132.png)

2.2 叉积
Cross Product
叉乘会垂直于初始两个向量
方向取决于右手螺旋定则
当x cross y = +z时，称为右手坐标系
(unity使用左手坐标系)
![方向:](/img/16088048947285133.png)

![属性:](/img/16088048947285134.png)

![坐标相乘公式:](/img/16088048947285135.png)

作用：
1. 判定左右
当a cross b = +z时，a在右
![左右判定:](/img/16088048947285136.png)

2. 判写inside/outside
AB cross AP = +z 同时 BC cross BP == +z 同时 CA cross CP == +z 这时在inside 否则必为outside
![左右判定:](/img/16088048947285137.png)

3. 以任意三个相互垂直的向量创建坐标系
![自定义坐标系表示法:](/img/16088048947285138.png)

2.3 矩阵
相乘，第一个矩阵的对应行的元素，与第二个矩阵的对应列的元素，两两相乘得到结果

> 由此可知，对于想得一个任意行列的一个结果的矩阵值，只需要取第一个矩阵对应行的向量，与第二个矩阵对应列的向量做点积即可！！

属性：
矩阵不支持交互律，但有结合律，A(BC) = (AB)C

转置矩阵：
行和列互换
![转置矩阵:](/img/16088048947285139.png)

单位矩阵：
![3x3的单位矩阵:](/img/160880489472851310.png)
当两个矩阵相乘结果为单位矩阵，且不管顺序，则意为互为逆矩阵

矩阵在向量点乘的意义：
![矩阵在向量点乘的意义:](/img/160880489472851311.png)

矩阵在向量叉乘的意义：
![矩阵在向量叉乘的意义:](/img/160880489472851312.png)

#### 四、线性变换
共通性：线性变换：
![线性变换:](/img/160880489472851318.png)

缩放 （' 读为prime）
![缩放矩阵:](/img/160880489472851313.png)

翻转
![翻转矩阵:](/img/160880489472851314.png)

扭曲
![扭曲矩阵:](/img/160880489472851315.png)

旋转
![推导过程:](/img/160880489472851316.png)
![旋转矩阵:](/img/160880489472851317.png)


#### 五、Homogeneous Coordinate 齐次坐标

* 问题：平移的变换并不是线性变换（即不可以写为 x'= Mx）
![平移表示:](/img/160880489472851319.png)

齐次坐标中引入了w坐标值
为了使用线性变换的方程来表示带平移的变换，这时齐次坐标就发挥了作用：
* 对于 向量，齐次坐标w值为0 (x, y, 0)， (x, y, z, 0)
* 对于 点， 齐次坐标w值为1 (x, y, 1), (x, y, z, 1)

对于两个点相加的齐次坐标的意义，其实是求两个点的中点
![各种变换的意义:](/img/160880489472851320.png)

仿射变换：
![仿射变换：](/img/160880489472851321.png)
齐次坐标：
![齐次坐标：](/img/160880489472851322.png)

齐次坐标下的二维点变换：
![齐次坐标下的二维点变换：](/img/160880489472851323.png)

特征：
当x' = Mx 成立时， x = M-1x'也成立。 即如果需要还原，则使用变换矩阵的逆矩阵变换即可

#### 六、组合变换
无论二维还是三维，都是先线性变换，再平移

矩阵的组合相乘是从右往左算
![组合变换是从右往左算：](/img/160880489472851324.png)

* 启示：由于矩阵有结合律，可以对于复杂的变换，把变换的矩阵先乘在一起，如常用的MVP矩阵

#### 七、三维变换
平移变换和线性变换一起称为仿射变换
旋转的逆矩阵与旋转的转置矩阵是相同
数学上如果逆矩阵与转置矩阵相同，则为正交矩阵

y轴旋转矩阵不同的原因是, z cross x = +y，与x cross z的结果方向相反了

![三维变换：](/img/160880489472851325.png) 

* 任意的旋转都能分解为三种旋转： 

![三种旋转分解：](/img/160880489472851326.png) 

![罗得里格欺旋转公式：](/img/160880489472851327.png) 

#### 八、View变换/相机变换（Model-View Transformation）
将物体变到以相机为坐标系，即相机归成原点为轴

设定相机位置为e，看的方向为g，相机向上为t， 需要变以uvw构成的坐标系，设定w为-g的方向，u为t和w的叉积方向。
![变换：](/img/160880489472851328.png) 
$$
w=-\frac{g}{||g||},\
u=\frac{t\times w}{||t\times w||},\
u=\frac{g\times t}{||g\times t||},\
v=w\times u
$$

反向：假设已经得到uvw，变为XYZ如下：
$$
\left[
\begin{matrix}
u&v&w&e\\
0&0&0&1
\end{matrix}
\right]
$$

由于旋转的逆矩阵与转置矩阵相同，即互为正交矩阵，因此，只需要得到此矩阵的逆即可

先进行平移变换， 再进行变换，：
$$
M_cam = \left[
\begin{matrix}
u&v&w&e\\
0&0&0&1
\end{matrix}
\right]^{-1}
=
\left[
\begin{matrix}
x_u&y_u&z_u&0\\
x_v&y_v&z_v&0\\
x_w&y_w&z_w&0\\
0&0&0&1
\end{matrix}
\right]

\left[
\begin{matrix}
1&0&0&-x_e \\
0&1&0&-y_e \\
0&0&1&-z_e \\
0&0&0&1
\end{matrix} 
\right]
$$


#### 九、Projection变换

* $x=l \equiv$ left plane,
* $x=r \equiv$ right plane,
* $y=b \equiv$ bottom plane,
* $y=t \equiv$ top plane,
* $z=n \equiv$ near plane,
* $z=f \equiv$ far plane.

正交变换
* 1.将所有模型所在的空间的中心点平移至原点。依据模型变换中的平移矩阵，其实就是平移空间中心坐标的负值
* 2.将空间的坐标轴数值缩放至 [-1, 1]³ 的标准立方体中。依据模型变换中的缩放矩阵

$$

M_{\text {ortho }}=\left[\begin{array}{cccc}
\frac{2}{r-l} & 0 & 0 & 0 \\
0 & \frac{2}{t-b} & 0 & 0 \\
0 & 0 & \frac{2}{n-f} & 0 \\
0 & 0 & 0 & 1
\end{array}\right]\left[\begin{array}{cccc}
1 & 0 & 0 & -\frac{r+l}{2} \\
0 & 1 & 0 & -\frac{t+b}{2} \\
0 & 0 & 1 & -\frac{n+f}{2} \\
0 & 0 & 0 & 1
\end{array}\right]
=\left[\begin{array}{cccr}
\frac{2}{r-l} & 0 & 0 & -\frac{r+l}{r-l} \\
0 & \frac{2}{t-b} & 0 & -\frac{t+b}{t-b} \\
0 & 0 & \frac{2}{n-f} & -\frac{n+f}{n-f} \\
0 & 0 & 0 & 1
\end{array}\right]
$$

透视变换:
变换过程：透视投影的空间是一个四棱台，因为正交投影的矩阵已知，所以可以先将四棱台“挤压”为一个长方体，然后再对其进行正交投影。在“挤压”过程中，首先，近平面上的点坐标不变，因为最终就是投影到近平面； 其次，远平面上的点Z轴坐标不变，注意近平面和远平面之间的点Z轴坐标还是会变的，这也是产生“近大远小”的原因；最后，通过前两个性质，就限定了四棱台“挤压”为长方体只会有一种方式，即最终的变换矩阵是唯一的

![四棱台内的关系：](/img/160880489472851329.png) 

$$
\begin{aligned}
&M_{\text {persp-ortho }}^{4 \times 4} \times\left[\begin{array}{l}
x \\
y \\
z \\
1
\end{array}\right]=\left[\begin{array}{c}
\frac{n}{z} x \\
\frac{n}{z} y \\
\text { unknow }
\end{array}\right]=\left[\begin{array}{c}
n x \\
\text { ny } \\
\text { unknow } \\
z
\end{array}\right] \\
&\Rightarrow M_{\text {persp-ortho }}^{4 \times 4}=\left[\begin{array}{cccc}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
? & ? & ? & ? \\
0 & 0 & 1 & 0
\end{array}\right]
\end{aligned}
$$

* 近平面的点的推导
对于近平面的点（x, y, n, 1） 经过透视变换，必定得到点(nx, ny, $n^2$, n)

$$
\begin{aligned}
&M_{\text {persp-ortho }}^{4 \times 4} \times\left[\begin{array}{l}
x \\
y \\
n \\
1
\end{array}\right]=\left[\begin{array}{c}
n x \\
n y \\
n^{2} \\
n
\end{array}\right]\\
&\Rightarrow M_{\text {persp-ortho }}^{4 \times 4}=\left[\begin{array}{cccc}
\boldsymbol{n} & \mathbf{0} & \mathbf{0} & 0 \\
\mathbf{0} & \boldsymbol{n} & \mathbf{0} & \mathbf{0} \\
\mathbf{0} & \mathbf{0} & \boldsymbol{A} & B \\
0 & 0 & 1 & 0
\end{array}\right]\\
&\therefore \exists A n+B=n^{2}
\end{aligned}
$$

* 对于远平面的中心点的推导
对于远平面的中心点(x, y, f, 1) 经过透视变换，必定得到点（nx, ny, $f^2$, f)

$$
M_{\text {persp-ortho }}^{4 \times 4} \times\left[\begin{array}{l}
x \\
y \\
f \\
1
\end{array}\right]=\left[\begin{array}{c}
n x \\
n y \\
f^{2} \\
f
\end{array}\right]\\
\therefore \exists A f+B=f^{2}
$$

由上两种情况，得到如下“挤压”的变换方程：
$$
\begin{aligned}
&\therefore\left\{\begin{array} { l } 
{ A n + B = n ^ { 2 } } \\
{ A f + B = f ^ { 2 } }
\end{array} \Rightarrow \left\{\begin{array}{l}
A=n+f \\
B=-n f
\end{array}\right.\right. \\
&M_{\text {persp-ortho }}^{4 \times 4}=\left[\begin{array}{cccc}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -n f \\
0 & 0 & 1 & 0
\end{array}\right]
\end{aligned}
$$

因此，透视变换矩阵应为：先进行挤压，再进行一次正交变换
$$
\begin{aligned}
&M_{\text {persp }} \\
&=M_{\text {ortho }} M_{\text {persp-ortho }} \\
&=\left[\begin{array}{cccc}
\frac{2}{r-l} & 0 & 0 & 0 \\
0 & \frac{2}{t-b} & 0 & 0 \\
0 & 0 & \frac{2}{n-f} & 0 \\
0 & 0 & 0 & 1
\end{array}\right]\left[\begin{array}{cccc}
1 & 0 & 0 & -\frac{r+l}{2} \\
0 & 1 & 0 & -\frac{t+b}{2} \\
0 & 0 & 1 & -\frac{n+f}{2} \\
0 & 0 & 0 & 1
\end{array}\right]\left[\begin{array}{cccc}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -n f \\
0 & 0 & 1 & 0
\end{array}\right]
\end{aligned}
$$
