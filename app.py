# DB接続
import json
import pymysql
from bottle import Bottle
from routes import setup_routes

DB_Auth = json.load(open("./secret/db_secret.json", "r", encoding="utf-8"))
host = DB_Auth["connectionInfo"]["host"]
user = DB_Auth["connectionInfo"]["user"]
password = DB_Auth["connectionInfo"]["password"]
db_name = DB_Auth["connectionInfo"]["db_name"]
db_connection = pymysql.connect(host=host, user=user, password=password, database=db_name)

app = Bottle()
setup_routes(app, db_connection)

if __name__ == '__main__':
  try:
    app.run(host='localhost', port=8080)
  finally:
    db_connection.close()


  