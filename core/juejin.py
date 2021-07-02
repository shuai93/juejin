
import time
import requests

from requests import cookies
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from .track import track
from .config import *


class Juejin(object):

    # 掘金发布文章URL
    publish_url = "https://api.juejin.cn/content_api/v1/article/publish"

    # 掘金草稿箱文章URL
    article_draft_url = "https://api.juejin.cn/content_api/v1/article_draft/query_list"

    def __init__(self, driver_cookies):

        self.session = requests.session()
        if driver_cookies is False:
            raise Exception("Cookie is Blank")
        for cookie in driver_cookies:
            cookie_obj = requests.cookies.create_cookie(
                domain=cookie.get("domain"),
                name=cookie.get("name"),
                value=cookie.get("value")
            )
            self.session.cookies.set_cookie(cookie_obj)

    def push_draft_last_one(self):
        article_draft = self.get_draft()
        if article_draft:
            raise Exception("The article draft is empty")
        draft_id = article_draft[0].get("id")
        return draft_id, self.publish(draft_id)

    def request(self, *args, **kwargs):

        response = self.session.request(*args, **kwargs)
        if response.status_code != 200:
            raise Exception("请求错误")
        return response.json()

    def get_draft(self):
        result = self.request('post', self.article_draft_url)
        return result.get("data", [])

    def publish(self, draft_id):

        body = {
            "draft_id": draft_id,
            "sync_to_org": False,
            "column_ids": []
        }
        result = self.request('post', self.publish_url, body=body)
        return result


class JuejinDriver(object):
    # 掘金首页
    juejin_home = "https://juejin.cn/"

    # 截屏
    screenshot_verify_image = 'temp/verify_image.png'
    screenshot_prepare_login = 'temp/prepare_login.png'

    # 重试
    retry = 10

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.juejin_username = JUEJIN_USERNAME
        self.juejin_password = JUEJIN_PASSWORD
        self.juejin_nickname = JUEJIN_NICKNAME
        print(JUEJIN_USERNAME, JUEJIN_PASSWORD, JUEJIN_NICKNAME)
        self.driver = webdriver.Chrome(executable_path="./driver/linux/chromedriver", chrome_options=chrome_options)
        self.driver.get(self.juejin_home)

    def run(self):
        try:
            self.prepare_login()
        except Exception as e:
            self.driver.save_screenshot(self.screenshot_prepare_login)
            raise Exception("Prepare login is error" + str(e))
        flag = False
        for retry in range(self.retry):
            self.get_cookies(retry + 5)
            try:
                avatar = self.driver.find_element(By.XPATH, '''//img[@alt="西红柿蛋炒饭的头像"]''')
                if avatar:
                    flag = True
                    break
            except NoSuchElementException:
                pass

        if flag is False:
            raise Exception(f"Verify slide image error and retry {self.retry}! ")

        return self.driver.get_cookies()

    def get_cookies(self, num):
        slider_url, background_url = self.get_verify_image_url()
        result = track.get_track(slider_url, background_url)
        self.click_and_move(result)
        time.sleep(num)

    def click_and_move(self, slide_track):
        verify_div = self.driver.find_element(By.XPATH, '''//div[@class="sc-kkGfuU bujTgx"]''')

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(verify_div).perform()
        time.sleep(0.5)
        # 遍历轨迹进行滑动
        for t in slide_track:
            time.sleep(0.01)
            ActionChains(self.driver).move_by_offset(xoffset=t, yoffset=0).perform()
        # 释放鼠标
        ActionChains(self.driver).release(on_element=verify_div).perform()

    def get_verify_image_url(self):

        # 获取验证图片
        verify_image1 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[1]''')
        verify_image2 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[2]''')
        verify_image1_src = verify_image1.get_attribute("src")
        verify_image2_src = verify_image2.get_attribute("src")
        self.driver.save_screenshot(self.screenshot_verify_image)
        return verify_image1_src, verify_image2_src

    def prepare_login(self):

        login_button = self.driver.find_element(By.XPATH, '''//button[text()="登录"]''')

        ActionChains(self.driver).move_to_element(login_button).click().perform()

        time.sleep(5)

        other_login_span = self.driver.find_element(By.XPATH, '''//span[text()="
          其他登录方式
        "]''')

        ActionChains(self.driver).move_to_element(other_login_span).click().perform()
        time.sleep(2)

        username_input = self.driver.find_element(By.XPATH, '//input[@name="loginPhoneOrEmail"]')
        password_input = self.driver.find_element(By.XPATH, '//input[@name="loginPassword"]')
        # 保护用户名密码
        self.driver.execute_script("arguments[0].type = 'password';", username_input)
        username_input.send_keys(self.juejin_username)
        password_input.send_keys(self.juejin_password)

        login_button = self.driver.find_element(By.XPATH, '''//button[text()="
        登录
      "]''')
        ActionChains(self.driver).move_to_element(login_button).click().perform()

        time.sleep(5)
