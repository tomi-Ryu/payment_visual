from bottle import Bottle, template, static_file
from function.web_scraping import get_Rakuten_Billing_Statement_Csv
from function.save_billing_statement import save_billing_statement
app = Bottle()

@app.route('/static/<filePath:path>')
def provide_StaticFile(filePath):
  return static_file(filePath, root='./static/')

@app.get("/")
def get_Latest_Billing_statement_And_Save():
  # スクレイピングで取得
  get_Rakuten_Billing_Statement_Csv()

  # 明細をDBに保存
  hoge = str(save_billing_statement())

  
  return template("payment_Latest_Month", hoge=hoge)


