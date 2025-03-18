/*
スクレイピングで得た明細情報を保存。
最新月の情報は更新に近いことをする。つまりDeleteしてからInsert。
*/
USE PaymentVisual;
DELIMITER //
CREATE PROCEDURE update_Billing_Statement (
	statement_List json # 要素は[購入日,支払対象(店名or商品名),金額]というリスト
)
BEGIN
	DECLARE restCnt_Statement INT;
	DECLARE statement JSON;
	DECLARE latest_Statement_Day DATE;
	CREATE TEMPORARY TABLE Statement_Tbl (
		dt date,
		paymentTarget char(250),
		cost  mediumint
	);

	SET restCnt_statement = JSON_LENGTH(statement_List);
	IF restCnt_statement > 0 THEN
		# 明細情報を一時テーブルにInsert
		WHILE restCnt_statement > 0 DO
		SET statement = JSON_EXTRACT(statement_List, CONCAT('$','[',CAST(restCnt_statement-1 as CHAR) ,']'));
		INSERT Statement_Tbl(dt, paymentTarget, cost) 
		VALUES (CAST(JSON_EXTRACT(statement, '$[0]') as DATE), JSON_EXTRACT(statement, '$[1]'), JSON_EXTRACT(statement, '$[2]'));
		SET restCnt_statement = restCnt_statement - 1;
		END WHILE;

		## 最新月の明細情報は全部消す
		# まず最新日の取得
		SELECT dt INTO latest_Statement_Day
		FROM Statement_Tbl
		ORDER BY dt DESC
		LIMIT 1;
		# 最新日を利用し最新月の明細情報消去
		DELETE FROM Billing_Statement_Rakuten
		WHERE LAST_DAY(latest_Statement_Day - INTERVAL 1 MONTH) < useDate;

		# 明細情報保存
		INSERT Billing_Statement_Rakuten(useDate, paymentTarget, cost)
		SELECT dt, paymentTarget, cost
		FROM Statement_Tbl;
	END IF;
END//
DELIMITER ;