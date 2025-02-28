import glob
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

LOGIN_URL = "https://www.rakuten-card.co.jp/e-navi/auth/login.xhtml"
# "tabNo=" の直後に数字を入れて、参照月を指定。0:来月分支払い(今月利用分), 1: 今月支払い・・・
RAKUTEN_MEISAI_BASE_URL = "https://www.rakuten-card.co.jp/e-navi/members/statement/index.xhtml?tabNo="
# 絶対パスでないと動作しない
CSV_DL_PATH = "/Users/ryusuke.tomita/Desktop/payment_visual/billing_statement_latest_csv"

enavi_Auth = json.load(open("./secret/enavi_secret.json", "r", encoding="utf-8"))
user_Id = enavi_Auth["e-navi_login"]["user_id"]
password = enavi_Auth["e-navi_login"]["password"]

def login():
  # ログインページ / ユーザid入力
  driver.get(LOGIN_URL)
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

# CSV_DL_PATHのすべてのCSVファイルを削除
def all_billing_statement_delete():
  # 全CSVファイルを取得
  csv_files = glob.glob(os.path.join(CSV_DL_PATH, '*.csv'))

  # 全CSVファイルを削除
  for file in csv_files:
      os.remove(file)

def get_rakuten_billing_statement(month_span):
  for m_No in range(month_span):
    Url_curMonth = RAKUTEN_MEISAI_BASE_URL + str(m_No)
    driver.get(Url_curMonth)
    time.sleep(1)

    csv_DL_Btn = driver.find_element(By.PARTIAL_LINK_TEXT, "CSV")
    csv_DL_Btn.click()
    time.sleep(1)

# FireFoxブラウザをGUIなしで利用
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2) # DL先を変更
fp.set_preference("browser.download.dir", CSV_DL_PATH)
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.profile = fp
driver = webdriver.Firefox(options=options)

login()
all_billing_statement_delete()
# 引数: 取得明細数。一番最近の明細から取る。
get_rakuten_billing_statement(1)
  
driver.quit()
