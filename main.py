import traceback

from core import Juejin, JuejinDriver, EmailPoster
from core.config import *


def main():

    if not all([MAIL_TO, MAIL_PORT, MAIL_HOST, MAIL_ADDRESS, MAIL_PASSWORD, PUBLISH_SWITCH,
                MAIL_USER, JUEJIN_USERNAME, JUEJIN_PASSWORD, JUEJIN_NICKNAME, SWITCH]):
        raise Exception("Wrong configuration")

    if SWITCH != "on":
        return

    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    body = {
        'subject': "掘金自动发布结果",
        'to': [MAIL_TO],
    }
    # 掘金登录签到过程
    juejin_driver = JuejinDriver()
    juejin_cookies, sign_return = None, None

    try:
        juejin_cookies = juejin_driver.run()
        sign_return = juejin_driver.do_sign()
    except Exception as e:
        traceback.print_exc()
        body['body'] = "不好意登录签到遇到问题了， 结果为：" + str(e) + "\n"
    finally:
        juejin_driver.driver.close()
        juejin_driver.driver.quit()

    if juejin_cookies is None:
        EmailPoster().send(data=body)
        return

    juejin = Juejin(driver_cookies=juejin_cookies)

    body['payload'] = {
        "user": JUEJIN_NICKNAME,
    }

    if sign_return is True:
        lottery_result = juejin.draw_lottery()

        if lottery_result.get("err_no") == 0:
            message = "抽奖成功，奖品为：" + lottery_result.get("data", {}).get("lottery_name")

        else:
            message = "抽奖失败，接口返回值：" + str(lottery_result)

    elif sign_return is False:
        message = "今日已签到！"
    else:
        message = "未知结果？"

    body['payload']['sign_result'] = {
        "message": message
    }

    # 掘金发布文章过程
    if PUBLISH_SWITCH == "on":
        try:

            article = juejin.push_draft_last_one()
            body['payload']['publish_result'] = {
                "message": article.get("title", "") + " https://juejin.cn/post/" + article.get("article_id", ""),
            }
        except Exception as e:
            traceback.print_exc()
            body['payload']['publish_result'] = {
                "message": "不好意思发布遇到问题了， 结果为：" + str(e) + "\n"
            }

    EmailPoster().send(data=body)


if __name__ == "__main__":
    main()

