# juejin


## 项目描述 🔑

一个关于掘金的自动发布文章的脚本


## 项目部署 🥳

目前仅实现了 Github Action 的部署方式，因为我觉得这种方式最适合这个项目。

### 1. Fork 项目 🔗



### 2. Github Action Secrets 配置  🕹

| 变量 | 描述 |  示例 |
| --- | --- |  --- | 
| JUEJIN_USERNAME | 掘金登录帐号 |  xxx | 
| JUEJIN_PASSWORD | 掘金登录密码 | xxx |
| JUEJIN_NICKNAME | 掘金昵称 | 西红柿蛋炒饭 |


### 3. 运行  Github Action ▶️

关于如何配置以及启动 可以查看我的掘金文章 [ Github Action 的简单使用 ](https://juejin.cn/post/6969119163293892639)

### 4. 查看收件箱 📮

待完善

~~不出意外会收到一封推送文章的邮件~~

## 项目关键技术总结 🏳️

- Selenium 模拟浏览器操作

- 滑块验证码识别

- request 发送 HTTP 请求

## 写在最后 🔚

核心代码见 ` core `

