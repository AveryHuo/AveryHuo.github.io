---
title: Addressable打包流程
categories:
- 工作相关
tags: 
- CI
---
# 安卓打包流程

## 1. [Python]  添加配置
* 1.添加项目配置 vms/config/config.txt
* 2.新建一个config文件到 vms/config/platform_{project}_{branch/version}.txt
  
 >2的文件 将作为打包后项目带出去的platform.txt的模板
 > platform.txt在打包流程中 判断 branch是否以t开头，是则用1，否则用第一个字符设置为platformId
 

 ```python
 -------------------------------------------------
   File Name：     ModifyJsonFileHandler
   Author :       hujunhao
   date：          2018/3/16 16:03
   Description : 修改platform.txt文件
-------------------------------------------------
"""
class ModifyJsonFileHandler(BaseHandler):
    def __init__(self):
        super(ModifyJsonFileHandler, self).__init__(constants.H_MODIFY_JSON_FILE)
        pass

    def excute(self, args):
        version = args[0]
        publish_path = args[1]
        plat_path = args[2]
        to_path = args[3]

        cur_date_time = datetime.datetime.now()
        cur_date_time.strftime('%m%d%H%M')
        publish_data = script.configMgr.load_file(publish_path)
        ver_str = '%s_%s_%s_%s' % (
            version, publish_data['appVersion'], publish_data['resVersion'], cur_date_time.strftime('%m%d%H%M'))

        plat_data = script.configMgr.load_file(plat_path)
        plat_data['verInfo'] = ver_str

        # M by Yuk 2018-08-03
        # 修复不同platformId被覆盖回默认platformId的bug
        # platformId 取分支号
        platformId = str(version[0])
        if platformId == 't' or platformId == '0':
            platformId = 1
            pass
        plat_data['platformId'] = platformId
        
        script.configMgr.save_file(plat_data, to_path)

        return True

    pass

 ```


 ## 2. [Python]  执行流程： B_PACK_RES  [Unity] :PackAllRes 
 * 打包所有资源
 * 设置目录： res_ab: output\testsg\output\res\res_ab

## 3.[Python] 执行流程：B_CREATE_PUBLISH [Unity]: UpdateVersionAndPublishFile
* 创建项目内的publish.txt和xxx_version.txt
  
## 4.[Python] 执行流程：B_BUILD_PROJECT [Unity]: BuildProject
* 生成安卓工程
* 将调用Unity中对Manifest文件已经修改

## 5.[Python] 执行流程：B_COMMIT_MOBILE 
* 将资源提交到SVN

## 6.[Python] 执行流程：B_CREATE_ANDROID_APP 
* 生成安卓 apk。
 
## 7.上传资源： [Python]: H_UPLOAD_CDN_COMPRESS
 * 上传本地生成的diff.txt中的文件到cdn
 * 内容示例如下：
  ![diff文件内容](/img/1600238267260.png)
 
## 8.打补丁包： [Python]：H_GENERATE_PATCH_CDN_COMPRESS
 * 输入参数: 起始版本，目标版本
 * 1. 获取两个版本的version文件
 * 2. 获取version中的catalogs, resources文件列表，以目标版本为准，起始版本中不同的记录到diff列表中
 * 3. 将diff列表中的文件遍历出，并压缩为 [start_version]_[target_version]patch.7z
 * 4.在目标版本的version文件中，添加压缩文件名到patchs字段
 * 5. 上传修改后的新的version文件
 * 结果如图：
 ![生成的364-384的补丁包](/img/1600238404872.png)


# 加载流程
## 1. 获取所有项目内版本号及version文件
* GetLocalVersion 的System执行， 如图获取 resVersionInPack, resVersionInSD, appVersionInPack
 ![加载本地的版本号信息](/img/1600233059102.png)
 
 ## 2. 加载Addressable的Catelog
 * GetLocalVersion System结束时调用
 
## 3. 加载服务端的md5文件，notice文件，server文件，version文件
* GetServerList System执行
* * Server的根地址： 包体内的plaform.txt指明的serverKey, mCenterUrl
 
* md5文件: {mCenterUrl}static/md5/{mChannel}.json。 从其中获取如图内容
![md5文件内容](/img/1600236947016.png)
* notice文件： {mCenterUrl}static/notice/login/{mChannelKey}.json
* server文件： {mCenterUrl}static/server/{mChannelKey}.json
 
 
## 4. 判断是否需要强更？[非Editor]
 * DownloadApp System执行
 * 服务端给的APP版本号，如果比appVersionInPack要大，则强更，跳转到下载地址
  
  
## 5. 更新资源文件 [非Editor] 
* DownloadUpdateFiles System执行
* 服务端的res版本号，如果比(resVersionInPack与resVersionInSD中的最大者)大，则下载服务端的version文件

* 服务端version文件： cdnUrl / Resources/[Android/iOS/Windows/Mac]/xxx_version.7z
* 下载服务端版本文件并解压
* 1.查找patches列表，如果存在 [resVersionInPack]_[服务端res_version]patch.7z 文件名，则进入补丁包快速下载流程
* 2.未找到对应的patches记录，进入资源列表下载流程。
  
 >A: 补丁包快速下载流程：
 > 1. 补丁包地址： cdnUrl / Resources/[Android/iOS/Windows/Mac]/[resVersionInPack]\_[服务端res_version]patch.7z
 > 2. 解压补丁包到persistantData下，记录最新catalog名称，完成下载流程
 >B: 资源下载流程:
> 对比得到 mCoreUpdateDic 必更资源列表，mAfterUpdateDic 随后（运行时）更新的资源列表
> 结果： 
  1.mCoreUpdateDic与mAfterUpdateDic为空？ ： 将服务端的version文件复制到本地sd下
  2.进行下载，并记录catelog文件名称，完成后，再次检测mCoreUpdateDic与mAfterUpdateDic，循环直到1成立
  

## 6. [再次]加载Addressable的Catelog
 * DownloadUpdateFiles System执行
 * 设置当前资源版本号为服务端
 
## 7. 进入登录，执行LoginPreload, InitLua, EnterLogin进入游戏
