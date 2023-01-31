
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from .track import track
from .config import *


class JuejinDriver(object):

    # 掘金首页
    juejin_home = "https://juejin.cn"

    # 掘金签到页面
    juejin_sign = "https://juejin.cn/user/center/signin"

    # 截屏
    screenshot_verify_image = 'temp/verify_image.png'
    screenshot_prepare_login = 'temp/prepare_login.png'

    # 重试
    retry = 10

    # 最长等待时间
    wait = 10

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.juejin_username = JUEJIN_USERNAME
        self.juejin_password = JUEJIN_PASSWORD
        self.juejin_nickname = JUEJIN_NICKNAME
#         self.driver = webdriver.Chrome(executable_path="./driver/linux/chromedriver", chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=chrome_options)
        self.driver.implicitly_wait(self.wait)
        self.driver.get(self.juejin_home)

    def run(self):
        try:
            self.prepare_login()
        except Exception as e:
            self.driver.save_screenshot(self.screenshot_prepare_login)
            raise Exception("Prepare login is error" + str(e))
        flag = False
        for retry in range(self.retry):
            self.get_cookies()
            try:
                juejin_avatar_alt = self.juejin_nickname + "的头像"
                avatar = self.driver.find_element(By.XPATH, f'//img[@alt="{juejin_avatar_alt}"]')
                if avatar:
                    flag = True
                    break
            except NoSuchElementException:
                pass

        if flag is False:
            raise Exception(f"Verify slide image error and retry {self.retry}! ")

        return self.driver.get_cookies()

    def get_cookies(self):
        slider_url, background_url = self.get_verify_image_url()
        result = track.get_track(slider_url, background_url)
        self.click_and_move(result)

    def click_and_move(self, slide_track):
        verify_div = self.driver.find_element(By.XPATH, '''//div[@class="sc-kkGfuU bujTgx"]''')

        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(verify_div).perform()
        # 遍历轨迹进行滑动
        for t in slide_track:
            ActionChains(self.driver).move_by_offset(xoffset=t, yoffset=0).perform()
        # 释放鼠标
        time.sleep(0.2)
        ActionChains(self.driver).release(on_element=verify_div).perform()
        time.sleep(random.randint(2,5))


    def get_verify_image_url(self):

        # 获取验证图片
        verify_image1 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[1]''')
        verify_image2 = self.driver.find_element(By.XPATH, '''//img[@id="captcha-verify-image"]/../img[2]''')
        verify_image1_src = verify_image1.get_attribute("src")
        verify_image2_src = verify_image2.get_attribute("src")
        self.driver.save_screenshot(self.screenshot_verify_image)
        return verify_image1_src, verify_image2_src

    def prepare_login(self):

        login_button = self.driver.find_element(By.XPATH, '''//button[text()="
                登录
                "]''')

        ActionChains(self.driver).move_to_element(login_button).click().perform()
        
        time.sleep(5)

        other_login_span = self.driver.find_element(By.XPATH, '''//span[text()="
              密码登录
            "]''')

        ActionChains(self.driver).move_to_element(other_login_span).click().perform()

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

    def do_sign(self):
        self.driver.get("https://juejin.cn/user/center/signin")
        time.sleep(5)

        try:
            signed_button = self.driver.find_element(By.XPATH, '''//button[text()="
              今日已签到
            "]''')
        except NoSuchElementException:
            signed_button = None
            pass

        if signed_button is not None:
            print("*" * 10 + " 今日已签到！")
            return False

        try:
            sign_button = self.driver.find_element(By.XPATH, '''//button[text()="
              立即签到
            "]''')
        except NoSuchElementException:
            raise Exception("签到按钮获取失败，请查看页面是否有变化")
        ActionChains(self.driver).move_to_element(sign_button).click().perform()
        ActionChains(self.driver).move_to_element(sign_button).click().perform()
        time.sleep(2)
        print("-" * 10 + " > 签到结束！")
        return True
