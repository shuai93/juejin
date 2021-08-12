## 前言

掘金签到抽奖的功能上线一个月有余了，想着攒了不少钻石。所以就研究了掘金抽奖的接口。


掘金抽奖是没有过多的逻辑校验，在已登陆的情况下调用的接口 `https://api.juejin.cn/growth_api/v1/lottery/draw`

## 具体的脚本

脚本见 script/lottery.py

主要参数：

- `session_id` 掘金cookies sessionid


## 使用方式

python script/lottery.py 4085b767dcb6
