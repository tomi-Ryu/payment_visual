import json

######## e-navi操作関連 ########
ENAVI_LOGIN_URL = "https://www.rakuten-card.co.jp/e-navi/auth/login.xhtml"
# "tabNo=" の直後に数字を入れて、参照月を指定。0:来月分支払い(今月利用分), 1: 今月支払い・・・
ENAVI_BILLING_STATEMENT_BASE_URL = "https://www.rakuten-card.co.jp/e-navi/members/statement/index.xhtml?tabNo="
# 絶対パスでないと動作しない
ENAVI_CSV_DL_PATH = "/Users/ryusuke.tomita/Desktop/payment_visual/billing_statement_latest_csv"
# ログイン情報
enavi_Auth = json.load(open("./const/secret/enavi_secret.json", "r", encoding="utf-8"))
ENAVI_USER_ID = enavi_Auth["e-navi_login"]["user_id"]
ENAVI_PASSWORD = enavi_Auth["e-navi_login"]["password"]

######## DB ########
DB_AUTH = json.load(open("./const/secret/db_secret.json", "r", encoding="utf-8"))["connectionInfo"]