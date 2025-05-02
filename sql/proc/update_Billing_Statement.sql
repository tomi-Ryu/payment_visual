/*
	スクレイピングで得た明細情報を保存。
	より詳細には、スクレイピングで得た情報の月単位の期間(ex: 202501~202502)のテーブルレコードを消してから、情報保存。
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
	DECLARE earliest_Statement_Day DATE;
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
			VALUES (CAST(JSON_EXTRACT(statement, '$[0]') as DATE), JSON_UNQUOTE(JSON_EXTRACT(statement, '$[1]')), JSON_EXTRACT(statement, '$[2]'));
			SET restCnt_statement = restCnt_statement - 1;
		END WHILE;

		## スクレイピング情報の月単位期間と被るテーブルレコードは全部消す
		# まず最新日の取得
		SELECT max(dt) INTO latest_Statement_Day
		FROM Statement_Tbl;
		# 一番古い日の取得
		SELECT min(dt) INTO earliest_Statement_Day
		FROM Statement_Tbl;
		# 明細情報テーブルレコード消去
		DELETE FROM Billing_Statement_Rakuten
		WHERE LAST_DAY(earliest_Statement_Day - INTERVAL 1 MONTH) < useDate AND useDate <= LAST_DAY(latest_Statement_Day);

		# 明細情報保存。内容が同じ明細を複数DLした可能性を考慮し、DISTINCT
		INSERT Billing_Statement_Rakuten(useDate, paymentTarget, cost)
		SELECT DISTINCT dt, paymentTarget, cost
		FROM Statement_Tbl;
	END IF;
	
	# プロシージャ単体で複数回実行することもあるから、消しておこう。
	DROP TABLE Statement_Tbl;
	
END//
DELIMITER ;