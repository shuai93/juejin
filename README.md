# juejin


## 项目描述 🔑

一个关于掘金的自动发布文章的脚本


## 项目部署 🥳

目前仅实现了 Github Action 的部署方式，因为我觉得这种方式最适合这个项目。

### 1. Fork 项目 🔗



### 2. Github Action Secrets 配置  🕹

| 变量 | 描述 |  示例 | 用途 |
| --- | --- |  --- |  --- |
| JUEJIN_USERNAME | 掘金登录帐号 |  xxx | 
| JUEJIN_PASSWORD | 掘金登录密码 | xxx |
| JUEJIN_NICKNAME | 掘金昵称 | 西红柿蛋炒饭 | 
| MAIL_USER | 发件人邮箱用户名 |  xxx.qq.com | 
| MAIL_ADDRESS | 发件人邮箱地址 | xxx.qq.com |
| MAIL_HOST | 发件人邮箱服务器 | smt.qq.com |
| MAIL_PASSWORD | 发件人邮箱密码 | xxxxxx |
| MAIL_PORT | 邮箱服务器端口 |  465 |
| MAIL_TO | 收信邮箱 | xxx.qq.com |
| SWITCH | 自动发布开关 | on |


### 3. 运行  Github Action ▶️

关于如何配置以及启动 可以查看我的掘金文章 [ Github Action 的简单使用 ](https://juejin.cn/post/6969119163293892639)

### 4. 查看收件箱 📮

待完善

~~不出意外会收到一封推送文章的邮件~~

## 项目关键技术总结 🏳️

主要的技术点如下：

- Selenium 模拟浏览器操作
- 滑块验证码识别
- request 发送 HTTP 请求
- Github Action 部署项目

如果你有兴趣可以查看我掘金的专栏，可以一步步了解我是如何实现这个项目的。


## 写在最后 🔚

在写此项目的时候只考虑到个人使用帐号进行发布文章，所以此项目适合使用  [Github Action](https://docs.github.com/cn/actions) 进行部署。

当然如果你有自己的服务器，那么我有如下建议：

- 缓存 Selenium 获取到的 cookie （掘金的 cookie过期时间似乎是两个月）。

- 可以使用 Linux cron （Mac、Window 都有对应的定时任务）执行定时任务