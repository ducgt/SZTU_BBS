# SZTUBBS
技大论坛小程序前端及后台代码

小程序已上线

![image](https://github.com/XuShiKang/SZTU_BBS/demo_img/qrcode.png)

## 前端
***
### 微信小程序(wxapp)

- 图书馆研讨室预约功能(未上线)
- 组队打卡功能
- 狼人杀分配角色功能
- 动图制作功能
- 查看学校公文通功能
- 教务系统验证功能

由于微信小程序官方对社交功能的严格把控，我们的论坛功能无法放入小程序内部，所以只有使用内嵌webvive来实现我们的论坛功能，因此我们做了一个H5网页来实现论坛功能

### H5网页论坛(website_h5)

- 使用一个基于vue的国产框架uniapp制作
- 包含了论坛的基本功能
- 由于是H5，性能和功能方面有很多问题，目前只能将就

## 示例图片
***
### 小程序页面

<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/tools.png" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/notice.jpg" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/enter.jpg" width = "30%" style="margin: 1%" alt="图片名称" align=center />

### H5论坛页面

<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/index0.png" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/index1.png" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/index2.png" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/topic_list.jpg" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/topic_detail.jpg" width = "30%" style="margin: 1%" alt="图片名称" align=center />
<img src="https://github.com/XuShiKang/SZTU_BBS/demo_img/topic_detail_.png" width = "30%" style="margin: 1%" alt="图片名称" align=center />

## 后端
***
### Django服务器(server)

- 使用Python的web框架django，便于敏捷开发
- 服务器只做API，前后端分离
- 实现前端所需的读取数据功能
- 由于小型开发，只使用了简单的sqlite数据库
- 服务器带宽较小，无法存放图片，我们使用了腾讯云的对象存储存储图片，数据库记录url
- 使用xadmin作为后台管理系统
- 尽可能将多的数据用后台动态管理，前端数据不写死
- 使用selenium实现教务系统的模拟登录，验证用户的身份

### 后台管理界面

![image](https://github.com/XuShiKang/SZTU_BBS/demo_img/bg.png)

## 如何在你的电脑运行起来

### 小程序端

将app.js内globalData的host和webview_host改成你的本地服务器地址
```js
globalData: {
    //django一般泡在8000端口，可以自行设置
    host: "127.0.0.1:8000"
    // uniapp一般在8080端口，具体自行设置
    webview_host: "127.0.0.1:8080" 
}
```
### H5论坛

去[dcloud官网](https://www.dcloud.io/)下载官方工具, 编译运行即可

### 后台

安装环境依赖，直接运行即可，具体先了解django框架
```
# 在8000端口跑后台
python manage.py runserver 8000
# 创建后台管理用户密码
python manage.py createsuperuser
```

## 总结

这是我们团队的第一个练手项目，耗时一个多月，边做边学，完成了这个web应用

现在看着自己以前写的代码，觉得自己的代码能够改善的地方还有很多，不过，代码能跑就行了吧，动代码太费时间还有可能出bug，没事还是别碰吧。

