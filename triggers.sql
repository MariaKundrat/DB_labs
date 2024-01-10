DROP TRIGGER IF EXISTS CheckValidName_Countries;

DELIMITER //

CREATE TRIGGER CheckValidName_Countries BEFORE INSERT ON countries
FOR EACH ROW
BEGIN
    IF NEW.name NOT IN ('Ukraine', 'Poland', 'France') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid name: Should be Ukraine, Poland, France';
    END IF;
END//

DELIMITER ;

DROP TRIGGER IF EXISTS Prevent_double_zeros_model;
DELIMITER //
CREATE TRIGGER Prevent_double_zeros_model
BEFORE INSERT ON planes
FOR EACH ROW
BEGIN
    IF NEW.model LIKE '%00' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Value cannot end with double zeros';
    END IF;
END;
// 
DELIMITER ;

DROP TRIGGER IF EXISTS Prevent_modification_flights_have_passengers;
DELIMITER //
CREATE TRIGGER Prevent_modification_flights_have_passengers
BEFORE UPDATE ON flights_have_passengers
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Modification of data in "flights_have_passengers" table is not allowed';
END;
//
DELIMITER ;
