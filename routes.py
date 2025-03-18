from bottle import template, static_file
from function.web_scraping import get_Enavi_Billing_Statement_Csv
from function.save_billing_statement import save_billing_statement

def setup_routes(app, db_connection):
  @app.route('/static/<filePath:path>')
  def provide_StaticFile(filePath):
    return static_file(filePath, root='./static/')

  @app.get("/")
  def get_And_Save_Latest_Billing_statement_And_Display_Latest_Payment():
    with db_connection.cursor() as cursor:
      cursor.execute("SELECT calculate_Billing_Statement_Download_Span()")
      download_Span = cursor.fetchone()[0]

    # スクレイピングで取得。取得明細数はdownload_Span
    #get_Enavi_Billing_Statement_Csv(download_Span)

    # 明細をDBに保存
    #save_billing_statement(db_connection)

    # 最新月分の支払いデータをドーナツグラフで表示
    return template("payment_Latest_Month")


