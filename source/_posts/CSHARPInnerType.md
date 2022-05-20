---
title: CSHARP的内置引用类型
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1608707782744.png
categories:
- Unity
---

## 对象类型
object 类型是 System.Object 在 .NET 中的别名。 ==在 C# 的统一类型系统中，所有类型（预定义类型、用户定义类型、引用类型和值类型）都是直接或间接从 System.Object 继承的。 可以将任何类型的值赋给 object 类型的变量。 #F44336== 可以使用文本 null 将任何 object 变量赋值给其默认值。 将值类型的变量转换为对象的过程称为 装箱 。 将 object 类型的变量转换为值类型的过程称为取消装箱 。

## 字符串类型

string 类型表示零个或多个 Unicode 字符的序列。 string 是 System.String 在 .NET 中的别名。
string 为引用类型.

> The C# String type is internally a 'UTF-16' byte string.

![核心结构](/img/1608707782744.png)

### Intern pool:常量池，==调用String.Intern()将返回常量池里的相同的字符串引用！ #F44336==

``` csharp
var x = new string(new[] { 'f', 'o', 'o' });
var y = new string(new[] { 'f', 'o', 'o' });
var z = "foo";
var u = "foo";
var v = String.Intern(x);
 
// different reference: x != y != z
Console.WriteLine(Object.ReferenceEquals(x, y)); // false
Console.WriteLine(Object.ReferenceEquals(x, z)); // false
 
// same reference: z == u == v
Console.WriteLine(Object.ReferenceEquals(z, u)); // true
Console.WriteLine(Object.ReferenceEquals(z, v)); // true
 
// same value
Console.WriteLine(x == y && x == z && x == u && x == v); // true
```

### concat与+连接

C # 编译器执行专门的处理，String 的‘ + ’连接转换为 String.Concat。


``` csharp
//“‘ x: ” + x + “ y: ” + y + “ z: ” + z’
string.Concat(new string[]{"x:", x.ToString(), "y:", y.ToString(), "z:", z.ToString() } );//与上面等价
```

> 使用 c # 编译器优化“ + ”级联可能会在当前级联和过去级联之间获得不同的结果。例如，Visual Studio 2019的 c # 编译器的(int x) + (String y) + (int z)结果将是‘ String。Concat (x.ToString () ，y，z.ToString ())’。然而，Visual Studio 2017的 c # 编译器将是‘ String’。Concat ((object) x，y，(object) z)’ ，如果连接非字符串参数，将使用对象重载。因此，会发生结构装箱。如果使用 Unity，你必须注意，结果将根据与 Unity 捆绑的 c # 编译器的版本而有所不同。

### StringBuilder and SpanFormatter

‘ StringBuilder’是一个有‘ char []’作为临时缓冲区的类。Append 用于写入缓冲区，ToString 生成最终的字符串。

``` csharp
// .NET Standard 2.0
public StringBuilder Append(int value)
{
    return Append(value.ToString(CultureInfo.CurrentCulture));
}
 
// .NET Standard 2.1
public StringBuilder Append(int value)
{
    return AppendSpanFormattable(value);
}
 
private StringBuilder AppendSpanFormattable<T>(T value)
    where T : ISpanFormattable
{
    if (value.TryFormat(RemainingCurrentChunk,
        out int charsWritten, format: default, provider: null))
    {
        m_ChunkLength += charsWritten;
        return this;
    }
    return Append(value.ToString());
}
```

### String.Format

由于接收参数为object,因此有拆装箱操作


如图： “ x: ” + x + “ y: ” + y + “ z: ” + z’的简单字符串连接的性能度量。
![各string方式性能对比](/img/1608709965913.png)

## 委托类型

``` csharp
public delegate void MessageDelegate(string message);
public delegate int AnotherDelegate(MyType m, long num);
```

## 动态类型

dynamic 类型表示变量的使用和对其成员的引用绕过编译时类型检查。 

==编译器将有关该操作信息打包在一起，之后这些信息会用于在运行时评估操作。 在此过程中，dynamic 类型的变量会编译为 object 类型的变量。 因此，dynamic 类型只在编译时存在，在运行时则不存在。 #F44336==