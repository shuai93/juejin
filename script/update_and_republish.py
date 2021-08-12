import requests
import re
import time
import argparse
import sys
import os
import importlib

from requests import cookies

# 导入掘金的包
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.extend([project_dir])
core = importlib.import_module("core")

"""
一些参数的demo
session_id = "4085b767dcb6"
act_start_datetime = "2021-06-01 00:00:00"
act_end_datetime = "2021-06-30 23:59:59"
pattern="这是我参与更文挑战的第\d*天，活动详情查看： \[更文挑战\]\(https\://juejin\.cn/post/6967194882926444557\)"
pattern1=「本文已参与好文召集令活动，点击查看：\[后端、大前端双赛道投稿，2万元奖池等你挑战！\]\(https\://juejin\.cn/post/6978685539985653767\)」
"""

parser = argparse.ArgumentParser(description='更新文章活动链接重新发布')
parser.add_argument('session_id', type=str, help='掘金cookies sessionid', default="4085b767dcb6")
parser.add_argument('act_start_datetime', type=str, help='活动开始时间', default="2021-06-01 00:00:00")
parser.add_argument('act_end_datetime', type=str, help='活动结束时间', default="2021-07-01 00:00:00")
parser.add_argument('pattern_str', type=str, help='活动链接的正则表达式', default="")

args = parser.parse_args()


def update_and_republish(session_id, act_start_datetime, act_end_datetime, pattern_str):

    # 定义活动链接正则
    pattern = re.compile(pattern_str)

    cookie = requests.cookies.create_cookie(
        domain=".juejin.cn",
        name="sessionid",
        value=session_id
    )

    juejin = core.Juejin(cookie_obj=cookie)
    user_id = juejin.get_user().get("data", {}).get("user_id")
    start_flag = True
    cursor = "0"
    has_more = True

    act_start_time = time.mktime(time.strptime(act_start_datetime, '%Y-%m-%d %H:%M:%S'))
    act_end_time = time.mktime(time.strptime(act_end_datetime, '%Y-%m-%d %H:%M:%S'))

    patterns = [pattern]

    # 获取文章列表
    def art_info():
        nonlocal cursor, has_more
        response = juejin.get_article_list(user_id, cursor)
        has_more = response.get("has_more")
        cursor = response.get("cursor")
        return response.get("data")

    # 删除活动链接后更新文章并发布
    def do_update_and_republish(article_id):

        if article_id != "6987750400849870885":
            return

        draft_id = juejin.get_article_detail(article_id).get("data", {}).get("article_info", {}).get("draft_id")
        if not draft_id:
            return False
        data = juejin.get_draft_detail(draft_id).get("data", {})
        article_draft = data.get("article_draft")
        columns = data.get("columns")
        column_ids = [column.get("column_id") for column in columns]

        def mark_content_replace(mark_content):
            for p in patterns:
                mark_content = re.sub(p, "", mark_content)
            return mark_content

        article = {
            "brief_content": article_draft.get("brief_content"),
            "category_id": article_draft.get("category_id"),
            "cover_image": article_draft.get("cover_image"),
            "edit_type": article_draft.get("edit_type"),
            "html_content": article_draft.get("html_content"),
            "is_english": article_draft.get("is_english"),
            "is_gfw": article_draft.get("is_gfw"),
            "link_url": article_draft.get("link_url"),
            "mark_content": mark_content_replace(article_draft.get("mark_content")),
            "tag_ids": [str(tag_id) for tag_id in article_draft.get("tag_ids")],
            "title": article_draft.get("title"),
            "id": article_draft.get("id"),
        }
        print(article['mark_content'])
        print("文章：" + article.get("title"), end=" ")
        print("更新结果为：" + juejin.draft_update(article).get("err_msg"), end=" ")
        print("发布结果为：" + juejin.draft_publish(draft_id, column_ids).get("err_msg"))

    # 主调度函数
    def do(data):
        for art in data:
            ctime = int(art.get("article_info", {}).get("ctime"))
            if ctime and act_end_time < ctime:
                continue
            elif ctime and act_start_time > ctime:
                nonlocal start_flag
                start_flag = False
                break

            a_id = art.get("article_id")
            do_update_and_republish(a_id)

    while start_flag and has_more:
        do(art_info())


if __name__ == '__main__':
    update_and_republish(**vars(args))
