DELIMITER //
CREATE PROCEDURE proc_test (
	test_str VARCHAR(100)
)
BEGIN

	DELETE FROM Test;
    
    INSERT Test(hoge) VALUES(CONCAT(test_str, "  " , SYSDATE()));
    
END//
DELIMITER ;