---
title: 天天生鲜项目实例P1
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1573441070020.png
categories:
- Python
tags: 
- Python
- Note
- Django
- 实例
---

## 相关背景概念

> B2B, O2O, B2C, C2C..

## 数据库设计
![enter description here](/img/1573441070020.png)

> 对数据库进行授权
> ![enter description here](/img/1573442010455.png)

> 使用后台管理
>![enter description here](/img/1573442404015.png)


## 项目搭建

**1.一个模块对应一个APP**
**2.将所有app归类到一个apps文件夹**
**3.\[可选\]  设置一个系统路径，这样就不用注册APP时添加前缀文件夹**
	
``` python
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
```

**4.添加templates包和static包**
>TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
>TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
		...
> STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


**5.添加templates和static路径到setting**

**6.配置数据库为Mysql**

>   'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'USER': 'root',
        'PASSWORD':'bk102435',
        'HOST':'39.97.170.176',
        'PORT':3306,
	
**7.设置语言**

```python
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

**8.配置项目总的urls**
**9.为各应用创建urls**

**10.数据层准备，创建db包，创建basemodel.py**

**11.\[可选\]创建各models 或 链接现有数据库**

> Inpectdb 也可针对某张表：
> python manage.py inspectdb TableName > output.py
> 链接： https://www.jianshu.com/p/037bd7e20a7a

**12.指定django认证系统的模型**
这样superuser的模型表就被指定到自己的user表
> settings.py中加入 
> AUTH_USER_MODEL = ‘user.User’

###  13.  可能出现的问题
不确定是不是使用pymysql导致的，这里会有两个问题
*  1.现在django使用mysqlclient，而且恶心的是会在启动时自动验证版本号，pymysql最高只到0.9.3。这里根据报错直接那代码注释即可！
*  2.makemigration出错，提示在django代码里的operations.py中的last_executed_query函数，由于python3与Python2的decode与encode函数区别，这里也需要把.decode..去掉。




## User模块 - 注册

**1.准备views函数**
* views.py添加相应函数
register函数为接收跳转网页, register_handler函数接收处理及逻辑

```python
def register():
	pass
def register_handle():
	pass
```

* urls.py配置对应view函数路径

```python
path('register',views.register,name='register')
path('register_handle',views.register_handle,name='register_handle')
```


**2.templates里放入html信息**

* 编辑表单\<form\>
	添加method,action.
	写法升级：

```python
action="{% url 'user:detail' %}" 
```

旧的写法:

```python
action = "/user/register_handle"
```

> 注意事项：
> 1. 网页使用跳转，需要在urls.py中指定name:
> 如下：所对应的地址段需要设置不同的正则
> 
> ```python
> path('add/', calc_views.add, name='add'),  # new
> path('add/<int:a>/<int:b>/', calc_views.old_add2_redirect,name='add'),
> ```
> 2.使用shell, 用reverse测试
> 地址反射的机制：django.urls reverse
> 3.定义一个跳转函数来做：
> 
> ```python
> urls.py中加入如下：
>  path('add/<int:a>/<int:b>/', calc_views.old_add2_redirect,name='add'),
> path('new_add/<int:a>/<int:b>/', calc_views.add2, name='add2'),
>
> views.py中加入如下：
> def old_add2_redirect(request):
> return HttpResponseRedirect(
>        reverse('add2', args=(a, b))
>    )
> 测试网址： http://127.0.0.1:8000/add/5/6/ 
> 这时最终就将跳到美术http://127.0.0.1:8000/new_add/5/6/
> ```


	
**3.使用类视图**

> 1.优化去register_handle函数，使用get/post判断实现不同的跳转类型
> 2.基于1的优化，使用类视图方式加载

```python
from django.views.generic import View

class RegisterView(View):

    def get(self, request):
        pass

    def post(self, request):
		pass
```

**3.激活用户**

1. 使用itsdangerous为网址进行加密签名
2. 调用django.core.mail 的send_mail来发送邮件，把链接成文本发送过去

```python
from django.conf import settings
from django.core.mail import send_mail
import time

def send_register_active_email(to_email, username, token):
    '''send active email'''
    subject = "天天生鲜欢迎消息"
    message = ""
    sender = settings.DEFAULT_FROM_EMAIL
    receiver = [to_email]
    html_message = "<h1>%s, 欢迎你</h1>请点击下面链接激活<br/><a href=\"http://127.0.0.1:8000/user/active/%s\">http://127.0.0.1:8000/user/active/%s</a>" % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)
```
>也可使用Python的发email库

>```python
>  def active_email(self, email_addr, active_code):
>      # 第三方 SMTP 服务 # 授权码：cmatkgceuuxcbddc
>      mail_host = "smtp.qq.com"  # 设置服务器
>      mail_user = "1024037035@qq.com"  # 用户名
>      mail_pass = "cmatkgceuuxcbddc"  # 口令
>      sender = '1024037035@qq.com'
>      receivers = [email_addr]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 >       # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
>      try:
>          smtp_obj = smtplib.SMTP()
>          smtp_obj.connect(mail_host, 25)  # 25 为 SMTP 端口号
>          smtp_obj.login(mail_user, mail_pass)
>          smtp_obj.sendmail(sender, receivers, message.as_string())
>          return True
>          "邮件发送成功"
>      except smtplib.SMTPException:
 >           return False
>            "Error: 无法发送邮件"
>```

3. 在Url中配置激活的功能

```python
path('active/<token>',ActiveView.as_view(), name='active'),
```

4. 在views.py中写一个ActiveView的视图来处理激活
 
```python
class ActiveView(View):
    def get(self, request, token):
        try:
            serializer = Serializer(settings.SECRET_KEY, 3600)
            # print(type(token))
            token = token.encode()
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登陆页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已过期')
```


**4.使用celery做为异步处理**

![enter description here](/img/1574171584470.png)

1.配置一个项目目录为：celery_tasks/tasks.py的文件
2.在tasks.py写入配置如 

```python
# use celery
from celery import Celery
# create celery instance
app = Celery('celery_tasks.tasks', broker='redis://:pwd@39.97.170.176:6379/8')

# define task function
@app.task
def send_register_active_email(to_email, username, token):
	pass
```
3.执行的脚本函数里写入：

```python
        # 发送邮件1
        send_register_active_email.delay(email, username, secret_info)
```

4.在有redis的电脑上

* 复制项目代码
* 在tasks.py中加入初始化django的代码
* 
```python
import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()
```
* 启动worker

```
celery -A celery_tasks.tasks worker -l info
```
* 启动redis , 大功告成，测试

> 可能出现的问题
> 在windows系统中：
>  使用这种方式来启动worker: pip install eventlet -> celery -A your_app_name worker --pool=eventlet
>  或： celery -A your_app_name worker --pool=solo -l info
>  或：
>  at worker side:
set FORKED_BY_MULTIPROCESSING = 1
then
celery -A myworker worker --loglevel=info

## User模块 - 登录

**LoginView，使用自带的授权**

授权，如果成功则会返回user对象：：

```
user = authenticate(username=username, password=pwd)
```

登录：

```python
login(request, user)
```

添加URL及表单部分，参考注册流程

**为减少数据库操作，使用redis存储**

1.安装 django-redis
2.settings加入如下配置即可：

```python
#Django 缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/9", #服务器地址
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}, # 最大连接数
            "PASSWORD": "bk102435",
        }
    }
}
#配置session存储
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

**把用户名记在cookie**

1.登录成功时，把username字段存在cookie中

```python
response = redirect(reverse('goods:index'))
remember = request.POST.get('remember')

if remember == 'on':
	response.set_cookie('username', username, max_age=7*24*3600)
else:
	response.delete_cookie('username')
```

2.get方法中取出cookie数据

```
if 'username' in request.COOKIES:
	username = request.COOKIES.get('username')
	checked = 'checked'
else:
	username = ''
	checked = ''
return render(request, 'login.html', {'username':username, 'checked':checked})
```
## User 模块 - 用户中心

**从模板网页中抽象**

1. 将共同部分放在一个html， 不同部分使用{% block body%}{% endblock %}

base_user_center.html:

![enter description here](/img/1574937645193.png)

2.在对应的功能页面继承

![enter description here](/img/1574937788143.png)

**使用if 做功能块显示隐藏**

如上方的：

![enter description here](/img/1574937430699.png)

**使用官方提供的授权管理**

有些页面需要登录后才能显示，如这里的用户中心页
使用django的login_required装饰器来做

https://docs.djangoproject.com/en/2.2/topics/auth/default/

1. 当用户已登录过，将直接跳转至所需页面
2. 当未登录，将默认跳转至/accounts/login/?next=/polls/3/.
3. login_url可在settings.LOGIN_URL中配置 或login_url参数中配置
4. next可在redirect_field_name参数中配置

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def my_view(request):
```

5. 处理用户通过非登录界面过来的
```python
  # 处理通过跳转的请求值#
                # 设置下一步自动跳转 #
                next_url = request.GET.get('next', reverse('goods:index'))
                response = redirect(reverse(next_url))
```

> 注意：需要将form表单的action设成无action，这样提交的内容将按当前内容来指定！


6.使用Mixin优化写法

* 新建utils文件夹，新建一个LoginRequireMixin类

```python
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
```

在所有view函数中继承

```python
class AddressView(LoginRequiredMixin, View):
	pass
```
> Mixin的原理是，执行一个子类没有的函数，Python继承规则是第一个父类先找，找到cls所代表的类的父类，再调用其as_view
> super(A,cls) 找到A的父类，并将cls转成父类对象！

**使用官方提供的是否登录标识**


```python
if request.user.is_authenticated:
    # Do something for authenticated users.
    ...
else:
    # Do something for anonymous users.
    ...
```
因此在html中加入如下代码：

![enter description here](/img/1574937768754.png)


**使用官方提供的退出登录**

logout函数

```html
<a href="{% url 'user:logout' %}">退出</a>
```

```python
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('goods:index'))
```

**实现地址页的功能**

>1.使用request.user拿到user对象
>2.Address.objects.create/get 来操作数据库
>3.post请求中收到后再进行操作
>4.Post请求完毕后，在get请求中再取数据库的地址来到html
>5.显示get请求的结果到html

**抽象Model里的管理器**

model.py里：

需要继承manager
```python
class AddressManager(models.Manager):
    '''自定义模型管理器'''
    def get_default_address(self, user):
        #self.model: 获取self对象所在模型类
        try:
            address = self.get(user=user, is_default=True)
        except self.DoesNotExist as e:
            address = None
        return address
		
class Address(BaseModel):
    """地址模型类"""
    pass
    # 在这里使用定义的管理器
    objects = AddressManager()
```


> 需要使用Address.objects.get_default_address来调用。这样传入self

**用户中心的历史记录显示**

![enter description here](/img/1575029000281.png)

参考redis资料
https://django-redis-chs.readthedocs.io/zh_CN/latest/#
1. 获取StrictRedis对象
	一般做法：
	
	```python
	from redis import StrictRedis
	sr = StrictRedis(host='127.0.0.1', port='6379', db=9)
	```
	
	但可以使用原生端的使用方式：
	
	```python
	from django_redis import get_redis_connection
	con = get_redis_connection("default")
	```
2. 获取redis数据并返回界面

```python
  #获取redis数据连接
        con = get_redis_connection("default")
        #获取数据
        history_key = 'history_%id'%user.id
        #拿前五个
        sku_ids = con.lrange(history_key, 0, 4)
```


```python
 def get(self, request):
        user = request.user
        address = Address.objects.get_default_address(user)

        #获取redis数据连接
        con = get_redis_connection("default")
        #获取数据
        history_key = 'history_%id'%user.id
        #拿前五个
        sku_ids = con.lrange(history_key, 0, 4)
        #获取此ID内的物体
        # goods_li = GoodsSKU.objects.filter(id__in=sku_ids)
        goods_li = []
        for id in sku_ids:
            goods = GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        #数据组装
        context = {'page': 'user',
                   'address': address,
                   'goods_li':goods_li}

        return render(request, 'user_center_info.html', context)
```

3.在Html中配置数据，显示使用for goods, 和empty表示

![enter description here](/img/1575033223646.png)


## 分布式FastDFS文件系统

![enter description here](/img/1575033366217.png)


客户端先发请求到Tracker服务器，服务器将返回一个Storage服务器地址，客户端再上传到此Storage服务器

![enter description here](/img/1575033456146.png)


电商网站的图片数据一般不放在Django服务器，以防服务器存储器爆掉
![enter description here](/img/1575034858096.png)

FastDFS 采用hash值标识存储文件

**文件上传**

![enter description here](/img/1575035108391.png)
![enter description here](/img/1575035161292.png)

**文件下载**

![enter description here](/img/1575035213445.png) 

![enter description here](/img/1575035246421.png)

**安装配置**

![安装](/img/1575290159935.png)

![服务器配置](/img/1575290242736.png)

![服务器配置](/img/1575290266752.png)

![启动](/img/1575290288546.png)

![安装Nginx](/img/1575290314506.png)


**结合nginx使用，提高多人访问的效率**

获取文件需要借助nginx来获取静态文件。

![安装Nginx](/img/1575290314506.png)

![fastdfs-nginx](/img/1575603749178.png)

注： 是conf目录
![连接fadfs与nginx](/img/1575634128185.png)

![http server配置](/img/1575634466665.png)

![server配置](/img/1575635246200.png)

![启动](/img/1575635485238.png)

上传测试: windows电脑下：
1. 去github下下载zip，解压
2. 把fdfs_client文件夹复制到自己conda环境下
3. 复制远端的client.conf，修改base_path和 网址（一般不用改）
4. 注释掉fdfs_client.sendfile这句代码在storage_client.py
5. 写一个Python文件，一定要在自己的conda环境下！

```python
from fdfs_client.client import Fdfs_client

client = Fdfs_client('F:/Projects/django_env/client.conf')
ret = client.upload_by_filename('timg.jpg')
print(ret)
```

上传成功后：可以使用我们的 http://39.97.170.176:8888/ 做为前缀加上地址来访问图片
![测试上传](/img/1575640031870.png)

**fdfs工作流程**

![fdfs工作流程](/img/1575981798051.png)


**实现fdfs**

* 写一个如下结构：
![fdfs文件](/img/1575984532516.png)
* storage.py中继承官方的Storage类并重写方法

```python
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FDFSStorage(Storage):

    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        client = Fdfs_client(self.client_conf)

        # 上传文件内容
        res = client.upload_by_buffer(content.read())
        # return dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None

        if res.get('Status') !=  'Upload successed.':
            # 上传失败
            raise Exception('上传文件到DFS失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        # 返回文件ID
        return filename

    def exists(self, name):
        return False


    def url(self, name):
        '''返回文件url'''
        return self.base_url+name

```

* 最后在settings中加入

```python
#配置文件存储器
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'

#设置fdfs 的client.conf文件路径
FDFS_CLIENT_CONF='./utils/fdfs/client.conf'

#FDFS服务器地址
FDFS_URL='http://39.97.170.176:8888/'
```

**总结**

使用fdfs好处：
1. 海量存储，存储内容易扩展
2. 解决文件内容重复
3. 结合nginx，提高网站提供图片的效率
