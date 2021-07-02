
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.config import JUEJIN_USERNAME

chrome_options = Options()
chrome_options.add_argument('--headless')

print("juejin_username: " + str(JUEJIN_USERNAME))

driver = webdriver.Chrome(executable_path="./driver/linux/chromedriver", chrome_options=chrome_options)
driver.get("https://juejin.cn/")

