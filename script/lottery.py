from core.juejin import Juejin

import requests

from requests import cookies


def lottery():
    # session id 自行设置
    session_id = "4085b767c41edc448faec9ab1b53dcb6"

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

    print(f"总抽奖次数为：{num - 1}")

    print("最终抽奖结果为：")
    for k, v in gift.items():
        print(f"礼物：{k} ---- 个数：{v}")


if __name__ == '__main__':
    lottery()
