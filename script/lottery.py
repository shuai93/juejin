import requests
import argparse
import os
import importlib
import sys


from requests import cookies

# 导入掘金的包
project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.extend([project_dir])
core = importlib.import_module("core")


"""
一些参数
session_id = "4085b767dcb6"
"""

parser = argparse.ArgumentParser(description='掘金抽奖')
parser.add_argument('session_id', type=str, help='掘金cookies sessionid')


args = parser.parse_args()


def lottery(session_id):

    cookie = requests.cookies.create_cookie(
        domain=".juejin.cn",
        name="sessionid",
        value=session_id
    )
    juejin = core.Juejin(cookie_obj=cookie)
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

    print(f"总抽奖次数为：{num - 1}")

    print("最终抽奖结果为：")
    for k, v in gift.items():
        print(f"礼物：{k} ---- 个数：{v}")


if __name__ == '__main__':
    lottery(args.session_id)
