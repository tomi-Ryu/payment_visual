import datetime
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
    
    for_Cache_Buster = str(datetime.datetime.now())
    YYYY_hyphen_MM = for_Cache_Buster[:7]

    # 最新月分の支払いデータをドーナツグラフで表示
    return template("payment_Monthly_data",for_Cache_Buster=for_Cache_Buster, YYYY_hyphen_MM=YYYY_hyphen_MM)
  
  @app.get("/graph_detail_Monthly_data/<yyyy_MM>/<kind>")
  def get_graph_detail_Monthly_data(yyyy_MM, kind):
    cost_json = "{}"
    with db_connection.cursor() as cursor:
      # cost_jsonはプロシージャのOUTパラメータ。
      cursor.callproc("get_Confirmed_Monthly_Cost", (yyyy_MM, kind, cost_json))
      # OUTパラメータの値を取得。意味は公式doc参照  https://pymysql.readthedocs.io/en/latest/index.html
      cursor.execute("SELECT @_get_Confirmed_Monthly_Cost_2")
      cost_json = cursor.fetchone()[0]

    return cost_json
  
  ## 以下、基本的にエラーhttpステータスコードに対応したメソッドが実行される。

  @app.error(400)
  def error400(error):
    return "400 Bad Request"

  @app.error(404)
  def error404(error):
    return "404 Not Found"
  
  # 以下、bottle公式docより引用
  # All exceptions other than HTTPResponse or HTTPError will result in a 500 Internal Server Error response
  # 例えば、SQL処理でエラーが出た際に実行される。
  @app.error(500)
  def error500(error):
    return "500 Internal Server Error"

