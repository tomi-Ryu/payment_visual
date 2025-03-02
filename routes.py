from bottle import Bottle, template
from function.web_scraping import get_Rakuten_Billing_Statement_Csv
app = Bottle()

@app.get("/")
def get_Latest_Billing_statement_And_Save():
  # スクレイピングで取得
  get_Rakuten_Billing_Statement_Csv()
  
  return template("payment_Latest_Month")
