---
title: Linux与window常用指令
tags: 
- linux
- 指令
---

## linux启动关闭服务

```shell
ps -ef|grep tomcat                        //查看所有进程
kill -9 pid                               //关闭对应pid进程
cd /root/DCIM/apache-tomcat-7.0.90/bin    //打开服务所在的文件夹
ls                                        //查看所有文件 显示除隐藏文件外所有文件及目录的名字
./startup.sh                              //启动.sh文件
tail -f ../logs/catalina.out              //查看指定文件夹里的日志
 
 
ls –a                                     //显示当前目录中的所有文件，包含隐藏文件
```