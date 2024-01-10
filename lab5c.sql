DROP PROCEDURE IF EXISTS CreateDynamicTables;

SHOW TABLES LIKE 'dynamic_table_%';

DELIMITER //

CREATE PROCEDURE CreateDynamicTables()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur_column_name VARCHAR(255);
    DECLARE column_count INT;

    DECLARE column_names_cursor CURSOR FOR
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = 'flights';

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN column_names_cursor;

    read_column_names: LOOP
        FETCH column_names_cursor INTO cur_column_name;
        IF done THEN
            LEAVE read_column_names;
        END IF;

        SET column_count = FLOOR(RAND() * 9) + 1; -- Random number of columns from 1 to 9

        -- Generate a more unique table name with a timestamp
        SET @table_name = CONCAT('dyn_table_', LEFT(cur_column_name, 20), '_', UNIX_TIMESTAMP());
        SET @sql = CONCAT('CREATE TABLE IF NOT EXISTS ', @table_name, ' (');

        -- Generate random columns
        SET @column_definitions = '';
        SET @i = 0;

        WHILE @i < column_count DO
            SET @column_name = CONCAT('column_', @i);
            SET @data_type = CASE ROUND(RAND() * 2)
                              WHEN 0 THEN 'INT'
                              WHEN 1 THEN 'VARCHAR(50)'
                              WHEN 2 THEN 'TEXT'
                              END;
            SET @column_definitions = CONCAT(@column_definitions, @column_name, ' ', @data_type, ', ');
            SET @i = @i + 1;
        END WHILE;

        -- Complete the SQL query to create the table
        SET @sql = CONCAT(@sql, SUBSTRING(@column_definitions, 1, LENGTH(@column_definitions) - 2), ')');

        -- Execute the generated SQL query
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END LOOP;

    CLOSE column_names_cursor;
END //

DELIMITER ;

CALL CreateDynamicTables();
