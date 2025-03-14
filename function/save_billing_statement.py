def save_billing_statement(db_connection):

  # 明細保存プロシージャ呼び出し
  with db_connection.cursor() as cursor:
    # 今はテスト用func,proc呼び出し
    cursor.callproc("proc_test", ("proc_OK?",))
    # 多分sql側でコミットすれば以下コードを消せる。
    db_connection.commit()
    cursor.execute("SELECT func_test(%s)", ("func_OK?"))

    return cursor.fetchone()


