# juejin


## 项目描述 🔑

一个关于掘金的自动化的脚本

主要的技术点如下：

- Selenium 模拟浏览器操作
- 滑块验证码识别
- request 发送 HTTP 请求
- Github Action 部署项目

主要的功能点：

- 掘金自动登录
- 掘金自动签到、抽奖
- 自动发布文章
- 批量更新文章内容（统一删除活动链接）
- 批量抽奖（梭哈钻石-解放双手）

如果你有兴趣可以查看[我掘金的专栏](https://juejin.cn/column/6980219687397228551)，可以一步步了解我是如何实现这个项目的。


## 项目部署 🥳

目前仅实现了 Github Action 的部署方式，因为我觉得这种方式最适合这个项目。

### 1. Fork 项目 🔗

![image](https://user-images.githubusercontent.com/21220871/124370460-a2464f80-dcaa-11eb-85b9-fbbb8552035b.png)


### 2. Github Action Secrets 配置  🕹

关于邮件配置，推荐使用QQ邮箱。163邮箱可能会有问题。

ps:如下参数需要挨个配置；如不需邮件功能，需要修改 main.py 中的代码，删除对应的校验即可。

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
| SWITCH | 脚本开关 | on |
| PUBLISH_SWITCH | 自动发布开关 | off |

![image](https://user-images.githubusercontent.com/21220871/124370464-ba1dd380-dcaa-11eb-9c51-30cab0fdf98c.png)


### 3. 运行  Github Action ▶️

![image](https://user-images.githubusercontent.com/21220871/124370473-cf92fd80-dcaa-11eb-8238-e8f04a8c9828.png)

ps：默认情况下提交代码到 master 分支就会触发一次构建。

关于如何配置以及启动 可以查看我的掘金文章 [ Github Action 的简单使用 ](https://juejin.cn/post/6969119163293892639)

### 4. 查看运行结果 😬

![image](https://user-images.githubusercontent.com/21220871/124370571-bc346200-dcab-11eb-9a88-3f9067dc9047.png)


### 5. 查看收件箱 📮

不出意外会收到一封推送文章的邮件

![image](https://user-images.githubusercontent.com/21220871/124370449-85118100-dcaa-11eb-99a9-9ce0c5de57ae.png)

## 其他功能

`core/juejin.py update_and_republish` 新增文章批量更新功能。

主要目的用脚本的方式移除掘金活动的文案及链接， 以保证文章的美感。

使用方式为

```bash
# 1. 配置sessionid

# 2. 配置活动链接以及活动时间

# 3. 执行脚本
python3  core/juejin.py

# 4. 查看结果
文章：程序员，申请个域名吧 更新结果为：success 发布结果为：success
文章：掘金登录引发的思考 更新结果为：success 发布结果为：success
文章：Python Selenium 使用指南 更新结果为：success 发布结果为：success
文章：Java 常见知识整理 更新结果为：success 发布结果为：success
文章：Django REST framework 完结 更新结果为：success 发布结果为：success
```




## 写在最后 🔚

在写此项目的时候只考虑到个人使用帐号进行发布文章，所以此项目适合使用  [Github Action](https://docs.github.com/cn/actions) 进行部署。

当然如果你有自己的服务器，那么我有如下建议：

- 缓存 Selenium 获取到的 cookie （掘金的 cookie过期时间似乎是两个月）。

- 可以使用 Linux cron （Mac、Window 都有对应的定时任务）执行定时任务
