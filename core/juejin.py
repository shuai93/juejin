import requests

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

    # 掘金沸点
    short_msg_url = "https://api.juejin.cn/content_api/v1/short_msg/publish"

    # 掘金钻石数量
    point_url = "https://api.juejin.cn/growth_api/v1/get_cur_point"

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

    def get_curl_point(self):
        # {
        #   "err_no": 0,
        #   "err_msg": "success",
        #   "data": 436
        # }
        return self.request("get", self.point_url)

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

        data = {
            "draft_id": draft_id,
            "sync_to_org": False,
            "column_ids": column_ids
        }
        result = self.request('post', self.publish_url, json=data)
        return result

    def short_msg_publish(self, content):
        # 好文推荐的沸点
        data = {
            "content": content,
            "topic_id": "6824710203389247501",
        }
        return self.request('post', self.short_msg_url, json=data)

