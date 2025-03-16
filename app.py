import pymysql
from bottle import Bottle
from routes import setup_routes
from const.const import DB_AUTH

# 辞書型変数DB_AUTHを**で展開
db_connection = pymysql.connect(**DB_AUTH)

app = Bottle()
setup_routes(app, db_connection)

if __name__ == '__main__':
  try:
    app.run(host='localhost', port=8080)
  finally:
    db_connection.close()


  