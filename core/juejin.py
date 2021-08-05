import requests
import re
import time

from requests import cookies


class Juejin(object):

    # 掘金发布文章URL
    publish_url = "https://api.juejin.cn/content_api/v1/article/publish"

    # 掘金草稿箱文章URL
    article_draft_url = "https://api.juejin.cn/content_api/v1/article_draft/query_list"

    # 掘金草稿箱文章详情
    article_draft_detail_url = "https://api.juejin.cn/content_api/v1/article_draft/detail"

    # 掘金草稿箱文章详情
    article_draft_update_url = "https://api.juejin.cn/content_api/v1/article_draft/update"

    # 掘金草稿箱文章详情
    article_detail_url = "https://api.juejin.cn/content_api/v1/article/detail"

    # 文章列表
    article_list_url = "https://api.juejin.cn/content_api/v1/article/query_list"

    # 获取用户信息
    user_url = "https://api.juejin.cn/user_api/v1/user/get"

    # 掘金抽奖 URL
    lottery_url = "https://api.juejin.cn/growth_api/v1/lottery/draw"

    def __init__(self, driver_cookies=None, cookie_obj=None):
        self.session = requests.session()
        if driver_cookies:
            for cookie in driver_cookies:
                cookie_obj = requests.cookies.create_cookie(
                    domain=cookie.get("domain"),
                    name=cookie.get("name"),
                    value=cookie.get("value")
                )
                self.session.cookies.set_cookie(cookie_obj)
        elif cookie_obj:
            self.session.cookies.set_cookie(cookie_obj)
        else:
            raise Exception("Cookie is Blank")

    def push_draft_last_one(self):
        article_draft = self.get_draft().get("data", [])
        if not article_draft:
            raise Exception("The article draft is empty")
        draft_id = article_draft[0].get("id")

        result = self.draft_publish(draft_id)
        print(result)
        if result.get("err_no", "") != 0:
            err_msg = result.get("err_msg", "")
            raise Exception(f"Juejin push article error, error message is {err_msg} ")
        return result.get("data", {})

    def request(self, *args, **kwargs):

        response = self.session.request(*args, **kwargs)
        if response.status_code != 200:
            raise Exception("Request error")
        return response.json()

    def draw_lottery(self):
        return self.request("post", self.lottery_url)

    def get_user(self):
        return self.request("get", self.user_url)

    def get_article_list(self, user_id, cursor="0"):
        data = {
            "user_id": user_id,
            "sort_type": 2,
            "cursor": cursor
        }
        return self.request("post", self.article_list_url, json=data)

    def get_draft(self):
        return self.request('post', self.article_draft_url)

    def get_draft_detail(self, draft_id):
        return self.request("post", self.article_draft_detail_url, json={"draft_id": draft_id})

    def get_article_detail(self, article_id):
        return self.request("post", self.article_detail_url, json={"article_id": article_id})

    def draft_update(self, article_info):
        return self.request('post', self.article_draft_update_url, json=article_info)

    def draft_publish(self, draft_id, column_ids=None):

        if column_ids is None:
            column_ids = []

        json = {
            "draft_id": draft_id,
            "sync_to_org": False,
            "column_ids": column_ids
        }
        result = self.request('post', self.publish_url, json=json)
        return result


def lottery():

    # session id 自行设置
    session_id = ""

    cookie = requests.cookies.create_cookie(
        domain=".juejin.cn",
        name="sessionid",
        value=session_id
    )
    juejin = Juejin(cookie_obj=cookie)

    gift = {}
    num = 1

    while True:
        result = juejin.draw_lottery()
        if result.get("err_no") == 0:
            lottery_name = result.get("data", {}).get("lottery_name")
            if gift.get(lottery_name):
                gift[lottery_name] += 1
            else:
                gift[lottery_name] = 1
            print(f"第{num}次-抽奖结果为：{lottery_name}")
            num += 1
        else:
            print(result.get("err_msg"))
            break

    print(f"总抽奖次数为：{num}")

    print("最终抽奖结果为：")
    for k, v in gift.items():
        print(f"礼物：{k} ---- 个数：{v}")


def update_and_republish():

    # 定义活动时间
    act_start_datetime = "2021-06-01 00:00:00"
    act_end_datetime = "2021-06-30 23:59:59"

    # 定义活动链接正则
    pattern1 = re.compile(r"这是我参与更文挑战的第\d*天，活动详情查看： \[更文挑战\]\(https\://juejin\.cn/post/6967194882926444557\)\n")
    pattern2 = re.compile(r"这是我参与更文挑战的第\d*天，活动详情查看： \[更文挑战\]\(https\://juejin\.cn/post/6967194882926444557\)")

    # session id 自行设置
    session_id = ""

    cookie = requests.cookies.create_cookie(
        domain=".juejin.cn",
        name="sessionid",
        value=session_id
    )
    juejin = Juejin(cookie_obj=cookie)

    user_id = juejin.get_user().get("data", {}).get("user_id")
    start_flag = True
    cursor = "0"
    has_more = True

    act_start_time = time.mktime(time.strptime(act_start_datetime, '%Y-%m-%d %H:%M:%S'))
    act_end_time = time.mktime(time.strptime(act_end_datetime, '%Y-%m-%d %H:%M:%S'))

    patterns = [pattern1, pattern2]

    # 获取文章列表
    def art_info():
        nonlocal cursor, has_more
        response = juejin.get_article_list(user_id, cursor)
        has_more = response.get("has_more")
        cursor = response.get("cursor")
        return response.get("data")

    # 删除活动链接后更新文章并发布
    def do_update_and_republish(article_id):
        # if article_id != '6970265949941760030':
        #     return
        draft_id = juejin.get_article_detail(article_id).get("data", {}).get("article_info", {}).get("draft_id")
        if not draft_id:
            return False
        data = juejin.get_draft_detail(draft_id).get("data", {})
        article_draft = data.get("article_draft")
        columns = data.get("columns")
        column_ids = [column.get("column_id") for column in columns]

        def mark_content_replace(mark_content):
            for pattern in patterns:
                mark_content = re.sub(pattern, "", mark_content)
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
    # update_and_republish()
    lottery()
