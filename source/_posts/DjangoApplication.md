---
title: Django 实例 Web Application
categories:
- Python
tags: 
- Python
- Note
- Django
- 实例
---

## Preparing

 > Python
 > Django
 > Html
 > css
 > Javascript
 > Databases
 > HeroKu
 > Materialize  
 > Beautiful suite
 > Web scraping


## Starters!

+ 创建conda环境

```
conda create --name codedaddies python=3
```

+ 安装django

```
pip install django
```

+ 创建工程（指定目录下）

```
django-admin startproject codedaddies_list
```

+ 创建APP

```
python manage.py startapp my_app
```

+ 数据库构建

```
python manage.py makemigrations
python manage.py migrate
```

+ Templates文件夹
> 配置在settings中，加入以下：
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
> 底部加入:
STATICFILES_DIR = (os.path.join(BASE_DIR, 'static'),)

> TEMPLATES块中设置DIRS
> 'DIRS': [TEMPLATE_DIR],

注：需要在pycharm中设置templates标志

+ 启用admin
```
python manage.py createsuperuser
```


## First Page

+ APP中新建urls.py
在文件中配置路径表：

```
from . import views


urlpatterns = [
    path('', views.home, name='home'),
]
```

+ 创建视图（与上面的Home匹配）
在views.py

```
def home(request):
    return render(request, 'base.html')
```

+ 创建数据表

models.py中

```
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

```
记得执行migrate操作

+ 添加admin管理

```
from .models import Search

# Register your models here.
admin.site.register(Search)
```

