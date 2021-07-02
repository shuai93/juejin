import cv2
import numpy as np
import requests


class Track(object):
    # 处理前图片
    slider = "temp/slider.png"
    background = "temp/background.png"

    # 将处理之后的图片另存
    slider_bak = "temp/slider_bak.png"
    background_bak = "temp/background_bak.png"

    def get_track(self, slider_url, background_url) -> list:
        distance = self.get_slide_distance(slider_url, background_url)
        result = self.gen_normal_track(distance)
        return result

    @staticmethod
    def gen_normal_track(distance):
        def norm_fun(x, mu, sigma):
            pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
            return pdf

        result = []
        for i in range(-10, 10, 1):
            result.append(norm_fun(i, 0, 1) * distance)
        result.append(sum(result) - distance)
        return result

    @staticmethod
    def gen_track(distance):  # distance为传入的总距离
        # 移动轨迹
        result = []
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
            result.append(round(move))
        return result

    @staticmethod
    def onload_save_img(slider_url, slider):
        r = requests.get(slider_url)
        with open(slider, 'wb') as f:
            f.write(r.content)

    def get_slide_distance(self, slider_url, background_url):

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
        return left * 340 / 552


track = Track()


if __name__ == "__main__":
    Track()
