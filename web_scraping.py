import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

enavi_Auth = json.load(open("./secret/enavi_secret.json", "r", encoding="utf-8"))
user_Id = enavi_Auth["e-navi_login"]["user_id"]
password = enavi_Auth["e-navi_login"]["password"]

def login(driver):
  # ログインページ / ユーザid入力
  driver.get('https://www.rakuten-card.co.jp/e-navi/auth/login.xhtml')
  time.sleep(1)
  id_InputElement = driver.find_element(By.ID, "user_id")
  id_InputElement.clear()
  id_InputElement.send_keys(user_Id)

  toInputPwd_btn = driver.find_element(By.ID, "cta001")
  toInputPwd_btn.click()
  time.sleep(1)

  # ログインページ / パスワード入力
  pwd_InputElement = driver.find_element(By.NAME, "password")
  pwd_InputElement.clear()
  pwd_InputElement.send_keys(password)

  login_btn = driver.find_element(By.ID, "cta011")
  login_btn.click()
  time.sleep(5)

  # スクショでログイン成功か確認
  driver.get_screenshot_as_file("./screenshots/login_or_not.png")


# FireFoxブラウザをGUIなしで利用
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

login(driver)

driver.quit()