import csv
import glob
import json
import os
from const.const import ENAVI_CSV_DL_PATH

def save_billing_statement(db_connection):
  ## DLしたCSVファイルからsave_Data_Listをセット ##
  # save_Data_Listの要素は、[購入日,支払対象(店名or商品名),金額]というリスト
  save_Data_List = []
  csv_files = glob.glob(os.path.join(ENAVI_CSV_DL_PATH, '*.csv'))
  for file in csv_files:
    with open(file) as f:
      first_Row = True
      for row in csv.reader(f):
        if first_Row == True:
          # 1行目は2行目以降に格納されている値の説明
          first_Row = False
          continue      
        save_Element_List = []
        save_Element_List.append(row[0]) # YYYY/MM/DD
        save_Element_List.append(row[1]) # 支払対象情報
        save_Element_List.append(row[6]) # 支払総額

        save_Data_List.append(save_Element_List[:])
  
  # 明細保存プロシージャ呼び出し
  with db_connection.cursor() as cursor:
    cursor.callproc("update_Billing_Statement", (json.dumps(save_Data_List),))
    db_connection.commit()

