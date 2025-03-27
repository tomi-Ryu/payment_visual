/*
	特定月の確定支払額を返す。確定支払額は、明細データと固定費で構成。
	現状、返すデータは以下2種類のうちどれか。

	<1>: e-naviからDLした素のデータ。利用日時・支払い対象毎に区別されたデータ。
	<2>: e-naviのDLデータの同一支払い対象でgroup byしたデータ。

	<1>は、詳細データのみ保持。グラフ用データはnull。
	<2>は、グラフ用データと詳細データの2つある。
	詳細データ・グラフ用データ共に金額の降順にソートするが、グラフ用データにおいて10位以下は「その他」として1つにまとめる。
*/
USE PaymentVisual;
DELIMITER //
CREATE FUNCTION get_Confirmed_Monthly_Cost(
	yyyymm	CHAR(6),
	kind	TINYINT
)
RETURNS JSON
/*
	ex)
		<1>
		{
			"graph": null,
			"detail": [[null,"家賃",120000],["2025-01-05","オーケー",28000]]
		}

		<2>
		{
			"graph": {
				"paymentTarget":["家賃","オーケー"],
				"cost":[120000,28000],
				"color":["rgb(255, 0, 0)","rgb(255, 178, 153)"]
			},
			"detail": [["家賃",120000],["オーケー",20000],["オーケー",8000]]
		}
*/
BEGIN
	DECLARE graph JSON;
	DECLARE detail JSON;
	DECLARE cursorDone BOOLEAN;
	DECLARE ud DATE;
	DECLARE pt CHAR(250);
	DECLARE c MEDIUMINT;
	DECLARE sumC INT;
	DECLARE cnt INT;
	DECLARE rgbStr char(20);
	DECLARE graphLastRank TINYINT;

	DECLARE curOrigDetail CURSOR FOR
	SELECT useDate, paymentTarget, cost
	FROM baseTbl
	ORDER BY cost DESC, useDate ASC;

	DECLARE curGrp CURSOR FOR
	SELECT paymentTarget, cost, SUM(cost) OVER (PARTITION BY costRank)
	FROM (
		SELECT
			paymentTarget, 
			cost, 
			CASE WHEN ROW_NUMBER() OVER w < graphLastRank THEN ROW_NUMBER() OVER w ELSE graphLastRank END AS costRank
		FROM targetGroupTbl
		WINDOW w AS (ORDER BY cost DESC, paymentTarget ASC)
	) as Tbl
	ORDER BY costRank ASC, cost DESC;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET cursorDone = TRUE;

	CREATE TEMPORARY TABLE baseTbl (
		useDate DATE,
		paymentTarget CHAR(250),
		cost MEDIUMINT
	);
	CREATE TEMPORARY TABLE targetGroupTbl (
		paymentTarget CHAR(250),
		cost MEDIUMINT
	);

	# 返却データ全種類で使う情報をInsert
	INSERT INTO baseTbl(useDate, paymentTarget, cost)
	SELECT useDate, paymentTarget, cost
	FROM Billing_Statement_Rakuten
	WHERE CONCAT(yyyymm, '01') <= useDate AND useDate <= LAST_DAY(CONCAT(yyyymm, '01'))
	UNION ALL
	SELECT NULL, paymentTarget, cost
	FROM Fixed_Cost;

	SET cursorDone = FALSE;
	SET graph = JSON_OBJECT("paymentTarget", JSON_ARRAY(), "cost", JSON_ARRAY(), "color", JSON_ARRAY());
	SET graphLastRank = 10;
	SET detail = JSON_ARRAY();
	IF kind = 1 THEN
		# グラフデータは生成せず、e-navi明細通りのデータのみを作成。
		SET graph = NULL;

		# detailデータをカーソルで作成
		open curOrigDetail;
		loop1: LOOP    
			FETCH curOrigDetail INTO ud, pt, c;
			IF cursorDone THEN
				LEAVE loop1;
			END IF;
			SET detail = JSON_ARRAY_APPEND(detail, '$', JSON_ARRAY(ud, pt, c));
		END LOOP loop1;
		CLOSE curOrigDetail;

	ELSEIF kind = 2 THEN
		# graph・detailの元データを作成。
		INSERT INTO targetGroupTbl(paymentTarget, cost)
		SELECT paymentTarget, SUM(cost)
		FROM baseTbl
		GROUP BY paymentTarget;

		# graph・detailデータをカーソルで作成。
		open curGrp;
		SET cnt = 0;
		loop2: LOOP    
			FETCH curGrp INTO pt, c, sumC;
			IF cursorDone THEN
				LEAVE loop2;
			END IF;

			# graphデータ作成。コード行がそこまで増えなければ、カーソル部では格納のみの実装にさせた方がbetterか?
			SET cnt = cnt + 1;
			IF cnt <= graphLastRank THEN
				SELECT rgb INTO rgbStr FROM Graph_Color WHERE `rank` = cnt;

				IF cnt < graphLastRank THEN
					SET graph = JSON_ARRAY_APPEND(graph, '$.paymentTarget', pt);
				ELSE
					SET graph = JSON_ARRAY_APPEND(graph, '$.paymentTarget', "その他");
				END IF;
				SET graph = JSON_ARRAY_APPEND(graph, '$.cost', sumC);
				SET graph = JSON_ARRAY_APPEND(graph, '$.color', rgbStr);
			END IF;

			SET detail = JSON_ARRAY_APPEND(detail, '$', JSON_ARRAY(pt, c));
		END LOOP loop2;
		CLOSE curGrp;

	END IF;

	RETURN JSON_OBJECT('graph', graph, 'detail', detail);
END//
DELIMITER ;