---
title: 天天生鲜项目实例P2
date: 2022-05-19 21:28:29
updated: 2022-05-19 21:28:29
top_img: false
cover: /img/1576549292557.png
categories:
- Python
tags: 
- Python
- Note
- Django
- 实例
---

## 首页模块


**IndexView中加入信息**

在goods/views.py加入indexview的功能

```python
from django.urls import path
from .views import IndexView

app_name = 'goods'
urlpatterns = [
    path('', IndexView.as_view() ,name='index')
]

```

```python
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from django_redis import get_redis_connection
from django.core.cache import cache
from goods.models import GoodsType, IndexGoodsBanner, IndexTypeGoodsBanner, IndexPromotionBanner, GoodsSKU
from order.models import OrderGoods

class IndexView(View):
    def get(self, request):
        # get all goods type
        types = GoodsType.objects.all()

        # 获取首页轮播商品信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')

        # 获取促销信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        # 获取分类商品展示信息
        for type in types:
            #获取图片类的banner展示信息
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
            #获取文字类的banner展示信息
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)

            #添加属性
            type.image_banners = image_banners
            type.title_banners = title_banners

        #获取用户购物车中的商品数目
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            # 用户已登录有授权
            conn = get_redis_connection('default')
            cart_key = 'cart_%d'%user.id
            cart_count = conn.hlen(cart_key)

        # 组织上下文
        context = {
            'types':types,
            'goods_banners':goods_banners,
            'promotion_banners':promotion_banners,
            'cart_count':cart_count
        }

        # 使用模板
        return render(request, 'index.html', context)

```

**使用celery生成Index的static文件**

新建任务：

> 注意：
> 1.from goods.models 要在django.setup之后
> 2.worker端的fdfs_client需要升级到Python3的exception写法。
> 3.worker端的fdfs_client考虑先将utils的import注释

```python
@app.task
def generate_static_index_html():
    # get all goods type
    types = GoodsType.objects.all()

    # 获取首页轮播商品信息
    goods_banners = IndexGoodsBanner.objects.all().order_by('index')

    # 获取促销信息
    promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

    # 获取分类商品展示信息
    for type in types:
        # 获取图片类的banner展示信息
        image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1)
        # 获取文字类的banner展示信息
        title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0)

        # 添加属性
        type.image_banners = image_banners
        type.title_banners = title_banners

    # 组织上下文
    context = {
        'types': types,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners,
    }

    # 使用模板
    # 1.加载模板文件
    temp = loader.get_template('static_index.html')
    # 2.渲染
    static_index_html = temp.render(context)

    # 生成首页的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w') as f:
        f.write(static_index_html)
```

![流程](/img/1576549292557.png)

**在admin的委托返回调用中，执行celery**

在goods的admin.py中监听一下admin后台的save和delete操作，然后执行celery刷新内容返回。

![执行流程](/img/1576551196217.png)

 在admin.py中加入

```python
class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # 先执行数据库操作
        super().save_model(request, obj, form, change)

        # 发送celery事件
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()

    def delete_model(self, request, obj):
        # 先执行数据库操作
        super().delete_model(request, obj)

        # 发送celery事件
        from celery_tasks.tasks import generate_static_index_html
        generate_static_index_html.delay()
```

> 遇到问题： 第一次修改后，celery生成的页面太快了，还没等save-model结束，因此查出来的数据是旧的。下一次又可以刷出最新数据
> 方案：在celery里加入一个等待，保证model已经处理完数据库了，这样celery任务可以查到最新的结果。

**将index页面的两种获取方式调度起来**

![静态页面的调度](/img/1576554364999.png)

**使用django的缓存机制存储页面**

https://docs.djangoproject.com/zh-hans/3.0/topics/cache/

* 存储

```python
cache.set()
pass
cache.get()
```

* 更新
在admin.py里进行清空缓存

```python
        # 清缓存
        cache.delete(index_cache_key)
```

> 小结：缓存机制的目的之一在于防止黑客利用各多台电脑进行访问型攻击（DDOS），缓存通过减少数据库的查询次数，实现对性能的优化。

![缓存机制](/img/1576636756891.png)

**使用redis存储购物车数据**

![讨论](/img/1576722037256.png)


## 商品详情页面

**1.views.py 为页面添加必要数据**

```python
# 商品详情页
    def get(self, request, goods_id):

        try:
            # 拿商品SKU
            good_sku = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse("goods:index"))

        # 拿所有类型
        all_good_types = GoodsType.objects.all()

        # 拿商品评论并排除掉commit为空的
        sku_orders = OrderGoods.objects.filter(sku=good_sku).exclude(comment='')

        # 拿同类型的商品（以时间倒序）
        new_skus = GoodsSKU.objects.filter(type=good_sku.type).order_by("-create_time")

        # 获取购物车数量
        user = request.user
        cart_count = 0

        if user.is_authenticated:
            # 用户已登录有授权
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        # 上下文组织，sku,types, sku_orders, new_skus, cart_count
        context = {
            "sku": good_sku,
            "types": all_good_types,
            "sku_orders": sku_orders,
            "new_skus": new_skus,
            "cart_count": cart_count
        }

        return render(request, 'detail.html',context)
```

**2.页面编辑**

使用双curly braces（放变量）或百分号的curly braces（放语句）

 forloop.counter来获取循环当前的ID

**3.关闭escape转义**

1.使用autoescape off来关闭转义，

![关闭转义](/img/1576810604102.png)

2.使用| safe来关闭转义

![用safe关闭转义](/img/1576810673369.png)


## 商品列表页

**分析页面**

> 使用/list/type/page?sort=default 这种地址来设计

**分页的功能实现**

> 使用Paginator分页来查询分页

**路径传递方式**

![路径传递方式](/img/1577414335373.png)

**页码控制**

![控制显示的页码](/img/1577414816762.png)

> 遇到一个问题：get误写成filter，后果就是把这些结果放里面搜索会报 The QuerySet value for an exact lookup must be limited to one result using slicing. 以后需要注意


**搜索引擎与全文检索**

使用haystack的全文检索框架，whoosh的搜索引擎

![结构分析](/img/1578122441016.png)

![全文检索](/img/1578122530429.png)


* 安装和配置

![安装](/img/1578122591339.png)

![配置haystack](/img/1578122991267.png)

>haystack默认安装无如下内容，需按情况配置
![配置](/img/1578123391128.png)

> 索引文件生成：
![索引文件生成：](/img/1578123481409.png)


[官网](https://django-haystack.readthedocs.io/en/master/signal_processors.html)


![索引类定义](/img/1578365001196.png)
![建立索引](/img/1578377646492.png)

改成如下：

```python
# 定义索引类

from haystack import indexes
# 导入模型类
from goods.models import GoodsSKU

#指定类建立索引
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段， use_template表明把哪些字段建立索引文件（使用一个模板文件来说明）
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
```

> 手动建立模型文件
templates / search / indexes / 【app】 / 【模型类全小写】_text.txt

![全文检索](/img/1578378838931.png)


* 使用

![结果](/img/1578378917671.png)
> 表单中，参数名：q为写死的。method=‘get’是写死的
url的路径配置必须也是haystack.urls模块

> 改变分词方式：
![改变分词方式](/img/1578379986297.png)

创建ChineseAnalyzer.py，写入：

![内容截图](/img/1578380200054.png)
![内容截图2](/img/1578380227603.png)

![更改默认分析](/img/1578380391307.png)

![更新分词方式](/img/1578380648851.png)

> 总结： 选一个全文搜索的框架，如这里的haystack（django内置的），再找一个搜索引擎，如这里的whoosh引擎， 使用时会生成index文件，一般在配置中指明。在执行搜索时，引擎会在Index中查找。 另外也可以为其指定一个分词规则，如这里的jieba，这样可以根据分词来生成搜索。


## 购物车模块

**商品详情个数的JS**

```js
update_price();
function update_price(){
	price = $('.show_pirze').children('em').text();
	count = $('.num_show').val();

	price = parseFloat(price);
	count = parseInt(count);
	amount = price * count;
	$('.total').children('em').text(amount.toFixed(2)+'元');//保留两位小数
}
$('.add').click(function () {
	count = $('.num_show').val();
	count = parseInt(count)+1;
	$('.num_show').val(count);
	update_price();
});

$('.minus').click(function () {
	count = $('.num_show').val();
	count = parseInt(count)-1;
	if(count <= 0){
		return;
	}
	$('.num_show').val(count);
	update_price();
});
```

**购物车添加的请求设计**

流程：
1. 采用ajax， post请求
2. 传递参数，商品ID，数量

> 目前为止，有post,get,url三种类型的请求类型，
> 对于访问数据为主的参数，一般使用get请求
> 对于涉及增删改的参数，一般使用post请求。

> 另外，django防止csrf的方式，默认打开csrf中间件，post提交时加上csrf token标签
![csrf生成的代码](/img/1578454158486.png)
> Ajax发起的请求都在后台，在浏览器看不到效果
> 前后端合作过程中，得确定好请求方式和参数

![enter description here](/img/1578453777774.png)
![enter description here](/img/1578453790169.png)
![enter description here](/img/1578454203406.png)
![enter description here](/img/1578454302221.png)