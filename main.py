import traceback

from core import Juejin, JuejinDriver, EmailPoster
from core.config import *


def main():

    if not all([MAIL_TO, MAIL_PORT, MAIL_HOST, MAIL_ADDRESS, MAIL_PASSWORD,
                MAIL_USER, JUEJIN_USERNAME, JUEJIN_PASSWORD, JUEJIN_NICKNAME, SWITCH]):
        raise Exception("Wrong configuration")

    if SWITCH != "on":
        return

    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    juejin_driver = JuejinDriver()
    body = {
        'subject': "掘金自动发布结果",
        'to': [MAIL_TO],
    }
    try:
        juejin_cookies = juejin_driver.run()
        article = Juejin(driver_cookies=juejin_cookies).push_draft_last_one()

        body['payload'] = {
            "result": {
                "title": article.get("title", ""),
                "article_id": article.get("article_id", ""),
            },
            "user": JUEJIN_NICKNAME
        }
    except Exception as e:
        traceback.print_exc()
        body['body'] = "不好意思发布遇到问题了， 结果为：" + str(e)
    finally:
        juejin_driver.driver.close()
        juejin_driver.driver.quit()

    EmailPoster().send(data=body)


if __name__ == "__main__":
    main()
