---
title: Centos 部署 Django
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

### 1. 下载必要库

```
yum -y groupinstall "Development tools"
```

### 2. 下载最新SQLITE

到SQLite官网的下载页面：https://www.sqlite.org/download.html  这里是最新的版本，我们就安装它吧。

```
wget https://www.sqlite.org/2017/sqlite-autoconf-3160200.tar.gz
tar zxvf sqlite-autoconf-3160200.tar.gz
cd sqlite-autoconf-3160200

./configure
make
sudo make install
```

以默认方式安装后，会把编译好的二进制文件安装到 /usr/local/lib， 把头文件sqlite3.h sqlite3ext.h安装到/usr/local/include。

用这两条命令确认一下已成功安装到这里：

```
ls -l /usr/local/lib/*sqlite*
ls -l /usr/local/include/*sqlite*
```

### 3.Python 安装

```
wget https://www.python.org/ftp/python/3.6.6/Python-3.6.6.tgz
tar -zxvf Python-3.6.6.tgz
```

进入解压好的目录
```

sudo LD_RUN_PATH=/usr/local/lib ./configure --enable-optimizations
sudo LD_RUN_PATH=/usr/local/lib make altinstall

```

建立软链接

```
ln -s /usr/local/python3/bin/python3.6 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3.6 /usr/bin/pip3
```

看Python3和pip3安装情况
```
python3

pip3 -V
```

卸载：

```
whereis python
rm -rf ....
```

### 4. virtualenv安装

```
pip3 install virtualenv
```

建立链接
```
ln -s /usr/local/python3/bin/virtualenv /usr/bin/virtualenv
```
 
 创建虚拟环境
 
 ```
 mkdir -p /data/env
 mkdir -p /data/wwwroot

virtualenv --python=/usr/bin/python3 pyweb
 ```

进入虚拟环境

```
cd /data/env/pyweb/bin
source activate
```

退出虚拟环境

```
deactivate
```

### 5.虚拟环境下安装django, uwsgi

```
pip3 install django （如果用于生产的话，则需要指定安装和你项目相同的版本）
pip3 install uwsgi

ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi
```

### 6. Django下创建项目和app

```
django-admin.py startproject mysite

cd mysite

python3 manage.py startapp blog
```



### 参考文章
https://www.cnblogs.com/djangocn/p/9538551.html
https://stackoverflow.com/questions/55674176/django-cant-find-new-sqlite-version-sqlite-3-8-3-or-later-is-required-found
https://blog.csdn.net/yohjob/article/details/90760862