---
title: WPF
cover: false
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- WPF
tags: 
- WPF
- Note
---
# Windows Presentation Foundation 

> 扩展： .net framework与.net core与.net与.net standard与mono的区别
> .net framework是最早出现在2002微软发布的商业框架，仅支持windows平台，目前到4.8版本后暂无更新的后续，但只要windows系统存在，就会一直可用。
> mono则是针对.net framework做的跨平台版本。
> .net core是跨平台的开源框架，发现在于2016年，吸取了mono的经验。
> .net standard则是一个标准接口库，对于跨平台的接口，不同的系统有不同的实现
> 而.net5,.net6将是集合这两种的全新时代

## XAML
* eXtensible Application Markup Language
* Microsoft's version of XML for coding a graphical user interface
* An essential part of WPF
* Each GUI element, will consist of a XAML file and CodeBehind(.cs) file
* Together they create the window

* 管理其下的UI元素
* 其背后的CS 文件，处理所有的事件和有权限去管理GUI的元素
* 每一行的XAML代码都可以被写成CS代码

```
<Label Content="Hello"/> 
<Label>Hello</Label>
```
* 属性详情可参考MSDN： 
https://docs.microsoft.com/zh-cn/dotnet/desktop/wpf/xaml/?view=netdesktop-6.0
https://docs.microsoft.com/en-us/dotnet/desktop/wpf/advanced/xaml-syntax-in-detail?view=netframeworkdesktop-4.8

## Window
应用程序的开始，每个WPF程序自带一个Window.
包含:
* title bar
* maximize button
* minimize button
* close button
常用属性：
WindowState: Normal, Maximized, Minimized. 初始的窗口显示状态
WindowStartupLocation: Manual(由top,left属性决定位置)， CenterOwner(所有自己的window的中间)， CenterScreen（屏幕中间）
Topmost: 置顶（默认为False）
SizeToContent: Manual(默认)， Height, Width, WidthAndHeight。 决定窗口大小的自动适配
ShowInTaskbar:是否显示在系统任务栏，默认为True
ResizeMode: CanResize（默认值） CanMinimize/ CanMaxmize. NoResize。 重定义窗口大小的方法
Icon: 图标

内置属性：
x:Class: 表示其子结点是哪一个CS文件
xmlns: xml namespace. 表示以哪种命名空间去对应XML的结点
xmlns:x: 非默认标签，表示xaml结点。 被xaml的命名空间使用。 如x:Name将为组件声明一个xaml.cs文件中可用的组件名
xmlns:d: 用于在VS中不用编译和运行实时看到组件。意味着带着这个前缀的属性不会影响任何runtime的设置，只会影响设计中
xmlns:mc: markup compatibility 对不同版本的xml的适配。
mc:Ignorable；通常为：'d'表示忽略d的前缀在运行时
xmlns:local: 本地项目想使用的自定义标签

## App Config
App.xaml文件
* 可以设置启动的window: StartupUri = "xxxxwindow.xaml"
* 全局Application级都要使用到的资源文件

## TextBlock
文本块标签。可支持富文本
可添加子标签：
* LineBreak标签换行。
* span 定制某段文字
属性： 
* TextTrimming: "WordEllipsis" 自动使用省略号为看不到的字符。默认值为None
* TextWrapping: "Wrap"会切单词 "WrapWithOverflow"不会切割一个单词
* Foreground: 颜色
```
this.Content = myTextBlock; // 设置为当前内容面板
myTextBlock.Inlines.Add("this is added");//添加新内容
myTextBlock.Inlines.Add(new Run("Run text with this code"){
    Forground = Brushes.Red,
    TextDecorations = TextDecoration.Underline
});
```

## Hyperlink
在xaml中添加
```
<Hyperlink RequestNavigate="MethodName" NavigateUrl="https://www.google.com">Google</Hyperlink>
```
将生成如下CS函数：
```
private void MethodName(object sender, RequestNavigationEventArgs arg)
{
    System.Diagnostics.Process.Start(e.Uri.AbsoluteUri);
}
```
> loremipsum.io 生成文本

## Label & TextBox & PasswordBox
* Label: 向其中可以添加StackPanel并定为水平，再放上Image和AccessText。也可以设置上Margin。 
属性： 
BorderThickness:边缘厚度
BorderBrush: 边缘颜色

* TextBox: 输入框 
属性：
FontSize: 大小
Margin: 外间距
AcceptsReturn: True/False 是否支持回车换行
TextWrapping: Wrap
SpellCheck.IsEnabled: 是否支持拼写
Language: en-US 英文
Background: 背景
Foreground: 文字颜色

* PasswordBox: 密码输入框 
属性：
 PasswordChar: 指定输入字符
 MaxLength:最大输入长度

## Button & RadioButton & Checkbox
* Button:
属性：
Click, MouseDoubleClick: 单击和双击事件
MouseEnter/MouseLeave: 鼠标进入进出事件
ToolTip: 鼠标放置上显示的提示文字

* RadioButton:
单选按钮，可为其中放置WrapPanel放置更多内容
属性：
GroupName:组名，不设置则全局的RadioButton只能选一个
x:Name: 设置名字，可以在cs中获取此名字拿到ischecked的属性
Checked: 当选中时使用的事件
UnChecked: 不选中时使用的事件

* CheckBox
多选选项框
其他属性与RadioButton类似

## Image
默认保证其Ratio比例
属性：
width:宽
Source: 可以是本地路径或网址
>如果是项目根目录创建一个Images文件夹，则这里的本地路径格式为：（可省pack://application:...）/Images/xx.PNG
MouseUp：点击图片的事件

```
//此处ImageControlDemo为项目名，component为固定
myImage.Source = new BitmapImage(new Uri(@"/ImageControlDemo;component/Images/xx.png", UriKind.Relative));
```

## Slider
0d 与 0 
属性：
TickPlacement:结点的位置
TickFrequency: 结点分布
IsSnapToTickEnable: 自动贴合到结点
Value: 数值（0-100）
ValueChanged: 值变化事件，注意，这个事件会在进入时调用一次
Maxiumn:最大值
Minimum:最小值

使用数据绑定：
```
# 获取滑动条的数值变动文本的文字大小
<Slider x:Name="mySlider"></Slider>
<TextBlock FontSize="{Binding ElementName=mySlider, Path=Value, UpdateSourceTrigger=PropertyChanged}"></TextBlock>
```

## Calendar

属性：
SelectedDate: 选中的日期
DisplayMode: Year, Decade， Month 各种显示视图

去除日期：
```
<ViewBox Stretch="Uniform">
<Calendar>
<Calendar.BlackoutDates>
    <CalendarDateRange Start="03.05.2021" End="03.09.2021"/>
</Calendar.BlackoutDates>
</Calendar>
</ViewBox>
```

## DatePicker
日期选择器
属性：
SelectedDate ="03/01/2021"
SelectedDateFormat="Long"
去除日期：
DatePicker.BlackoutDates

变更事件：
SelectedDateChanged

## Expander
缩放扩大器
属性：
Header: 图标的标题
标签：
定制标题
```
<Expander.Header></Expander.Header>
```
```
<Expander></Expander>
```

事件：
Expanded: 是否展开的事件回调

## 布局器-Grid
```
<Grid>
//定义列， 使用权重： Width=0.6* 或使用像素width=200， 或使用width=Auto根据子物品自动适配
<Grid.ColumnDefinitions>
</Grid.ColumnDefinitions>
</Grid>
```

Grid.RowSpan Grid.ColumnSpan每一格所占的子格数

## 布局器-StackPanel
属性：
Orientation: 方向 

## 滚动器-ScrollViewer
与StackPanel布局器使用类似，直接套在外层

## 布局器-WrapPanel
使相同行具有最大的高度或宽度，类似于相互对齐的功能
属性：
Orientation: 以何方向对齐

## 布局器-DockPanel
以地毯式的布局

属性：
LastChildFill: 默认True 最后一个元素来填充空白，False则最后一个元素按Dock位置而定
```
****************
*****  Top *****
****************
***          ***
*L*          *R*
*e*  CENTER  *i*
*f*          *g*
*t*          *h*
***          ***
****************
***  Bottom ***
****************
<DockPanel>
<Button DockPanel.Dock="Top"></Button>
<Button DockPanel.Dock="Left"></Button>
<Button DockPanel.Dock="Right"></Button>
<Button DockPanel.Dock="Bottom"></Button>
<Button DockPanel.Dock="Left"></Button>
</DockPanel>
```

## 画板-Canvas
自由摆放位置的画板
属性：
Opacity:透明度
```
<Canvas>
<Button Canvas.Left="5"></Button>
</Canvas>
```

## StatusBar-状态栏控件
条型布局
```
<StatusBar>
<StatusBarItem></StatusBarItem>
<Separator></Separator>
</StatusBar>
```

## 关于Binding

MVVM中充当VM的作用，把Model与View绑定起来。 类似于监听器模式，对于Model中的数据变化当实时反应到Model

```
this.textBox1.SetBinding(TextBox.TextProperty, new Binding("Value"){ElementName="slider1"})
==>
<TextBox x:Name="textBox1" Text="{Binding Path=Value, ElementName=slider1}">
<TextBox x:Name="textBox1" Text="{Binding Value, ElementName=slider1}">
```
xaml中的属性：
Path: 
关注的属性名或使用点取子对象的属性，也可使用/（斜线）表示当前的Source。
xaml中可以不写Path，此情况，表示使用当前的Source为值显示。 与写.的意义一样，但在CS中不可以不写Path

UpdateSourceTrigger: 枚举，Default, PropertyChanged, LostFocus, Explicit 变化通知的方式（即时性）
BindingMode: 控制数据流向， 只读采用OneWay
RelativeSource: 当需要找的数据源不是直接Source指定，比如是父级组件上的，这时需要用到Relative

    Mode: Self 自身， PreviouseData 静态实例, TemplatedParent 静态实例, FindAncestor：使用往上找
    AncestorType: 类型
    AncestorLevel:从哪一层开始，从当前0 往上不断加1
    Path: 指定属性名
```
<Grid xName="g1">
<Grid xName="a1">
<Grid xName="b1">
<TextBox x:Name="textBox1">
</Grid>
</Grid>
</Grid>

//如果希望textBox1中显示g1的Grid名字，则需要用RelativeSource
<TextBox x:Name="textBox1" text="{Binding FindAncestor AncestorType={x:Type Grid}, AncestorLevel=1, Path=Name}">
```

Converter: 
数据类型转换器，可指定内置的，如：
```
Converter={StaticResource BooleanToVisibilityConverter}
```

DataContext：
对于一整个xaml都需要使用的VM,可以指定一个DataContext作为VM
