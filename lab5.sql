DROP PROCEDURE IF EXISTS PerformDistanceOperations;
DROP FUNCTION IF EXISTS GetMaxDistance;
DROP FUNCTION IF EXISTS GetMinDistance;
DROP FUNCTION IF EXISTS GetSumDistance;
DROP FUNCTION IF EXISTS GetAvgDistance;

DELIMITER //

CREATE FUNCTION GetMaxDistance() RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE max_value DECIMAL(10,2);
    SELECT MAX(distance) INTO max_value FROM flights;
    RETURN max_value;
END //

CREATE FUNCTION GetMinDistance() RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE min_value DECIMAL(10,2);
    SELECT MIN(distance) INTO min_value FROM flights;
    RETURN min_value;
END //

CREATE FUNCTION GetSumDistance() RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE sum_value DECIMAL(10,2);
    SELECT SUM(distance) INTO sum_value FROM flights;
    RETURN sum_value;
END //

CREATE FUNCTION GetAvgDistance() RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE avg_value DECIMAL(10,2);
    SELECT AVG(distance) INTO avg_value FROM flights;
    RETURN avg_value;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE PerformDistanceOperations()
BEGIN
    DECLARE max_value DECIMAL(10,2);
    DECLARE min_value DECIMAL(10,2);
    DECLARE sum_value DECIMAL(10,2);
    DECLARE avg_value DECIMAL(10,2);

    SET max_value = GetMaxDistance();
    SET min_value = GetMinDistance();
    SET sum_value = GetSumDistance();
    SET avg_value = GetAvgDistance();

    SELECT max_value AS MaxDistance,
           min_value AS MinDistance,
           sum_value AS SumDistance,
           avg_value AS AvgDistance;
END //

DELIMITER ;

CALL PerformDistanceOperations();
