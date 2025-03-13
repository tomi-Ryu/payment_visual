import json 
import pymysql

def save_billing_statement():
  DB_Auth = json.load(open("./secret/db_secret.json", "r", encoding="utf-8"))
  host = DB_Auth["connectionInfo"]["host"]
  user = DB_Auth["connectionInfo"]["user"]
  password = DB_Auth["connectionInfo"]["password"]
  db_name = DB_Auth["connectionInfo"]["db_name"]

  # DB接続
  connection = pymysql.connect(host=host, user=user, password=password, database=db_name)

  # 明細保存プロシージャ呼び出し
  with connection:
    with connection.cursor() as cursor:
      # 今はテスト用func,proc呼び出し
      cursor.callproc("proc_test", ("proc_OK?",))
      # 多分sql側でコミットすれば以下コードを消せる。
      connection.commit()
      cursor.execute("SELECT func_test(%s)", ("func_OK?"))

      return cursor.fetchone()


