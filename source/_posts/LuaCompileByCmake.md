---
title: 用Cmake编译测试Lua
cover: false
date: 2022-01-24 21:28:29
updated: 2022-01-24 21:28:29
top_img: false
categories:
- Lua
tags: 
- Lua
---

# 用Cmake编译测试Lua

## 1. 新建clion新的c++运行项目

## 2. 拖入lua的src目录

## 3. CMAKELISTS.TXT改为以下：

```
cmake_minimum_required(VERSION 3.20)
project (LuaProject01)  # project here actually means solution in premake

set(LUA_VERSION 5.4.3)

if(WIN32)
    add_definitions("-DLUA_BUILD_AS_DLL")
    add_definitions( -D_CRT_SECURE_NO_WARNINGS )
endif(WIN32)

aux_source_directory(src LUA_SOURCES)
list(REMOVE_ITEM LUA_SOURCES "src/lua.c" "src/luac.c")

set(LUA_LIBRARY lua${LUA_VERSION})
add_library(${LUA_LIBRARY} SHARED ${LUA_SOURCES})

add_executable(lua src/lua.c)
target_link_libraries(lua ${LUA_LIBRARY})
if(UNIX AND NOT APPLE) #add math library for linux
    target_link_libraries(lua m)
endif()

add_executable(luac ${LUA_SOURCES} src/luac.c)
if(UNIX AND NOT APPLE)
    target_link_libraries(luac m)
endif()

include_directories(src)
add_executable (LuaProject01 main.cpp)
target_link_libraries (LuaProject01 ${LUA_LIBRARY})
if(UNIX AND NOT APPLE) #add math library for linux
    target_link_libraries( LuaProject01 m )
endif()



```



## 4. 添加测试cpp文件

```
#include <iostream>

extern "C"
{
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

int main(int argc, char** argv)
{
    std::cout << "Hello World!\n";
    int status, result;
    lua_State* L = luaL_newstate();  /* create state */
    if (L == NULL) {
        //l_message(argv[0], "cannot create state: not enough memory");
        return EXIT_FAILURE;
    }
    std::string cmd = "a = 7+11";
    int r = luaL_dostring(L, cmd.c_str());

    if (r == LUA_OK)
    {
        lua_getglobal(L, "a");
        if (lua_isnumber(L, -1))
        {
            float a_in_cpp = (float)lua_tonumber(L, -1);
            std::cout << "a_in_cpp = " << a_in_cpp << std::endl;
        }
    }
    else {
        std::string errormsg = lua_tostring(L, -1);
        std::cout << errormsg << std::endl;
    }

    //luaL_dofile(L, "xxx.lua")

    lua_close(L);
}
```

