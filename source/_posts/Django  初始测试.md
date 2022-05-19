---
title: Django  初始测试
categories:
- Python
tags: 
- Python
- Note
- Django
---

### 使用models.py 创建数据库

> 注意事项：
>1、makemigrations 和 migrate 工作原理分别是什么：
makemigrations：根据检测到的模型创建新的迁移。迁移的作用，更多的是将数据库的操作，以文件的形式记录下来，方便以后检查、调用、重做等等。
migrate：使数据库状态与当前模型集和迁移集同步。说白了，就是将对数据库的更改，主要是数据表设计的更改，在数据库中真实执行。例如，新建、修改、删除数据表，新增、修改、删除某数据表内的字段等等。
2、如果不想使用 Django 的 makemigrations 和 migrate 功能，但是不小心执行了这两个命令会发生什么，
首先在该app下建立 migrations目录，并记录下你所有的关于modes.py的改动，比如0001_initial.py，
接着执行migrate的话，这时候会作用到数据库文件，产生对应的表
3、官方解释：
运行 python manage.py makemigrations 为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。
参考： https://blog.csdn.net/weixin_43507484/article/details/87950788

> 1. 先执行一下迁移


> 2. 编辑app里的models.py
如：

```
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

> 3. 激活模型

```
#mysite/settings.py
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

> 4. 执行生成数据库


```
python manage.py makemigrations polls
```

输出迁移过程中可能执行的sql

```
python manage.py sqlmigrate polls 0001
```

最后，正式执行迁移

```
python manage.py migrate
```



### 使用API

进入项目的Python控制台

```
python manage.py shell

from polls.models import Choice, Question  # Import the model classes we just wrote.
Question.objects.all()
```

给模型添加__str__()函数，这样默认输出将会改变

```
from django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```



### 使用管理员账号

```
python manage.py createsuperuser
```

此时进入xxxx/admin网址，登录就可看到数据库资源

```
python manage.py runserver
```

加入我们的项目

```
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

无需重启，直接刷新就可以看到项目在主界面


