
import cv2
import numpy as np
import time
import requests

from requests import cookies
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class Juejin(object):

    # 处理前图片
    slider = "temp/slider.png"
    background = "temp/background.png"

    # 将处理之后的图片另存
    slider_bak = "temp/slider_bak.png"
    background_bak = "temp/background_bak.png"

    # 截屏
    screenshot_path = 'temp/screenshot.png'

    # 掘金发布文章URL
    publish_url = "https://api.juejin.cn/content_api/v1/article/publish"

    # 掘金草稿箱文章URL
    article_draft_url = "https://api.juejin.cn/content_api/v1/article_draft/query_list"

    # 掘金用户名密码
    juejin_username = ""
    juejin_password = ""

    def __init__(self):
        
        self.driver = webdriver.Chrome(executable_path="./driver/chromedriver")
        self.driver.get("https://juejin.cn/")
        self.session = requests.session()

    def run(self):
        slider_url, background_url = self.get_verify_image_url()
        self.driver.save_screenshot(self.screenshot_path)
        distance = self.juejin_slide_distance(slider_url, background_url)
        print("需要滑动的距离为：", distance)

        track = self.get_track(int(distance)-1)
        self.click_and_move(track)
        print()

    def prepare_session(self):
        if self.driver.get_cookies() is False:
            raise Exception("Cookie is Blank")

        for cookie in self.driver.get_cookies():
            cookie_obj = requests.cookies.create_cookie(
                domain=cookie.get("domain"),
                name=cookie.get("name"),
                value=cookie.get("value")
            )
            self.session.cookies.set_cookie(cookie_obj)

    def publish(self):
        article_draft_response = self.session.post(self.article_draft_url)
        if article_draft_response.status_code != 200:
            raise Exception("Query article draft Error")
        data = article_draft_response.json().get("data", [])

        if data is False:
            raise Exception("No article to publish")

        body = {
            "draft_id": data[0].get("id"),
            "sync_to_org": False,
            "column_ids": []
        }
        self.session.post(self.publish_url, body=body)

    def click_and_move(self, track):
        verify_div = self.driver.find_element(By.XPATH, '''//div[@class="sc-kkGfuU bujTgx"]''')

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(verify_div).perform()
        time.sleep(0.5)
        # 遍历轨迹进行滑动
        for t in track:
            time.sleep(0.01)
            ActionChains(self.driver).move_by_offset(xoffset=t, yoffset=0).perform()
        # 释放鼠标
        ActionChains(self.driver).release(on_element=verify_div).perform()
        time.sleep(5)

    @staticmethod
    def get_track(distance):  # distance为传入的总距离
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 1

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 4
            else:
                # 加速度为-2
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def get_verify_image_url(self):

        login_button = self.driver.find_element(By.XPATH, '''//button[text()="登录"]''')

        ActionChains(self.driver).move_to_element(login_button).click().perform()

        time.sleep(2)

        other_login_span = self.driver.find_element(By.XPATH, '''//span[text()="
          其他登录方式
        "]''')

        ActionChains(self.driver).move_to_element(other_login_span).click().perform()
        time.sleep(2)

        username_input = self.driver.find_element(By.XPATH, '//input[@name="loginPhoneOrEmail"]')
        password_input = self.driver.find_element(By.XPATH, '//input[@name="loginPassword"]')
        username_input.send_keys(self.juejin_username)
        password_input.send_keys(self.juejin_password)

        login_button = self.driver.find_element(By.XPATH, '''//button[text()="
        登录
      "]''')
        ActionChains(self.driver).move_to_element(login_button).click().perform()

        time.sleep(2)

        # 获取验证图片
        verify_image1 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[1]''')
        verify_image2 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[2]''')
        verify_image1_src = verify_image1.get_attribute("src")
        verify_image2_src = verify_image2.get_attribute("src")
        print(verify_image1_src, verify_image2_src)
        return verify_image1_src, verify_image2_src

    def juejin_slide_distance(self, slider_url, background_url):

        return self.get_element_slide_distance(slider_url, background_url) * 340/552

    @staticmethod
    def onload_save_img(slider_url, slider):
        r = requests.get(slider_url)
        with open(slider, 'wb') as f:
            f.write(r.content)

    def get_element_slide_distance(self, slider_url, background_url, correct=0):
        """
        根据传入滑块，和背景的节点，计算滑块的距离
        """

        # 下载验证码背景图,滑动图片
        self.onload_save_img(slider_url, self.slider)
        self.onload_save_img(background_url, self.background)
        # 读取进行色度图片，转换为numpy中的数组类型数据，
        slider_pic = cv2.imread(self.slider, 0)
        background_pic = cv2.imread(self.background, 0)
        # 获取缺口图数组的形状 -->缺口图的宽和高
        width, height = slider_pic.shape[::-1]
        
        cv2.imwrite(self.background_bak, background_pic)
        cv2.imwrite(self.slider_bak, slider_pic)
        # 读取另存的滑块图
        slider_pic = cv2.imread(self.slider_bak)
        # 进行色彩转换
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        # 获取色差的绝对值
        slider_pic = abs(255 - slider_pic)
        # 保存图片
        cv2.imwrite(self.slider_bak, slider_pic)
        # 读取滑块
        slider_pic = cv2.imread(self.slider_bak)
        # 读取背景图
        background_pic = cv2.imread(self.background_bak)
        # 比较两张图的重叠区域
        result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
        # 获取图片的缺口位置
        top, left = np.unravel_index(result.argmax(), result.shape)
        # 背景图中的图片缺口坐标位置
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))

        return left

    def __del__(self):
        self.driver.close()


if __name__ == "__main__":
    Juejin().run()
