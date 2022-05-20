---
title: Django  初步构建
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
categories:
- Python
tags: 
- Python
- Note
- Django
---

### Generic View
>　简化写法，可选的有generic.IndexView和generic.DetailView
>　DetailView 默认使用  \<app name\>/\<model name\>_detail.html.为模板， 可使用template重定向。自动生成model小写名字_list 为名的对象
>　ListView 默认使用  \<app name\>/\<model name\>_list.html 为模板，可使用template重定向。 自动生成model小写名字的context对象

