---
title: LUA与CSHARP交互
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Unity
---

## 相互调用
原理：  C#与Lua进行交互主要通过虚拟栈实现

## C# Call Lua:
* 内存： 由C#先将数据放入栈中，由lua去栈中获取数据，然后返回数据对应的值到栈顶，再由栈顶返回至C#。
* 代码： C#生成Bridge文件，Bridge调dll文件（dll是用C写的库），先调用lua中dll文件，由dll文件执行lua代码
C#->Bridge->dll->Lua  OR   C#->dll->Lua

## Lua Call C#:
* 内存： 先生成C#源文件所对应的Wrap文件或者编写C#源文件所对应的c模块，然后将源文件内容通过Wrap文件或者C模块注册到Lua解释器中，然后由Lua去调用这个模块的函数。
* 代码：先生成Wrap文件（中间文件/适配文件），wrap文件把字段方法，注册到lua虚拟机中（解释器luajit），然后lua通过wrap就可以调C#了
或者在config文件中添加相应类型也可以

## unity下的lua框架

为了使基于unity开发的应用在移动平台能够热更新，我们嵌入了Lua虚拟机，将需要热更新的逻辑用lua实现。c#通过P/Invoke和lua交互（lua由ANSI C实现）。在这个过程中，由于数据的交换需要使用==lua提供的虚拟栈 #F44336==，不够简单高效，为了解决这个问题，我们引入了\*lua框架（xlua、slua、ulua）来达到类似RPC式的函数调用、类原生对象式的对象访问以及高效的对象传递。

### XLUA
可以把xlua的push API归为两类：一类是针对某种特定类型的push，暂且叫做LowLevelAPI；还有一类是基于LowLevelAPI封装的更上层的HighLevelAPI。

* 门面模式
使用HighLevelAPI时你只要简单的传入你想push的对象，HighLevelAPI会帮你找到最适合的LowLevelAPI调用，因为就算同一种类型的push方法，也可能有用户自定义的优化版本。而对于LowLevelAPI最终是需要调用xlua.dll中提供的C API来协调完成最终的工作。

#### LowLevelAPI

``` csharp
//using RealStatePtr = System.IntPtr;
//using LuaCSFunction = XLua.LuaDLL.lua_CSFunction;
//typedef int (*lua_CFunction) (lua_State *L);

//ObjectTranslator.cs
void pushPrimitive(RealStatePtr L, object o)
public void Push(RealStatePtr L, object o)
public void PushObject(RealStatePtr L, object o, int type_id)
public void Push(RealStatePtr L, LuaCSFunction o)
internal void PushFixCSFunction(RealStatePtr L, LuaCSFunction func)
public void Push(RealStatePtr L, LuaBase o)
public void PushDecimal(RealStatePtr L, decimal val)
```

* 传递基元类型
 
 
基元类型为 Boolean、Byte、SByte、Int16、UInt16、Int32、UInt32、Int64、UInt64、UIntPtr、Char、Double、Single和IntPtr （对应的void*）。
``` csharp
void pushPrimitive(RealStatePtr L, object o)
```

XLUA中：

``` csharp
//push一个int
LUA_API void xlua_pushinteger (lua_State *L, int n)
//push一个double
#define LUA_NUMBER	double
typedef LUA_NUMBER lua_Number;
LUA_API void lua_pushnumber (lua_State *L, lua_Number n)
//push一个IntPtr
LUA_API void lua_pushlightuserdata (lua_State *L, void *p)
```

对于long，xlua定制：

``` cpp
//i64lib.c
//在lua中表示c#中的long
typedef struct {
	int fake_id;
	int8_t type;
    union {
		int64_t i64;
		uint64_t u64;
	} data;
} Integer64;
```

* 传递 object

``` csharp
public void Push(RealStatePtr L, object o)
public void PushObject(RealStatePtr L, object o, int type_id)
```


不管object是什么类型，最终的push都是使用:
``` c
LUA_API void xlua_pushcsobj(lua_State *L, int key, int meta_ref, int need_cache, int cache_ref) {
	int* pointer = (int*)lua_newuserdata(L, sizeof(int));
	*pointer = key;
	
	if (need_cache) cacheud(L, key, cache_ref);

    lua_rawgeti(L, LUA_REGISTRYINDEX, meta_ref);

	lua_setmetatable(L, -2);
}
```

为什么我们传给lua的对象是一个int类型（这里的key）？其实我们这里的key是我们要传递的c#对象的一个索引，我们可以通过这个索引找到这个c#对象。

当传递一个c#对象的时候，我们创建一个userdate，并把这个索引值赋给这个userdata。然后，lua在全局注册表中，有一张专门的表用来存放c#各种类型所对应的元表，而**meta_ref**就是当前这个对象所对应类型的元表的索引id，我们通过他找到对应的元表，就可以通过setmetatable来绑定操作这个对象的方法。最终lua就可以愉快的使用这个对象。

>每种类型所对应的元表，是我们在push一种类型的对象之前，提前注册进来的，后面详述。


但是对于引用类型的对象，其生命周期是有可能超出当前的调用栈的（比如lua用一个变量引用了这个对象） 。这时，我们就不仅要能够通过这个key找到c#原始对象，还要通过这个key能够找到对应的lua代理对象。因此，对于引用类型，我们在lua中同样也要建立一套索引机制，这就是need_cache和cache_ref的作用：
``` c
static void cacheud(lua_State *L, int key, int cache_ref) {
	lua_rawgeti(L, LUA_REGISTRYINDEX, cache_ref);
	lua_pushvalue(L, -2);
	lua_rawseti(L, -2, key);
	lua_pop(L, 1);
}
```

* 缓存

再回过头来看看c#中的索引和缓存机制：

在调用xlua_pushcsobj之前,所有object都会被放入一个对象的缓存池中ObjectTranslator.objects。而我们得到的key就是这个对象在缓存池中的下标。


* gc

对于引用类型，它的生命周期管理会略微复杂。**mono和lua虚拟机有各自的gc系统**，并且相互无法感知。当lua和c#同时引用一个对象时，我们需要能够保证对象生命周期的正确，不能一边还在引用，另一边却把它释放掉了。

这个过程是由lua的gc驱动的。我们**把对象push到lua时，会缓存在c#的对象池中，所以是不会被mono的gc所释放掉，这样就保证了lua能够安全的持有c#对象。同时我们也会把这个对象的代理缓存到lua中，而lua中对象的缓存表是一个弱表，也就是说，当没有其他的lua引用这个对象时，lua的gc会把这个对象从lua的缓存中回收**，而对象被gc回收的过程会触发这个对象的的__gc元方法。

而这个__gc元方法就会通知到c#这端，来告诉我们lua不再使用这个对象，我们可以把它从对象缓存池中移除。当没有其他c#对其的引用时，mono的gc就会正常的回收这个对象。

``` csharp
//StaticLuaCallback.cs
//__gc元方法：
public static int LuaGC(RealStatePtr L)
{
    try
    {
        int udata = LuaAPI.xlua_tocsobj_safe(L, 1);
        if (udata != -1)
        {
            ObjectTranslator translator = ObjectTranslatorPool.Instance.Find(L);
            if ( translator != null )
            {
                translator.collectObject(udata);
            }
        }
        return 0;
    }
    catch (Exception e)
    {
        return LuaAPI.luaL_error(L, "c# exception in LuaGC:" + e);
    }
}

//从缓存池中删除
internal void collectObject(int obj_index_to_collect)
{
	object o;
	
	if (objects.TryGetValue(obj_index_to_collect, out o))
	{
		objects.Remove(obj_index_to_collect);
        
        if (o != null)
        {
            int obj_index;
            //lua gc是先把weak table移除后再调用__gc，这期间同一个对象可能再次push到lua，关联到新的index
            bool is_enum = o.GetType().IsEnum();
            if ((is_enum ? enumMap.TryGetValue(o, out obj_index) : reverseMap.TryGetValue(o, out obj_index))
                && obj_index == obj_index_to_collect)
            {
                if (is_enum)
                {
                    enumMap.Remove(o);
                }
                else
                {
                    reverseMap.Remove(o);
                }
            }
        }
	}
}
```

* 元表

对于业务来说，我们只是单纯的把对象的索引传递过去，是远远不够的，我们还需要提供直接使用和操作对象的方法。前面我们提到，在我们把一个对象push到lua之前，我们会把对象类型所对应的元表提前注册到lua之中。这样在我们真正push一个对象时，就会用这个元表来设置操作这个对象的方法。

首先第一个问题就是，如何表示c#对象的类型？回过头来看看我们的Push函数，其中最重要的就是getTypeId：

首先会尝试从c#的类型缓存typeIdMap中检查是否已经注册过这种类型，如果没有的话，我们就需要为其生成一个type_id。

**再从lua的类型缓存中用类型名来检索是否已经注册过这种类型，如果没有的话，意味着我们还没有为这种类型在lua中注册一个元表，继而通过TryDelayWrapLoader来生成这个类型的元表**。

``` csharp
//
public void Push(RealStatePtr L, object o)
{
	//...
	Type type = o.GetType();
	bool is_first;
	int type_id = getTypeId(L, type, out is_first);
	//...
}

//这里再次吐槽getTypeId函数的设计和实现，为了保持清楚，我只保留能大体说明逻辑的的代码
internal int getTypeId(RealStatePtr L, Type type, out bool is_first, LOGLEVEL log_level = LOGLEVEL.WARN)
{
	//尝试获取c#中检索
	if (typeIdMap.TryGetValue(type, out type_id)){return;}
	//尝试从lua中检索
	LuaAPI.luaL_getmetatable(L,type.FullName);
	if (LuaAPI.lua_isnil(L, -1)) 
	{
	    LuaAPI.lua_pop(L, 1);
	    //获取类型的元表
	    if (TryDelayWrapLoader(L,  type))
	    {
	        LuaAPI.luaL_getmetatable(L, type.FullName);
	    }
	    else
	    {
	        throw new Exception("Fatal: can not load metatable of type:" + type);
	    }
	}
	//生成新的type_id
	type_id = LuaAPI.luaL_ref(L, LuaIndexes.LUA_REGISTRYINDEX);
	//注册到lua
    LuaAPI.lua_pushnumber(L, type_id);
    LuaAPI.xlua_rawseti(L, -2, 1);
    LuaAPI.lua_pop(L, 1);
    
    if (type.IsValueType())
    {
    	typeMap.Add(type_id, type);
    }

    typeIdMap.Add(type, type_id);
}
```

* 传递c#函数
 

xlua通过lua_pushstdcallcfunction来push一个LuaCSFunction，其调用的时xlua.dll提供的xlua_push_csharp_function。
``` csharp
 //LUADLL.cs
public static void lua_pushstdcallcfunction(IntPtr L, lua_CSFunction function, int n = 0)//[-0, +1, m]
{
	IntPtr fn = Marshal.GetFunctionPointerForDelegate(function);
	xlua_push_csharp_function(L, fn, n);
}
```

最终提供给用户的是这两个接口：

``` csharp
internal void PushFixCSFunction(RealStatePtr L, LuaCSFunction func)
public void Push(RealStatePtr L, LuaCSFunction o)
```

这两个函数都做了一件事情，就是在LuaCSFunction函数push到lua之前，用另一个LuaCSFunction来包装了一层，用来做异常捕获。

> 和gc一样，mono和lua有自己的异常

两种索引方式的不同，使用在了不同的场景。

PushFixCSFunction()大量被用在我们静态生成的元表构造器中，做为默认需要支持的类型的元表，注册进lua，并永久存在。而Push()被大量使用在反射生成的元表之中，在使用完之后，可能就会被释放。

最后还有一个小细节，Push()中对IsStaticPInvokeCSFunction的函数没有加包装，因为这种类型的函数是我们静态生成的，在生成时，我们已经加入了异常捕获的代码，不需要再被捕获了。

>可以看到，一个函数在被调用之前，进行了多次的包装，每次包装都附带了一些额外的功能，但又对原函数没有侵入。（函数式编程，面向切片编程）

* 其他push

``` csharp
//push一个lua在c#中的代理对象
public void Push(RealStatePtr L, LuaBase o)
```

LuaBase是c#对lua中特有的类型的封装。比如说LuaTable对应table、LuaFunction对应luafunction（此处不是luacfunction）。C#可以通过对应的类型去创建、操作一个lua原生对象。

所以，LuaBase只是一个lua对象在c#中的代理，我们push一个LuaBase其实是找到真正的lua对象，并push。

``` csharp
//重载push一个decimal，避免gc
void PushDecimal(RealStatePtr L, decimal val)
```


#### HighLevelAPI

对于HighLevelAPI，里面不包含具体的push实现，而是通过获取对象的类型，来选择性的调用类型所对应的具体push函数。

可以看作类似是编译器的函数重载功能

``` csharp
public void PushAny(RealStatePtr L, object o)
public void PushByType<T>(RealStatePtr L,  T v)
```

* 顾名思义，PushAny()可以用来push所有的类型，可以被用在我们提前没法知道对象类型的地方。最典型的例子就是在反射生成元表时，我们动态的获取对象，通过PushAny()把类型未知的对象push到lua。

* PushByType()是对PushAny()的封装，唯一的不同就是做了一个优化：
对于基元类型，不再调用pushPrimitive() （会有装箱/拆箱）,而是通过查表的方式直接获取针对各个基元类型的直接push的方式。