import pymysql
from bottle import Bottle
from routes import setup_routes
from const.const import DB_AUTH
from function.web_scraping import get_Enavi_Billing_Statement_Csv
from function.save_billing_statement import save_billing_statement

# 辞書型変数DB_AUTHを**で展開
db_connection = pymysql.connect(**DB_AUTH)

app = Bottle()
setup_routes(app, db_connection)

if __name__ == '__main__':
  try:
    with db_connection.cursor() as cursor:
      cursor.execute("SELECT calculate_Billing_Statement_Download_Span()")
      download_Span = cursor.fetchone()[0]

    # スクレイピングで取得。取得明細数はdownload_Span
    get_Enavi_Billing_Statement_Csv(download_Span)

    # 明細をDBに保存
    save_billing_statement(db_connection)

    app.run(host='localhost', port=8080)
  finally:
    db_connection.close()


  