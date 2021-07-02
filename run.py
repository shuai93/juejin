
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.config import juejin_username

chrome_options = Options()
chrome_options.add_argument('--headless')

print("juejin_username: " + juejin_username)

driver = webdriver.Chrome(executable_path="./driver/linux/chromedriver", chrome_options=chrome_options)
driver.get("https://juejin.cn/")

