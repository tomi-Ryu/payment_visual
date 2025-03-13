DELIMITER //
CREATE FUNCTION func_test(
	test_str varchar(100)
)
RETURNS varchar(200)
BEGIN
	DECLARE AAA varchar(50);
    
	SELECT hoge INTO AAA
    FROM Test
    ORDER BY hoge DESC
    LIMIT 1;
    
    RETURN concat(test_str, AAA);
END//
DELIMITER ;