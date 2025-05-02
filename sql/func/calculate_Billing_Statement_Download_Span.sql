/*
if 明細データなし(基本的に、一度もダウンロードしていないのと同義)
	return 12 (最新月含む最大1年間分。1年間分DLできないならできるだけDLする)
else:
	return min(12, DB保存明細データの最新月から本コード実行時の月までの月数<ex:202503~202505→03/04/05の3つ>)
*/
USE PaymentVisual;
DELIMITER //
CREATE FUNCTION calculate_Billing_Statement_Download_Span()
RETURNS TINYINT
BEGIN
	DECLARE max_yyyymm_saved CHAR(6);
	DECLARE diff_Month TINYINT;

	# 明細データがあるかどうか判定。なければnullだがあればyyyymm
	SELECT DATE_FORMAT(max(useDate), "%Y%m") INTO max_yyyymm_saved
	FROM Billing_Statement_Rakuten;

	IF max_yyyymm_saved IS NULL
	THEN 
		RETURN 12;
	ELSE
		SET diff_Month = PERIOD_DIFF(DATE_FORMAT(curdate(), "%Y%m"), max_yyyymm_saved) + 1;

		IF diff_Month < 12
		THEN
			RETURN diff_Month;
		ELSE
			RETURN 12;
		END IF;
	END IF;

END//
DELIMITER ;