import glob
import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from const.const import ENAVI_LOGIN_URL, ENAVI_CSV_DL_PATH, ENAVI_BILLING_STATEMENT_BASE_URL, ENAVI_USER_ID, ENAVI_PASSWORD

def get_Enavi_Billing_Statement_Csv(month_span):
  def login():
    # ログインページ / ユーザid入力
    driver.get(ENAVI_LOGIN_URL)
    time.sleep(2)
    id_InputElement = driver.find_element(By.ID, "user_id")
    id_InputElement.clear()
    id_InputElement.send_keys(ENAVI_USER_ID)

    toInputPwd_btn = driver.find_element(By.ID, "cta001")
    toInputPwd_btn.click()
    time.sleep(2)

    # ログインページ / パスワード入力
    pwd_InputElement = driver.find_element(By.NAME, "password")
    pwd_InputElement.clear()
    pwd_InputElement.send_keys(ENAVI_PASSWORD)

    login_btn = driver.find_element(By.ID, "cta011")
    login_btn.click()
    time.sleep(5)

    # スクショでログイン成功か確認
    #driver.get_screenshot_as_file("./screenshots/login_or_not.png")

  # ENAVI_CSV_DL_PATHのすべてのCSVファイルを削除
  def all_billing_statement_delete():
    # 全CSVファイルを取得
    csv_files = glob.glob(os.path.join(ENAVI_CSV_DL_PATH, '*.csv'))

    # 全CSVファイルを削除
    for file in csv_files:
        os.remove(file)
  
  # 取得明細数はmonth_span。一番最近の明細から取る。
  def get_Enavi_billing_statement():
    for m_No in range(month_span):
      Url_curMonth = ENAVI_BILLING_STATEMENT_BASE_URL + str(m_No)
      driver.get(Url_curMonth)
      time.sleep(1)

      # 画面最下部に広告がある場合の対策。下にスクロールしクリック対象を広告より上にする。
      driver.execute_script('window.scrollBy(0, window.innerHeight);')

      csv_DL_Btn = driver.find_element(By.PARTIAL_LINK_TEXT, "CSV")
      csv_DL_Btn.click()
      time.sleep(1)

  # FireFoxブラウザをGUIなしで利用
  fp = webdriver.FirefoxProfile()
  fp.set_preference("browser.download.folderList", 2) # DL先を変更
  fp.set_preference("browser.download.dir", ENAVI_CSV_DL_PATH)
  options = webdriver.FirefoxOptions()
  options.add_argument('--headless')
  options.profile = fp
  driver = webdriver.Firefox(options=options)

  login()
  all_billing_statement_delete()
  
  get_Enavi_billing_statement()
    
  driver.quit()
