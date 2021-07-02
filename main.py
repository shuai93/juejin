import traceback
import os

from core import Juejin, JuejinDriver


def main():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    juejin_driver = JuejinDriver()
    try:
        juejin_cookies = juejin_driver.run()
        draft_id, response = Juejin(juejin_cookies).push_draft_last_one()
        print(f"本次发布文章的id ：{draft_id}")
        print(f"本次发布文章的结果为：{response}")
    except Exception as e:
        traceback.print_exc()
        print(e)
    finally:
        juejin_driver.driver.close()
        juejin_driver.driver.quit()


if __name__ == "__main__":
    main()
