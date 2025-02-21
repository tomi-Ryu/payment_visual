from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
# Chromeを起動する
driver = webdriver.Chrome(options=options)
# Googleのページを開く
driver.get('https://www.google.com')
driver.get_screenshot_as_file("hoge.png")
driver.quit()