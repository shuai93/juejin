import traceback
import os

from core import Juejin, JuejinDriver


def main():
    if not os.path.exists("./temp"):
        os.mkdir("./temp")

    juejin_driver = JuejinDriver()
    try:
        juejin_cookies = juejin_driver.run()
        print(juejin_cookies)
        response = Juejin(juejin_cookies).get_draft()
        print(response)
    except Exception as e:
        traceback.print_exc()
        print(e)
    finally:
        juejin_driver.driver.close()
        juejin_driver.driver.quit()


if __name__ == "__main__":
    main()
