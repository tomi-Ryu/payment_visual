/*
	if 明細データなし(基本的に、一度もダウンロードしていないのと同義)
		return 12 (最新月含む最大1年間分。1年間分DLできないならできるだけDLする)
	else:
		return 1 (最新月分のみ)
*/
USE PaymentVisual;
DELIMITER //
CREATE FUNCTION calculate_Billing_Statement_Download_Span()
RETURNS TINYINT
BEGIN
	DECLARE download_Span TINYINT;
	DECLARE exist_Billing_Statement_Flg BOOLEAN;

	# 明細データがあるかどうか判定
	SELECT CASE COUNT(id) WHEN 0 THEN 0 ELSE 1 END INTO exist_Billing_Statement_Flg
	FROM Billing_Statement_Rakuten;

	IF exist_Billing_Statement_Flg = 0
	THEN 
		RETURN 12;
	ELSE
		RETURN 1;
	END IF;

END//
DELIMITER ;