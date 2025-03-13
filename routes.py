from bottle import Bottle, template, static_file
from function.web_scraping import get_Rakuten_Billing_Statement_Csv
from function.save_billing_statement import save_billing_statement
app = Bottle()

@app.route('/static/<filePath:path>')
def provide_StaticFile(filePath):
  return static_file(filePath, root='./static/')

@app.get("/")
def get_And_Save_Latest_Billing_statement_And_Display_Latest_Payment():
  # スクレイピングで取得
  get_Rakuten_Billing_Statement_Csv()

  # 明細をDBに保存
  save_billing_statement()

  # 最新月分の支払いデータをドーナツグラフで表示
  return template("payment_Latest_Month", hoge="AAAAAAAAA")


