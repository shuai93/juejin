## 前言

参与掘金活动的文章内一般都是要包含活动的链接，但是在活动结束后又不希望文章中包含类似的活动链接。


所以要做的就是更新文章，并重新发布。

## 具体的脚本

脚本见 script/update_and_republish.py

主要参数：

- `session_id` 掘金cookies sessionid
- `act_start_datetime` 活动开始时间
- `act_end_datetime` 活动结束时间
- `pattern_str` 活动链接的正则表达式


## 使用方式

python script/update_and_republish.py \
"4085b767c41edc448faec9ab1b53dcb6" \
"2021-07-01 00:00:00" \
"2021-08-01 00:00:00" \
"「本文已参与好文召集令活动，点击查看：\[后端、大前端双赛道投稿，2万元奖池等你挑战！\]\(https\://juejin\.cn/post/6978685539985653767\)」"
